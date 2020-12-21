import pygame as pg

tasa_1 = pg.image.load('images/new-TASA-TCG.png')

tasa_2 = pg.image.load('images/new-TASA-TCG.png')

lives = pg.image.load('images/new-TASA-Lives.png')

rocket = pg.image.load('images/rocket.png')

enemy_rocket = pg.image.load('images/rocket-2.png')

nuke_bomb = pg.image.load('images/nuke-bomb.png')

missile = pg.image.load('images/turret-missile.png')

helicopter_crash_1 = pg.image.load('sprites/helicopter_crash_1.png')
helicopter_crash_2 = pg.image.load('sprites/helicopter_crash_2.png')
helicopter_crash_3 = pg.image.load('sprites/helicopter_crash_3.png')
helicopter_crash_4 = pg.image.load('sprites/helicopter_crash_4.png')
tasa_damaged_1 = pg.image.load('images/new-TASA-TCG-Damaged.png')
tasa_damaged_2 = pg.image.load('images/new-TASA-TCG-Damaged-2.png')

enemy_gunner_1 = pg.image.load('images/enemy-gunner.png')
enemy_gunner_2 = pg.image.load('images/enemy-gunner.png')


turret = pg.image.load('images/turret.png')

tasa_list = [tasa_1, tasa_2]
damaged_tasa_list = [tasa_damaged_1, tasa_damaged_2]
enemy_gunner_list = [enemy_gunner_1, enemy_gunner_2]

enemy_rocketship = pg.image.load('images/enemy-rocketship.png')

enemy_spaceship = pg.image.load('images/enemy-spaceship.png')

icon = pg.image.load('images/new-TASA-Icon.png')

background = pg.image.load('images/space-extended.png')


all_images = [tasa_1, tasa_2, tasa_damaged_1, tasa_damaged_2, rocket, nuke_bomb, enemy_gunner_1,
               enemy_gunner_2, enemy_rocket, helicopter_crash_1, helicopter_crash_2, helicopter_crash_3,
               helicopter_crash_4, turret, missile, enemy_rocketship, enemy_spaceship, icon, background]


