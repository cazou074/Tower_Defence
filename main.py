import pygame as pg
import random

pg.init()

Screen = pg.display.set_mode((800, 600))
pg.display.set_caption("Tower defence")

clock = pg.time.Clock()
projectile_speed = 5
enemies_speed = 3

Wave = 1
Money = 0


class Enemies:
    def __init__(self):
        self.rect = pg.Rect(0, 0, 20, 20)
        self.health = 5
        self.damage = 1
        self.color = (255, 0, 0)

    def draw(self):
        pg.draw.rect(Screen, self.color, self.rect)

    def moving(self):
        centre_a = pg.Vector2(self.rect.center)
        centre_b = pg.Vector2(400, 300)
        vector_direction = centre_b - centre_a
        if vector_direction.length() > 1:
            vector_direction.normalize_ip()
            self.rect.center += vector_direction * enemies_speed

    def new_pos(self):
        self.rect.center = (random.randint(0, 800), random.randint(0, 600))


class Tower:
    def __init__(self):
        self.rect = pg.Rect(400, 300, 20, 20)
        self.health = 100
        self.level = 1
        self.color = (0, 255, 0)

    def draw(self):
        pg.draw.rect(Screen, self.color, self.rect, 0, 0, 15, 15, 15, 15)


class Projectile:
    def __init__(self):
        self.rect = pg.Rect(0, 0, 5, 5)
        self.damage = 1
        self.color = "Yellow"

    def draw(self):
        pg.draw.rect(Screen, self.color, self.rect)

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
        self.rect = pg.Rect(0, 0, 40, 40)
        self.health = 100
        self.color = (0, 0, 255)
        self.hover_color = '#666666'
        self.is_hovered = False
        self.is_pressed = False
        self.dragging = True  # suit la souris dès la création
        self.locked_pos = (400, 550)
        self.locked = False
        self.projectile = Projectile()

    def draw(self):
        pg.draw.rect(Screen, self.color, self.rect, 0, 0, 15, 15, 15, 15)

    def pos(self):
        if self.dragging:
            self.rect.center = pg.mouse.get_pos()
        else:
            self.rect.center = self.locked_pos

    def update(self, events):
        mouse_pos = pg.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        self.is_pressed = self.is_hovered and pg.mouse.get_pressed()[0]

        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.dragging:
                    self.locked_pos = self.rect.center
                    self.dragging = False
                    self.locked = True
                    self.projectile.rect.center = self.locked_pos
                elif self.is_hovered and not self.locked:
                    self.dragging = True


def is_collision(defences):
    global enemies
    for e in enemies:
        if pg.Rect.colliderect(tower.rect, e.rect):
            tower.health -= 1
            e.new_pos()
        for d in defences:
            if d.locked and pg.Rect.colliderect(d.projectile.rect, e.rect):
                e.health -= 1
                d.projectile.rect.center = d.locked_pos

    # supprime les ennemis à 0 vie
    enemies = [e for e in enemies if e.health > 0]


tower = Tower()
defences = []
enemies = [Enemies() for _ in range(1)]
for e in enemies:
    e.new_pos()

running = True
while running:

    events = pg.event.get()

    for event in events:
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN and event.key == pg.K_b:
            defences.append(Defence())

    if tower.health > 0:
        Screen.fill((0, 0, 0))
        tower.draw()
        is_collision(defences)

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