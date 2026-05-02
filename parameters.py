import pygame as pg

pg.init()

Screen = pg.display.set_mode((800, 600))
pg.display.set_caption("Tower defence")

projectile_speed = 3
enemies_speed = 1
DEFENCE_COST = 20
ENEMY_REWARD = 0.5
TOWER_POS = (385, 285)
MIN_SPAWN_DIST = 150
LEFT_PANEL_W = 50
RIGHT_PANEL_W = 110
TOP_BAR_H = 40
GAME_X = LEFT_PANEL_W
GAME_Y = TOP_BAR_H
GAME_W = 800 - LEFT_PANEL_W - RIGHT_PANEL_W
GAME_H = 600 - TOP_BAR_H

