import pygame as pg
import random

pg.init()

Screen = pg.display.set_mode((800, 600))
pg.display.set_caption("Tower defence")

clock = pg.time.Clock()
font_big = pg.font.SysFont(None, 22)
font_small = pg.font.SysFont(None, 18)

projectile_speed = 3
enemies_speed = 1

DEFENCE_COST = 20
ENEMY_REWARD = 10
TOWER_POS = (420, 320)
MIN_SPAWN_DIST = 150

# Layout
LEFT_PANEL_W = 50
RIGHT_PANEL_W = 110
TOP_BAR_H = 40
GAME_X = LEFT_PANEL_W
GAME_Y = TOP_BAR_H
GAME_W = 800 - LEFT_PANEL_W - RIGHT_PANEL_W
GAME_H = 600 - TOP_BAR_H

Wave = 1
Money = 20
defence_amount = 0
builder_mode = False


class Enemies:
    def __init__(self):
        self.rect = pg.Rect(0, 0, 20, 20)
        self.health = 1
        self.damage = 1
        self.color = (255, 0, 0)

    def draw(self):
        pg.draw.rect(Screen, self.color, self.rect)

    def moving(self):
        centre_a = pg.Vector2(self.rect.center)
        centre_b = pg.Vector2(TOWER_POS)
        vector_direction = centre_b - centre_a
        if vector_direction.length() > 1:
            vector_direction.normalize_ip()
            self.rect.center += vector_direction * enemies_speed

    def new_pos(self):
        while True:
            x = random.randint(GAME_X, GAME_X + GAME_W)
            y = random.randint(GAME_Y, GAME_Y + GAME_H)
            dist = pg.Vector2(x, y).distance_to(pg.Vector2(TOWER_POS))
            if dist >= MIN_SPAWN_DIST:
                self.rect.center = (x, y)
                break


class Tower:
    def __init__(self):
        self.rect = pg.Rect(TOWER_POS[0] - 10, TOWER_POS[1] - 10, 25, 25)
        self.health = 100
        self.max_health = 100
        self.color = (0, 255, 0)

    def draw(self):
        pg.draw.rect(Screen, self.color, self.rect, 0, 0, 15, 15, 15, 15)


class Projectile:
    def __init__(self):
        self.rect = pg.Rect(0, 0, 5, 5)
        self.damage = 1
        self.color = "Yellow"

    def draw(self):
        pg.draw.rect(Screen, self.color, self.rect, 0, 0, 15, 15, 15, 15)

    def moving(self, enemies):
        if not enemies:
            return
        centre_a = pg.Vector2(self.rect.center)
        cible = min(enemies, key=lambda e: centre_a.distance_to(pg.Vector2(e.rect.center)))
        centre_b = pg.Vector2(cible.rect.center)
        vector_direction = centre_b - centre_a
        if vector_direction.length() > 1:
            vector_direction.normalize_ip()
            self.rect.center += vector_direction * projectile_speed


class Defence:
    def __init__(self):
        self.rect = pg.Rect(0, 0, 20, 20)
        self.health = 100
        self.color = (0, 100, 255)
        self.is_hovered = False
        self.dragging = True
        self.locked_pos = (TOWER_POS[0], TOWER_POS[1] + 100)
        self.locked = False
        self.projectile = Projectile()

    def draw(self):
        pg.draw.rect(Screen, self.color, self.rect, 0, 0, 8, 8, 8, 8)

    def pos(self):
        if self.dragging:
            self.rect.center = pg.mouse.get_pos()
        else:
            self.rect.center = self.locked_pos

    def update(self, events):
        global builder_mode
        mouse_pos = pg.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.dragging:
                    self.locked_pos = self.rect.center
                    self.dragging = False
                    self.locked = True
                    builder_mode = False
                    self.projectile.rect.center = self.locked_pos
                elif self.is_hovered and not self.locked:
                    self.dragging = True


def spawn_wave(wave_number):
    nb = wave_number * 3
    new_enemies = [Enemies() for _ in range(nb)]
    for e in new_enemies:
        e.new_pos()
    return new_enemies, nb


def is_collision(defences):
    global enemies, Money
    for e in enemies:
        if pg.Rect.colliderect(tower.rect, e.rect):
            tower.health -= 1
            e.new_pos()
        for d in defences:
            if d.locked and pg.Rect.colliderect(d.projectile.rect, e.rect):
                e.health -= d.projectile.damage
                d.projectile.rect.center = d.locked_pos

    dead = [e for e in enemies if e.health <= 0]
    Money += len(dead) * ENEMY_REWARD
    enemies = [e for e in enemies if e.health > 0]


