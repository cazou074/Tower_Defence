from hud import *
from parameters import *
from enemies import Enemies
from tower import Tower
from defences import Defence
import state

clock = pg.time.Clock()

def spawn_wave(wave_number):
    # croissance exponentielle : 3, 4, 6, 9, 13, 19...
    nb = int(3 * (1.3 ** (wave_number - 1)))
    new_enemies = [Enemies(wave_number) for _ in range(nb)]
    for e in new_enemies:
        e.new_pos()
    return new_enemies, nb


def is_collision(defences):
    global enemies

    enemy_ids_before = set(id(e) for e in enemies)

    for e in enemies:
        if pg.Rect.colliderect(tower.rect, e.rect):
            tower.health -= 1
            e.new_pos()
        for d in defences:
            if d.locked and d.projectile and d.projectile.active:
                if pg.Rect.colliderect(d.projectile.rect, e.rect):
                    e.health -= d.projectile.damage
                    d.projectile.rect.center = d.locked_pos

    # ennemis morts
    dead_count = sum(1 for e in enemies if e.health <= 0)
    state.Money += dead_count * ENEMY_REWARD
    enemies = [e for e in enemies if e.health > 0]

    # reset projectiles si leur cible a disparu
    living_ids = set(id(e) for e in enemies)
    for d in defences:
        if d.locked and d.projectile:
            # si plus aucun ennemi ou projectile hors zone → reset
            proj_center = pg.Vector2(d.projectile.rect.center)
            in_bounds = (GAME_X <= proj_center.x <= GAME_X + GAME_W and
                         GAME_Y <= proj_center.y <= GAME_Y + GAME_H)
            if not enemies or not in_bounds:
                d.projectile.reset()


tower = Tower()
defences = []
enemies, total_enemies = spawn_wave(state.Wave)

running = True
while running:
    events = pg.event.get()

    for event in events:
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN and event.key == pg.K_b:
            if state.Money >= state.DEFENCE_COST and not state.builder_mode:
                state.builder_mode = True
                print("builder mode", state.builder_mode)
                state.Money -= state.DEFENCE_COST
                state.DEFENCE_COST = round(state.DEFENCE_COST * 1.5, 1)
                defences.append(Defence())

    if tower.health > 0:
        pg.draw.rect(Screen, (0, 0, 0), (GAME_X, GAME_Y, GAME_W, GAME_H))

        tower.draw()
        is_collision(defences)
        draw_hud(Screen, tower, enemies, total_enemies, defences, state.Wave, state.Money, state.DEFENCE_COST, state.builder_mode)

        if len(enemies) == 0:
            state.Wave += 1
            enemies, total_enemies = spawn_wave(state.Wave)

        for d in defences:
            d.draw()
            d.pos()
            d.update(events)
            if d.locked and d.projectile:
                d.projectile.draw()
                d.projectile.moving(enemies)

        for e in enemies:
            e.moving()
            e.draw()

        pg.display.flip()
        clock.tick(60)

pg.quit()