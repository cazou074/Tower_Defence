from parameters import *

font_big = pg.font.SysFont(None, 22)
font_small = pg.font.SysFont(None, 18)



def draw_hud(Screen, tower, enemies, total_enemies, defences, Wave, Money, DEFENCE_COST, builder_mode):
    pg.draw.rect(Screen, (20, 20, 20), (0, 0, LEFT_PANEL_W, 600))
    pg.draw.rect(Screen, (20, 20, 20), (800 - RIGHT_PANEL_W, 0, RIGHT_PANEL_W, 600))
    pg.draw.rect(Screen, (20, 20, 20), (0, 0, 800, TOP_BAR_H))

    # barre vague (rouge, haut centre)
    bx, by = GAME_X + 10, 8
    bw, bh = GAME_W - 20, 24
    pg.draw.rect(Screen, (60, 20, 20), (bx, by, bw, bh), 0, 5)
    if total_enemies > 0:
        ratio = len(enemies) / total_enemies
        pg.draw.rect(Screen, (210, 50, 50), (bx, by, int(bw * ratio), bh), 0, 5)
    pg.draw.rect(Screen, (255, 80, 80), (bx, by, bw, bh), 2, 5)
    label = font_big.render(f"Vague {Wave}  —  {len(enemies)} / {total_enemies}", True, (255, 255, 255))
    Screen.blit(label, (bx + bw // 2 - label.get_width() // 2, by + 4))

    # barre vie tour (verte, gauche verticale)
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

    # panneau droite
    rx = 800 - RIGHT_PANEL_W + 8
    rw = RIGHT_PANEL_W - 16

    # money (jaune) — arrondi à 1 décimale
    pg.draw.rect(Screen, (80, 70, 0), (rx, 8, rw, 28), 0, 5)
    pg.draw.rect(Screen, (255, 215, 0), (rx, 8, rw, 28), 2, 5)
    money_label = font_big.render(f"${round(Money, 1)}", True, (255, 215, 0))
    Screen.blit(money_label, (rx + rw // 2 - money_label.get_width() // 2, 13))

    # panneau défenses (bleu)
    pg.draw.rect(Screen, (0, 20, 60), (rx, TOP_BAR_H + 6, rw, GAME_H - 12), 0, 5)
    pg.draw.rect(Screen, (0, 120, 255), (rx, TOP_BAR_H + 6, rw, GAME_H - 12), 2, 5)
    def_title = font_small.render("Défenses", True, (150, 200, 255))
    Screen.blit(def_title, (rx + rw // 2 - def_title.get_width() // 2, TOP_BAR_H + 10))

    # slot achat
    slot_y = TOP_BAR_H + 32
    can_afford = Money >= DEFENCE_COST
    active = can_afford and not builder_mode
    print("can_afford", can_afford)
    print("builder_mode", builder_mode)
    print("active", active)
    slot_color = (0, 80, 200) if active else (50, 50, 80)
    border_color = (0, 150, 255) if active else (80, 80, 100)
    pg.draw.rect(Screen, slot_color, (rx, slot_y, rw, 50), 0, 5)
    pg.draw.rect(Screen, border_color, (rx, slot_y, rw, 50), 2, 5)
    b_label = font_big.render("[B]", True, (255, 255, 255))
    cost_label = font_small.render(f"${round(DEFENCE_COST, 1)}", True, (255, 215, 0) if can_afford else (150, 150, 150))
    Screen.blit(b_label, (rx + rw // 2 - b_label.get_width() // 2, slot_y + 6))
    Screen.blit(cost_label, (rx + rw // 2 - cost_label.get_width() // 2, slot_y + 28))

    dy = slot_y + 60
    d_label = font_small.render(f"amount : {len(defences)}", True, (150, 200, 255))
    Screen.blit(d_label, (rx + 4, dy))