def draw_hud():
    # ── fond des panneaux ──────────────────────────────────
    pg.draw.rect(Screen, (20, 20, 20), (0, 0, LEFT_PANEL_W, 600))
    pg.draw.rect(Screen, (20, 20, 20), (800 - RIGHT_PANEL_W, 0, RIGHT_PANEL_W, 600))
    pg.draw.rect(Screen, (20, 20, 20), (0, 0, 800, TOP_BAR_H))

    # ── barre vague (rouge, haut centre) ──────────────────
    bx, by = GAME_X + 10, 8
    bw, bh = GAME_W - 20, 24
    pg.draw.rect(Screen, (60, 20, 20), (bx, by, bw, bh), 0, 5)
    if total_enemies > 0:
        ratio = len(enemies) / total_enemies
        pg.draw.rect(Screen, (210, 50, 50), (bx, by, int(bw * ratio), bh), 0, 5)
    pg.draw.rect(Screen, (255, 80, 80), (bx, by, bw, bh), 2, 5)
    label = font_big.render(f"Vague {Wave}  —  {len(enemies)} / {total_enemies}", True, (255, 255, 255))
    Screen.blit(label, (bx + bw // 2 - label.get_width() // 2, by + 4))

    # ── barre vie tour (verte, gauche verticale) ───────────
    bx2, by2 = 8, TOP_BAR_H + 10
    bw2, bh2 = 34, GAME_H - 20
    pg.draw.rect(Screen, (20, 60, 20), (bx2, by2, bw2, bh2), 0, 5)
    ratio_hp = max(tower.health / tower.max_health, 0)
    filled_h = int(bh2 * ratio_hp)
    pg.draw.rect(Screen, (60, 210, 60), (bx2, by2 + bh2 - filled_h, bw2, filled_h), 0, 5)
    pg.draw.rect(Screen, (80, 255, 80), (bx2, by2, bw2, bh2), 2, 5)
    hp_label = font_small.render("HP", True, (200, 255, 200))
    Screen.blit(hp_label, (bx2 + bw2 // 2 - hp_label.get_width() // 2, by2 - 16))
    hp_val = font_small.render(str(tower.health), True, (255, 255, 255))
    Screen.blit(hp_val, (bx2 + bw2 // 2 - hp_val.get_width() // 2, by2 + 4))

    # ── panneau droite ─────────────────────────────────────
    rx = 800 - RIGHT_PANEL_W + 8
    rw = RIGHT_PANEL_W - 16

    # money (jaune)
    pg.draw.rect(Screen, (80, 70, 0), (rx, 8, rw, 28), 0, 5)
    pg.draw.rect(Screen, (255, 215, 0), (rx, 8, rw, 28), 2, 5)
    money_label = font_big.render(f"${Money}", True, (255, 215, 0))
    Screen.blit(money_label, (rx + rw // 2 - money_label.get_width() // 2, 13))

    # défenses (bleu)
    pg.draw.rect(Screen, (0, 20, 60), (rx, TOP_BAR_H + 6, rw, GAME_H - 12), 0, 5)
    pg.draw.rect(Screen, (0, 120, 255), (rx, TOP_BAR_H + 6, rw, GAME_H - 12), 2, 5)
    def_title = font_small.render("Défenses", True, (150, 200, 255))
    Screen.blit(def_title, (rx + rw // 2 - def_title.get_width() // 2, TOP_BAR_H + 10))

    # slot achat
    slot_y = TOP_BAR_H + 32
    can_afford = Money >= DEFENCE_COST
    slot_color = (0, 80, 200) if can_afford and not builder_mode else (50, 50, 80)
    pg.draw.rect(Screen, slot_color, (rx, slot_y, rw, 50), 0, 5)
    pg.draw.rect(Screen, (0, 150, 255) if can_afford else (80, 80, 100), (rx, slot_y, rw, 50), 2, 5)
    b_label = font_big.render("[B]", True, (255, 255, 255))
    cost_label = font_small.render(f"${DEFENCE_COST}", True, (255, 215, 0) if can_afford else (150, 150, 150))
    Screen.blit(b_label, (rx + rw // 2 - b_label.get_width() // 2, slot_y + 6))
    Screen.blit(cost_label, (rx + rw // 2 - cost_label.get_width() // 2, slot_y + 28))

    global defence_amount
    for i, d in enumerate(defences):
        defence_amount = i + 1

    dy = slot_y + 60
    d_label = font_small.render(f"amount :{defence_amount}", True, (150, 200, 255))
    Screen.blit(d_label, (rx + 4, dy))


tower = Tower()
defences = []
enemies, total_enemies = spawn_wave(Wave)

running = True
while running:
    events = pg.event.get()

    for event in events:
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN and event.key == pg.K_b:
            if Money >= DEFENCE_COST and not builder_mode:
                builder_mode = True
                Money -= DEFENCE_COST
                defences.append(Defence())

    if tower.health > 0:
        # zone de jeu
        pg.draw.rect(Screen, (0, 0, 0), (GAME_X, GAME_Y, GAME_W, GAME_H))

        tower.draw()
        is_collision(defences)
        draw_hud()

        if len(enemies) == 0:
            Wave += 1
            enemies, total_enemies = spawn_wave(Wave)

        for d in defences:
            d.draw()
            d.pos()
            d.update(events)
            if d.locked:
                d.projectile.draw()
                d.projectile.moving(enemies)

        for e in enemies:
            e.moving()
            e.draw()

        pg.display.flip()
        clock.tick(60)

pg.quit()