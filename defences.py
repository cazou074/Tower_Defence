from parameters import *
import state

class Defence:
    def __init__(self):
        self.rect = pg.Rect(0, 0, 20, 20)
        self.health = 100
        self.color = (0, 100, 255)
        self.is_hovered = False
        self.dragging = True
        self.locked_pos = (TOWER_POS[0], TOWER_POS[1] + 100)
        self.locked = False
        self.projectile = None  # créé au moment du placement

    def draw(self):
        pg.draw.rect(Screen, self.color, self.rect, 0, 0, 8, 8, 8, 8)

    def pos(self):
        if self.dragging:
            mouse = pg.mouse.get_pos()
            # empêche de poser dans les panneaux
            x = max(GAME_X + 10, min(mouse[0], GAME_X + GAME_W - 10))
            y = max(GAME_Y + 10, min(mouse[1], GAME_Y + GAME_H - 10))
            self.rect.center = (x, y)
        else:
            self.rect.center = self.locked_pos

    def update(self, events):
        mouse_pos = pg.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.dragging:
                    self.locked_pos = self.rect.center
                    self.dragging = False
                    self.locked = True
                    state.builder_mode = False
                    self.projectile = Projectile(self.locked_pos)
                elif not state.builder_mode:
                    state.builder_mode = True




class Projectile:
    def __init__(self, start_pos):
        self.rect = pg.Rect(0, 0, 5, 5)
        self.rect.center = start_pos
        self.start_pos = start_pos
        self.damage = 1
        self.color = "Yellow"
        self.active = True

    def draw(self):
        if self.active:
            pg.draw.rect(Screen, self.color, self.rect)

    def moving(self, enemies):
        if not self.active or not enemies:
            return

        centre_a = pg.Vector2(self.rect.center)
        cible = min(enemies, key=lambda e: centre_a.distance_to(pg.Vector2(e.rect.center)))
        centre_b = pg.Vector2(cible.rect.center)
        vector_direction = centre_b - centre_a

        if vector_direction.length() > 1:
            vector_direction.normalize_ip()
            self.rect.center += vector_direction * projectile_speed
        else:
            # a touché la cible
            cible.health -= self.damage
            self.rect.center = self.start_pos

    def reset(self):
        self.rect.center = self.start_pos
        self.active = True
