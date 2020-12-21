import pygame as pg
import tasa
import enemy_gunner
import turret
import images as img
import random as rand

# initialize pygame
pg.init()

# create a game display
pg.display.set_icon(img.icon)
display_width = 1280
display_height = 710
game_display = pg.display.set_mode((display_width, display_height))

# 8 bit madness font can be downloaded from here: http://www.dafont.com/8-bit-madness.font
font = "8-Bit-Madness.ttf"


# text rendering function
def message_to_screen(message, textfont, size, color):
    my_font = pg.font.Font(textfont, size)
    my_message = my_font.render(message, 0, color)

    return my_message


# colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (50, 50, 50)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
faded_gray = (145, 145, 145)

# image pixel format converting
for convert_images in img.all_images:
    convert_images.convert_alpha()

# framerate
clock = pg.time.Clock()
FPS = 30

# player variables
player = tasa.Tasa(100, display_height / 2 - 40)
moving = True
godmode = True

# score variables
score = 0
highscore_file = open('highscore.dat', "r")
highscore_int = int(highscore_file.read())

# background variables
background_x = 0
background_y = 0
background_x1 = 0
background_y1 = 0

# enemy_gunner variables
enemy_gunner = enemy_gunner.EnemyGunner(-100, display_height / 2 - 40)
enemy_gunner_alive = False

# turret variables
turret = turret.Turret(-110, 430)
turret_alive = False

# enemy_spaceship variables
enemy_spaceship_x = 1300
enemy_spaceship_y = rand.randint(0, 500)
enemy_spaceship_alive = False
enemy_spaceship_hit_player = False
warning_once = True
warning = False
warning_counter = 0
warning_message = message_to_screen("!", font, 200, red)

# enemy_rocketship variables
enemy_rocketship_x = 1280
enemy_rocketship_y = rand.randint(0, 500)

# bullet variables
bullets = []

# bomb variables
bombs = []


# main menu
def main_menu():

    global background_x
    global background_y
    global background_x1
    global background_y1

    menu = True

    selected = "play"

    while menu:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w or event.key == pg.K_UP:
                    selected = "play"
                elif event.key == pg.K_s or event.key == pg.K_DOWN:
                    selected = "quit"
                if event.key == pg.K_SPACE or event.key == pg.K_RETURN:
                    if selected == "play":
                        menu = False
                    if selected == "quit":
                        pg.quit()
                        quit()

        game_display.blit(img.background, (background_x, background_y))
        game_display.blit(img.background, (background_x1, background_y1))
        if background_x < -display_width:
            background_x = 0
        if background_x1 < 0:
            background_x1 = display_width

        background_x -= 10
        background_x1 -= 10

        if godmode:
            title = message_to_screen("T.A.S.A. 2023 (GODMODE)", font, 80, yellow)
        else:
            title = message_to_screen("T.A.S.A. 2023", font, 100, white)
        controls_1 = message_to_screen("use WASD to move, SPACE to shoot,", font, 30, white)
        controls_2 = message_to_screen("SHIFT to drop bombs, and P to toggle pause", font, 30, white)
        if selected == "play":
            play = message_to_screen("PLAY", font, 75, white)
        else:
            play = message_to_screen("PLAY", font, 75, faded_gray)
        if selected == "quit":
            game_quit = message_to_screen("QUIT", font, 75, white)
        else:
            game_quit = message_to_screen("QUIT", font, 75, faded_gray)

        title_rect = title.get_rect()
        controls_1_rect = controls_1.get_rect()
        controls_2_rect = controls_2.get_rect()
        play_rect = play.get_rect()
        quit_rect = game_quit.get_rect()

        # drawing text
        game_display.blit(title, (display_width/2 - (title_rect[2]/2), 40))
        game_display.blit(controls_1, (display_width/2 - (controls_1_rect[2]/2), 120))
        game_display.blit(controls_2, (display_width/2 - (controls_2_rect[2]/2), 140))
        game_display.blit(play, (display_width/2 - (play_rect[2]/2), 200))
        game_display.blit(game_quit, (display_width/2 - (quit_rect[2]/2), 260))

        pg.display.update()
        pg.display.set_caption("T.A.S.A. 2023 running at " + str(int(clock.get_fps())) + " frames per second.")
        clock.tick(FPS)


