from parameters import *

class Tower:
    def __init__(self):
        self.rect = pg.Rect(TOWER_POS[0] - 10, TOWER_POS[1] - 10, 30, 30)
        self.health = 100
        self.max_health = 100
        self.color = (0, 255, 0)

    def draw(self):
        pg.draw.rect(Screen, self.color, self.rect, 0, 0, 15, 15, 15, 15)
