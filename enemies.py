import random
from parameters import *


class Enemies:
    def __init__(self, wave):
        self.rect = pg.Rect(0, 0, 20, 20)
        self.wave = wave
        # +1 PV tous les 3 vagues
        self.health = 1 + (wave // 3)
        self.max_health = self.health
        self.damage = 1
        # plus la vague est haute, plus la couleur est foncée
        intensity = max(255 - wave * 15, 60)
        self.color = (intensity, 0, 0)

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