def pause():

    global highscore_file
    global highscore_int

    paused = True

    player.moving_up = False
    player.moving_left = False
    player.moving_down = False
    player.moving_right = False

    paused_text = message_to_screen("PAUSED", font, 100, white)
    paused_text_rect = paused_text.get_rect()

    game_display.blit(paused_text, (display_width/2 - (paused_text_rect[2]/2), 40))

    pg.display.update()
    clock.tick(15)

    while paused:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if score > highscore_int:
                    highscore_file = open('highscore.dat', "w")
                    highscore_file.write(str(score))
                    highscore_file.close()
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    paused = False


# create a game loop
def game_loop():

    global enemy_spaceship_x
    global enemy_spaceship_y
    global enemy_spaceship_alive
    global enemy_spaceship_hit_player
    global warning
    global warning_counter
    global warning_once

    global bullets
    global moving

    global highscore_file
    global highscore_int
    global score

    global background_x
    global background_y
    global background_x1
    global background_y1

    global enemy_rocketship_x
    global enemy_rocketship_y

    global enemy_gunner_alive

    global turret_alive

    game_exit = False
    game_over = False

    game_over_selected = "play again"

    while not game_exit:

        while game_over:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    if score > highscore_int:
                        highscore_file = open('highscore.dat', "w")
                        highscore_file.write(str(score))
                        highscore_file.close()
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_w or event.key == pg.K_UP:
                        game_over_selected = "play again"
                    elif event.key == pg.K_s or event.key == pg.K_DOWN:
                        game_over_selected = "quit"
                    if event.key == pg.K_SPACE or event.key == pg.K_RETURN:
                        if game_over_selected == "play again":
                            if score > highscore_int:
                                highscore_file = open('highscore.dat', "w")
                                highscore_file.write(str(score))
                                highscore_file.close()
                            game_over = False

                            score = 0

                            enemy_rocketship_x = 1280

                            enemy_gunner.x = -100
                            enemy_gunner_alive = False
                            enemy_gunner.bullets = []

                            turret.x = -110
                            turret_alive = False
                            turret.bullets = []

                            enemy_spaceship_x = 1300
                            enemy_spaceship_alive = False
                            warning = False
                            warning_counter = 0
                            warning_counter = 0

                            player.wreck_start = False
                            player.y = display_height/2-40
                            player.x = 100
                            player.wrecked = False
                            player.health = 3
                            bullets = []

                            game_loop()
                        if game_over_selected == "quit":
                            pg.quit()
                            quit()

            game_over_text = message_to_screen("GAME OVER", font, 100, white)
            your_score = message_to_screen("YOUR SCORE WAS: " + str(score), font, 50, white)
            if game_over_selected == "play again":
                play_again = message_to_screen("PLAY AGAIN", font, 75, white)
            else:
                play_again = message_to_screen("PLAY AGAIN", font, 75, faded_gray)
            if game_over_selected == "quit":
                game_quit = message_to_screen("QUIT", font, 75, white)
            else:
                game_quit = message_to_screen("QUIT", font, 75, faded_gray)

            game_over_rect = game_over_text.get_rect()
            your_score_rect = your_score.get_rect()
            play_again_rect = play_again.get_rect()
            game_quit_rect = game_quit.get_rect()

            game_display.blit(game_over_text, (display_width/2 - game_over_rect[2]/2, 40))
            game_display.blit(your_score, (display_width/2 - (your_score_rect[2]/2+5), 100))
            game_display.blit(play_again, (display_width/2 - play_again_rect[2]/2, 200))
            game_display.blit(game_quit, (display_width/2 - game_quit_rect[2]/2, 260))

            pg.display.update()
            pg.display.set_caption("T.A.S.A. 2023 running at " + str(int(clock.get_fps())) + " frames per second.")
            clock.tick(10)

        # event handler
        for event in pg.event.get():

            if event.type == pg.QUIT:
                if score > highscore_int:
                    highscore_file = open('highscore.dat', "w")
                    highscore_file.write(str(score))
                    highscore_file.close()
                pg.quit()
                quit()

            if moving:

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_w:
                        player.moving_up = True
                    if event.key == pg.K_a:
                        player.moving_left = True
                    if event.key == pg.K_s:
                        player.moving_down = True
                    if event.key == pg.K_d:
                        player.moving_right = True
                    if event.key == pg.K_SPACE:
                        if not player.wreck_start:
                            bullets.append([player.x, player.y])
                    if event.key == pg.K_LSHIFT:
                        if not player.wreck_start:
                            bombs.append([player.x, player.y])
                    if event.key == pg.K_p:
                        pause()

                if event.type == pg.KEYUP:
                    if event.key == pg.K_w:
                        player.moving_up = False
                    if event.key == pg.K_a:
                        player.moving_left = False
                    if event.key == pg.K_s:
                        player.moving_down = False
                    if event.key == pg.K_d:
                        player.moving_right = False

        if player.health < 1:
            player.wreck()

        if player.wrecked:
            game_over = True

        game_display.blit(img.background, (background_x, background_y))
        game_display.blit(img.background, (background_x1, background_y1))
        if background_x < -display_width:
            background_x = 0
        if background_x1 < 0:
            background_x1 = display_width

        background_x -= 10
        background_x1 -= 10

        # drawing player
        game_display.blit(player.current, (player.x, player.y))

        # drawing enemy_gunner
        game_display.blit(enemy_gunner.current, (enemy_gunner.x, enemy_gunner.y))

        # drawing enemy_spaceship
        game_display.blit(img.enemy_spaceship, (enemy_spaceship_x, enemy_spaceship_y))

        # drawing turret
        game_display.blit(img.turret, (turret.x, turret.y))

        # enabling movement and animations
        player.player_init()
        enemy_gunner.init()
        turret.init()

        # rendering bullets
        if not player.wreck_start and not player.wrecked:

            for draw_bullet in bullets:
                game_display.blit(img.rocket, (draw_bullet[0] + 90, draw_bullet[1] + 40, 20, 5))
            for move_bullet in range(len(bullets)):
                bullets[move_bullet][0] += 40
            for del_bullet in bullets:
                if del_bullet[0] >= 1280:
                    bullets.remove(del_bullet)

        # rendering bombs
        if not player.wreck_start and not player.wrecked:
            for draw_bomb in bombs:
                game_display.blit(img.nuke_bomb, (draw_bomb[0] + 90, draw_bomb[1] + 40, 20, 27))
            for move_bomb in range(len(bombs)):
                bombs[move_bomb][1] += 20
            for del_bomb in bombs:
                if del_bomb[1] > 600:
                    bombs.remove(del_bomb)

        # rendering enemy bullets
        if not player.wreck_start and not player.wrecked and not game_over:
            for draw_bullet in enemy_gunner.bullets:
                game_display.blit(img.enemy_rocket, (draw_bullet[0] + 90, draw_bullet[1] + 40, 20, 7))
            for move_bullet in range(len(enemy_gunner.bullets)):
                enemy_gunner.bullets[move_bullet][0] -= 15
            for del_bullet in enemy_gunner.bullets:
                if del_bullet[0] <= -40:
                    enemy_gunner.bullets.remove(del_bullet)

        # rendering turret bullets
        if not player.wreck_start and not player.wrecked and not game_over:
            for draw_bullet in turret.bullets:
                game_display.blit(img.missile, (draw_bullet[0] + 40, draw_bullet[1] + 30, 20, 20))
            for move_bullet in range(len(turret.bullets)):
                turret.bullets[move_bullet][0] -= 10
                turret.bullets[move_bullet][1] -= 10
            for del_bullet in turret.bullets:
                if del_bullet[1] < -40:
                    turret.bullets.remove(del_bullet)

        # draw randomly positioned enemy_rocketships, pop if they hit any bullet or bombs
        for pop_enemy_rocketship in bullets:
            if enemy_rocketship_x < pop_enemy_rocketship[0]+90 < enemy_rocketship_x+70 and enemy_rocketship_y < pop_enemy_rocketship[1]+40 < enemy_rocketship_y+100:
                bullets.remove(pop_enemy_rocketship)
                enemy_rocketship_x = 1280 - 1450
                score += 50
            elif enemy_rocketship_x < pop_enemy_rocketship[0]+100 < enemy_rocketship_x+70 and enemy_rocketship_y < pop_enemy_rocketship[1]+50 < enemy_rocketship_y+100:
                bullets.remove(pop_enemy_rocketship)
                enemy_rocketship_x = 1280 - 1450
                score += 50

        for pop_enemy_rocketship in bombs:
            if enemy_rocketship_x < pop_enemy_rocketship[0]+55 < enemy_rocketship_x+70 and enemy_rocketship_y < pop_enemy_rocketship[1]+70 < enemy_rocketship_y+100:
                bombs.remove(pop_enemy_rocketship)
                enemy_rocketship_x = 1280 - 1450
                score += 50
            elif enemy_rocketship_x < pop_enemy_rocketship[0]+75 < enemy_rocketship_x+70 and enemy_rocketship_y < pop_enemy_rocketship[1]+90 < enemy_rocketship_y+100:
                bombs.remove(pop_enemy_rocketship)
                enemy_rocketship_x = 1280 - 1450
                score += 50

        # spawn enemy_spaceship randomly
        enemy_spaceship_spawn_num = rand.randint(0, 100)
        if enemy_spaceship_spawn_num == 50 and not enemy_spaceship_alive and score > 450:
            warning = True

        # show warning before enemy_spaceship spawning
        if warning:
            if warning_once:
                warning_once = False
            game_display.blit(warning_message, (1070, enemy_spaceship_y-15))
            if warning_counter > 45:
                enemy_spaceship_alive = True
                warning_counter = 0
                warning = False
                warning_once = True
            else:
                warning_counter += 1

        # enemy_spaceship movement
        if enemy_spaceship_alive:
            enemy_spaceship_x -= 30
        if enemy_spaceship_x < 0-100:
            enemy_spaceship_hit_player = False
            enemy_spaceship_alive = False
            enemy_spaceship_x = 1300
            enemy_spaceship_y = rand.randint(0, 500)

        # spawn enemy gunner randomly
        enemy_spawn_num = rand.randint(0, 100)
        if not enemy_gunner_alive and score > 250 and enemy_spawn_num == 50:
            enemy_gunner_alive = True
            enemy_gunner.x = 1280

        # spawn turret randomly
        turret_spawn_num = rand.randint(0, 200)
        if score > 700 and turret_spawn_num == 100 and not turret_alive:
            turret.x = 1280
            turret_alive = True

        if turret.x <= -110:
            turret_alive = False

        # enemy-player bullet collision detection
        for hit_enemy_gunner in bullets:
            if enemy_gunner.x < hit_enemy_gunner[0] + 90 < enemy_gunner.x + 100 \
               or enemy_gunner.x < hit_enemy_gunner[0] + 100 < enemy_gunner.x + 100:
                if enemy_gunner.y < hit_enemy_gunner[1] + 40 < enemy_gunner.y + 80 \
                   or enemy_gunner.y < hit_enemy_gunner[1] + 50 < enemy_gunner.y + 80:
                    if not enemy_gunner.x > 1200:
                        score += 150
                        bullets.remove(hit_enemy_gunner)
                        enemy_gunner.x = -100
                        enemy_gunner_alive = False

        # enemy_spaceship-player bullet/bomb collision detection
        for hit_enemy_spaceship in bullets:
            if enemy_spaceship_x < hit_enemy_spaceship[0]+90 < enemy_spaceship_x+100 \
               or enemy_spaceship_x < hit_enemy_spaceship[0]+100 < enemy_spaceship_x+100:
                if enemy_spaceship_y < hit_enemy_spaceship[1]+40 < enemy_spaceship_y+80 \
                   or enemy_spaceship_y < hit_enemy_spaceship[1]+50 < enemy_spaceship_y+80:
                    if not enemy_spaceship_x > 1200:
                        bullets.remove(hit_enemy_spaceship)
                        score += 200
                        enemy_spaceship_hit_player = False
                        enemy_spaceship_alive = False
                        enemy_spaceship_x = 1300
                        enemy_spaceship_y = rand.randint(0, 500)

        for hit_enemy_spaceship in bombs:
            if enemy_spaceship_x < hit_enemy_spaceship[0]+55 < enemy_spaceship_x+100 \
               or enemy_spaceship_x < hit_enemy_spaceship[0]+65 < enemy_spaceship_x+100:
                if enemy_spaceship_y < hit_enemy_spaceship[1]+70 < enemy_spaceship_y+80 \
                   or enemy_spaceship_y < hit_enemy_spaceship[1]+80 < enemy_spaceship_y+80:
                    if not enemy_spaceship_x > 1200:
                        bombs.remove(hit_enemy_spaceship)
                        score += 200
                        enemy_spaceship_hit_player = False
                        enemy_spaceship_alive = False
                        enemy_spaceship_x = 1300
                        enemy_spaceship_y = rand.randint(0, 500)

        # turret-player bullet/bomb collision detection
        for hit_turret in bullets:
            if turret.x < hit_turret[0]+90 < turret.x+110 or turret.x < hit_enemy_spaceship[0]+100 < turret.x+110:
                if turret.y < hit_turret[1]+40 < turret.y+70 or turret.y < hit_turret[1]+50 < turret.y+70:
                    if not turret.x > 1200:
                        bullets.remove(hit_turret)
                        score += 200
                        turret_alive = False
                        turret.x = -110

        for hit_turret in bombs:
            if turret.x < hit_turret[0]+55 < turret.x+110 or turret.x < hit_enemy_spaceship[0]+75 < turret.x+110:
                if turret.y < hit_turret[1]+70 < turret.y+70 or turret.y < hit_turret[1]+90 < turret.y+70:
                    if not turret.x > 1200:
                        bombs.remove(hit_turret)
                        score += 200
                        turret_alive = False
                        turret.x = -110

        # player-enemy_rocketship collision detection
        if enemy_rocketship_x < player.x < enemy_rocketship_x + 65 or enemy_rocketship_x < player.x + 140 < enemy_rocketship_x + 65:
            if enemy_rocketship_y < player.y < enemy_rocketship_y + 65 or enemy_rocketship_y < player.y + 71 < enemy_rocketship_y + 65:
                player.damaged = True
                player.health -= 1
                enemy_rocketship_x = 1280 - 1450

        # player-enemy rocket collision detection
        for hit_player in enemy_gunner.bullets:
            if player.x < hit_player[0] < player.x+100 or player.x < hit_player[0]+40 < player.x+100:
                if player.y < hit_player[1]+40 < player.y+80 or player.y < hit_player[1]+50 < player.y+80:
                    player.damaged = True
                    player.health -= 1
                    enemy_gunner.bullets.remove(hit_player)

        # player-turret bullet collision detection
        for hit_player in turret.bullets:
            if player.x < hit_player[0] < player.x+100 or player.x < hit_player[0]+20 < player.x+100:
                if player.y < hit_player[1] < player.y+80 or player.y < hit_player[1]+20 < player.y+80:
                    if not turret.turret_hit_player:
                        player.damaged = True
                        player.health -= 1
                        turret.bullets.remove(hit_player)

        # player-turret collision detection
        if turret.x < player.x < turret.x + 110 or turret.x < player.x + 100 < turret.x + 110:
            if turret.y < player.y < turret.y + 70 or turret.y < player.y + 80 < turret.y + 70:
                if not turret.turret_hit_player:
                    player.damaged = True
                    player.health -= 1
                    turret.turret_hit_player = True

        # player-enemy_spaceship collision detection
        if enemy_spaceship_x < player.x < enemy_spaceship_x + 150 or enemy_spaceship_x < player.x + 140 < enemy_spaceship_x + 150:
            if enemy_spaceship_y < player.y < enemy_spaceship_y + 68 or enemy_spaceship_y < player.y + 71 < enemy_spaceship_y + 71:
                if not enemy_spaceship_hit_player:
                    player.damaged = True
                    player.health -= 1
                    enemy_spaceship_hit_player = True

        game_display.blit(img.enemy_rocketship, (enemy_rocketship_x, enemy_rocketship_y))
        if enemy_rocketship_x <= 1280 - 1330:
            enemy_rocketship_x = 1280
            enemy_rocketship_y = rand.randint(0, 500)
        else:
            if not player.wreck_start:
                enemy_rocketship_x -= 7

        # draw score
        game_display.blit(message_to_screen("SCORE: {0}".format(score), font, 50, white), (10, 10))

        # draw high score
        if score < highscore_int:
            hi_score_message = message_to_screen("HI-SCORE: {0}".format(highscore_int), font, 50, white)
        else:
            highscore_file = open('highscore.dat', "w")
            highscore_file.write(str(score))
            highscore_file.close()
            highscore_file = open('highscore.dat', "r")
            highscore_int = int(highscore_file.read())
            highscore_file.close()
            hi_score_message = message_to_screen("HI-SCORE: {0}".format(highscore_int), font, 50, yellow)

        hi_score_message_rect = hi_score_message.get_rect()

        game_display.blit(hi_score_message, (1280 - hi_score_message_rect[2] - 10, 10))

        # draw health
        if player.health >= 1:
            game_display.blit(img.lives, (10, 50))
            if player.health >= 2:
                game_display.blit(img.lives, (10 + 32 + 10, 50))
                if player.health >= 3:
                    game_display.blit(img.lives, (10 + 32 + 10 + 32 + 10, 50))

        # god-mode (for quicker testing)
        if godmode:
            score = 1000
            player.health = 3333

        pg.display.update()

        pg.display.set_caption("T.A.S.A. 2023 running at " + str(int(clock.get_fps())) + " frames per second.")
        clock.tick(FPS)


main_menu()
game_loop()
pg.quit()
quit()
