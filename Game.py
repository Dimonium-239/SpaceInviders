import math
import os
import time

import pygame
import random

import pyganim

WIDTH = 600
HEIGHT = 600
FPS = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

SCORE = 0
BONUS_SCORE = 0
ALI_X = 20
ALI_Y = 80
SECRET_ALI_X = 3
SECRET_ALI_y = 3
SHOOTING_COUNTER = 4
TIMER_SECRET_ALI = 12
TIME_OF_ALL = 1000
MOVE = 0
FONT = "monospace"
MENU_RUN = True
RUNNING = True
LIVES = 2

start_time = time.time()

pygame.init()
pygame.mixer.init()  # for sound

screen = pygame.display.set_mode((WIDTH, HEIGHT))
menu_screen = pygame.display.set_mode((WIDTH, HEIGHT))
pause_screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, TIME_OF_ALL)
random.seed()

img_directory = os.path.join(os.path.dirname(__file__), 'img')
player_img = pygame.image.load(os.path.join(img_directory, 'Laser_Cannon.png')).convert()
secret_alien_img = pygame.image.load(os.path.join(img_directory, 'Secret_Alien.png')).convert()
alien31_img = pygame.image.load(os.path.join(img_directory, 'Alien3.1.png')).convert()
alien32_img = pygame.image.load(os.path.join(img_directory, 'Alien3.2.png')).convert()
alien21_img = pygame.image.load(os.path.join(img_directory, 'Alien2.1.png')).convert()
alien22_img = pygame.image.load(os.path.join(img_directory, 'Alien2.2.png')).convert()
alien11_img = pygame.image.load(os.path.join(img_directory, 'Alien1.1.png')).convert()
alien12_img = pygame.image.load(os.path.join(img_directory, 'Alien1.2.png')).convert()

aliens_img = [[alien32_img, alien31_img], [alien22_img, alien21_img], [alien12_img, alien11_img]]


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speedy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((2, 8))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = speedy

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 54:
            self.kill()
        if self.rect.top > HEIGHT - 54:
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (60, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 70

    def update(self):
        speed_x = 5
        key_stat = pygame.key.get_pressed()
        if key_stat[pygame.K_LEFT]:
            self.rect.x -= speed_x
        if key_stat[pygame.K_RIGHT]:
            self.rect.x += speed_x
        if self.rect.right > WIDTH - 30:
            self.rect.right = WIDTH - 30
        if self.rect.left < 30:
            self.rect.left = 30

    def shoot(self):
        if SCORE < 250:
            bullet = Bullet(self.rect.centerx, self.rect.top, -6)
            bullets.add(bullet)
        elif SCORE >= 250:
            bullet1 = Bullet(self.rect.centerx-15, self.rect.top+25, -6)
            bullet2 = Bullet(self.rect.centerx+15, self.rect.top+25, -6)
            bullets.add(bullet2)
            bullets.add(bullet1)


class Aliens(pygame.sprite.Sprite):
    def __init__(self, mov_img=MOVE, sprite_img=0):
        pygame.sprite.Sprite.__init__(self)
        self.mov_img = mov_img
        self.sprite_img = sprite_img
        self.image = pygame.transform.scale(aliens_img[self.sprite_img][self.mov_img], (30, 25))
        self.image.set_colorkey(BLACK)
        # self.boltAnimMove = pyganim.PygAnimation(aliens_img[sprite_img])
        # self.boltAnimMove.play()
        # self.boltAnimMove.blit(self.image, (0, 0))  # П
        self.rect = self.image.get_rect()

    def shoot(self):
        bullet = Bullet(self.rect.centerx + 10, self.rect.top, 6)
        aliens_bullet_group.add(bullet)

    def update(self):
        if MOVE == 1:
            self.image = pygame.transform.scale(aliens_img[self.sprite_img][0], (30, 25))
            # self.image.fill(BLACK)
            # self.boltAnimMove.blit(self.image, (0, 0))
        if MOVE == 0:
            self.image = pygame.transform.scale(aliens_img[self.sprite_img][1], (30, 25))


class SecretAlien(pygame.sprite.Sprite):
    def __init__(self, x=-40, y=-40):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(secret_alien_img, (80, 60))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Brick(pygame.sprite.Sprite):
    def __init__(self, x=-20, y=-20):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


def frame(surf):
    pygame.draw.line(surf, YELLOW, [20, HEIGHT - 50], [WIDTH - 20, HEIGHT - 50], 1)
    pygame.draw.line(surf, YELLOW, [20, 50], [20, HEIGHT - 50], 1)
    pygame.draw.line(surf, YELLOW, [20, 50], [WIDTH - 20, 50], 1)
    pygame.draw.line(surf, YELLOW, [WIDTH - 20, 50], [WIDTH - 20, HEIGHT - 50], 1)


def button(surf, color, x, text):
    pygame.draw.rect(menu_screen, color, (WIDTH/2-75, x, 150, 45), 3)
    myfont = pygame.font.SysFont(FONT, 20)
    label = myfont.render(text, 1, color)
    surf.blit(label, (WIDTH/2-75+10, x+10))


player = Player()

alien11 = Aliens(0, 0)
alien12 = Aliens(0, 0)
alien13 = Aliens(0, 0)
alien14 = Aliens(0, 0)
alien15 = Aliens(0, 0)
alien16 = Aliens(0, 0)
alien17 = Aliens(0, 0)
alien18 = Aliens(0, 0)
alien19 = Aliens(0, 0)
alien110 = Aliens(0, 0)

aliens5 = [alien11, alien12, alien13, alien14, alien15, alien16, alien17, alien18, alien19, alien110]

alien21 = Aliens(0, 1)
alien22 = Aliens(0, 1)
alien23 = Aliens(0, 1)
alien24 = Aliens(0, 1)
alien25 = Aliens(0, 1)
alien26 = Aliens(0, 1)
alien27 = Aliens(0, 1)
alien28 = Aliens(0, 1)
alien29 = Aliens(0, 1)
alien210 = Aliens(0, 1)

aliens4 = [alien21, alien22, alien23, alien24, alien25, alien26, alien27, alien28, alien29, alien210]

alien31 = Aliens(0, 1)
alien32 = Aliens(0, 1)
alien33 = Aliens(0, 1)
alien34 = Aliens(0, 1)
alien35 = Aliens(0, 1)
alien36 = Aliens(0, 1)
alien37 = Aliens(0, 1)
alien38 = Aliens(0, 1)
alien39 = Aliens(0, 1)
alien310 = Aliens(0, 1)

aliens3 = [alien31, alien32, alien33, alien34, alien35, alien36, alien37, alien38, alien39, alien310]

alien21 = Aliens(0, 2)
alien22 = Aliens(0, 2)
alien23 = Aliens(0, 2)
alien24 = Aliens(0, 2)
alien25 = Aliens(0, 2)
alien26 = Aliens(0, 2)
alien27 = Aliens(0, 2)
alien28 = Aliens(0, 2)
alien29 = Aliens(0, 2)
alien210 = Aliens(0, 2)

aliens2 = [alien21, alien22, alien23, alien24, alien25, alien26, alien27, alien28, alien29, alien210]

alien11 = Aliens(0, 2)
alien12 = Aliens(0, 2)
alien13 = Aliens(0, 2)
alien14 = Aliens(0, 2)
alien15 = Aliens(0, 2)
alien16 = Aliens(0, 2)
alien17 = Aliens(0, 2)
alien18 = Aliens(0, 2)
alien19 = Aliens(0, 2)
alien110 = Aliens(0, 2)

aliens1 = [alien11, alien12, alien13, alien14, alien15, alien16, alien17, alien18, alien19, alien110]

aliens_all = [aliens5, aliens4, aliens3, aliens2, aliens1]

MENU_COUNTER = 0
while MENU_RUN:
    menu_screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            MENU_RUN = False
            RUNNING = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                MENU_RUN = False
                RUNNING = False
            if event.key == pygame.K_DOWN:
                MENU_COUNTER += 1
                if MENU_COUNTER > 2:
                    MENU_COUNTER = 0
            if event.key == pygame.K_UP:
                MENU_COUNTER -= 1
                if MENU_COUNTER < 0:
                    MENU_COUNTER = 2
            if event.key == pygame.K_RETURN:
                if MENU_COUNTER == 0:
                    MENU_RUN = False
                elif MENU_COUNTER == 1:
                    pass
                elif MENU_COUNTER == 2:
                    MENU_RUN = False
                    RUNNING = False

    if MENU_COUNTER == 0:
        button(menu_screen, YELLOW, 340, "Start")
        button(menu_screen, GREEN, 400, "High score")
        button(menu_screen, GREEN, 460, "Exit")
    elif MENU_COUNTER == 1:
        button(menu_screen, GREEN, 340, "Start")
        button(menu_screen, YELLOW, 400, "High score")
        button(menu_screen, GREEN, 460, "Exit")
    elif MENU_COUNTER == 2:
        button(menu_screen, GREEN, 340, "Start")
        button(menu_screen, GREEN, 400, "High score")
        button(menu_screen, YELLOW, 460, "Exit")

    frame(menu_screen)
    pygame.display.flip()

bullets = pygame.sprite.Group()
player_group = pygame.sprite.Group()
all_aliens_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
aliens_bullet_group = pygame.sprite.Group()
secret_alien_group = pygame.sprite.Group()
aliens5_group = pygame.sprite.Group()
aliens4_group = pygame.sprite.Group()
aliens3_group = pygame.sprite.Group()
aliens2_group = pygame.sprite.Group()
aliens1_group = pygame.sprite.Group()

player_group.add(player)
all_aliens_group.add(aliens_all)
secret_alien = SecretAlien()
aliens5_group.add(aliens_all[0])
aliens4_group.add(aliens_all[1])
aliens3_group.add(aliens_all[2])
aliens2_group.add(aliens_all[3])
aliens1_group.add(aliens_all[4])


secret_alien_group.add(secret_alien)


def draw_the_wall(x_cor):
    for y in range(6, 1, -1):
        for x in range(12, 1, -1):
            brick = Brick()
            if (y < 3 and x < 3) or (y < 3 and x > 11):
                pass
            else:
                brick.rect.x = x * 10 + x_cor
                brick.rect.y = y * 10 + 390
                wall_group.add(brick)


draw_the_wall(50)
draw_the_wall(225)
draw_the_wall(400)

while RUNNING:
    clock.tick(FPS)
    PAUSE_RUN = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                MENU_COUNTER = 0
                while PAUSE_RUN:
                    menu_screen.fill(BLACK)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            PAUSE_RUN = False
                            RUNNING = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                PAUSE_RUN = False
                                RUNNING = True
                            if event.key == pygame.K_DOWN:
                                MENU_COUNTER += 1
                                if MENU_COUNTER > 1:
                                    MENU_COUNTER = 0
                            if event.key == pygame.K_UP:
                                MENU_COUNTER -= 1
                                if MENU_COUNTER < 0:
                                    MENU_COUNTER = 1
                            if event.key == pygame.K_RETURN:
                                if MENU_COUNTER == 0:
                                    PAUSE_RUN = False
                                elif MENU_COUNTER == 1:
                                    PAUSE_RUN = False
                                    RUNNING = False

                    if MENU_COUNTER == 0:
                        button(pause_screen, YELLOW, 400, "Return")
                        button(pause_screen, GREEN, 460, "Exit")
                    elif MENU_COUNTER == 1:
                        button(pause_screen, GREEN, 400, "Return")
                        button(pause_screen, YELLOW, 460, "Exit")

                    frame(pause_screen)
                    pygame.display.flip()
        elif event.type == pygame.USEREVENT:
            if SHOOTING_COUNTER == 0:
                rand_row = random.randrange(len(aliens_all))
                rand_ali = random.randrange(len(aliens1))
                if aliens_all[rand_row][rand_ali] in all_aliens_group:
                    aliens_all[rand_row][rand_ali].shoot()
                    SHOOTING_COUNTER = 4
            SHOOTING_COUNTER -= 1
            if int(ALI_X / 10) % 2 == 1:
                MOVE = 1
            elif int(ALI_X / 10) % 2 == 0:
                MOVE = 0

            for i in range(len(aliens_all)):
                for j in range(len(aliens_all[i])):
                    aliens_all[i][j].update()

            if (ALI_Y / 20) % 2 == 0:
                ALI_X += 10
            if ALI_X >= WIDTH - 500:
                ALI_Y += 20
            if (ALI_Y / 20) % 2 == 1:
                ALI_X -= 10
            if ALI_X <= -40:
                ALI_Y += 20
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                player.shoot()

    if ALI_Y >= 120 and (time.time() - start_time >= TIMER_SECRET_ALI):
        SECRET_ALI_X += 2
        secret_alien.rect.x = SECRET_ALI_X
        secret_alien.rect.y = 20 * math.sin((SECRET_ALI_X - 100) / 8) + 60

        secret_alien_group.update()
        if secret_alien.rect.x >= WIDTH:
            secret_alien.rect.x = -40
            TIMER_SECRET_ALI = random.randrange(5, 15)
            SECRET_ALI_X = 20
            start_time = time.time() + 10

    player_group.update()
    bullets.update()
    aliens_bullet_group.update()
    for i in range(len(aliens_all)):
        for j in range(len(aliens_all[i])):
            aliens_all[i][j].rect.x = 75 + ((40 * j) + ALI_X)
            aliens_all[i][j].rect.y = (40 * i) + ALI_Y

    hits = pygame.sprite.groupcollide(aliens5_group, bullets, True, True)
    for hit in hits:
        SCORE += 40
        BONUS_SCORE += 40
        a = Aliens()
        a.kill()

    hits = pygame.sprite.groupcollide(aliens4_group, bullets, True, True)
    for hit in hits:
        SCORE += 20
        BONUS_SCORE += 20
        a = Aliens()
        a.kill()

    hits = pygame.sprite.groupcollide(aliens3_group, bullets, True, True)
    for hit in hits:
        SCORE += 20
        BONUS_SCORE += 20
        a = Aliens()
        a.kill()

    hits = pygame.sprite.groupcollide(aliens2_group, bullets, True, True)
    for hit in hits:
        SCORE += 10
        BONUS_SCORE += 10
        a = Aliens()
        a.kill()

    hits = pygame.sprite.groupcollide(aliens1_group, bullets, True, True)
    for hit in hits:
        SCORE += 10
        BONUS_SCORE += 10
        a = Aliens()
        a.kill()

    hits = pygame.sprite.groupcollide(bullets, wall_group, True, True)
    for hit in hits:
        w = Brick()
        w.kill()

    hits = pygame.sprite.groupcollide(all_aliens_group, wall_group, False, True)
    for hit in hits:
        w = Brick()
        w.kill()

    hits = pygame.sprite.groupcollide(aliens_bullet_group, wall_group, True, True)
    for hit in hits:
        w = Brick()
        w.kill()

    hits = pygame.sprite.groupcollide(secret_alien_group, bullets, False, True)
    for hit in hits:
        SCORE += random.randrange(100, 600, 100)
        secret_alien.rect.x = -60
        TIMER_SECRET_ALI = random.randrange(5, 15)
        SECRET_ALI_X = 20
        start_time = time.time() + 10

    hits = pygame.sprite.groupcollide(player_group, aliens_bullet_group, False, True)
    for hit in hits:
        LIVES -= 1

    if 0 >= BONUS_SCORE >= 200:
        TIME_OF_ALL = 1000
    elif 200 > BONUS_SCORE >= 300:
        TIME_OF_ALL = 800
    elif 300 > BONUS_SCORE >= 400:
        TIME_OF_ALL = 600
    elif 500 > BONUS_SCORE >= 600:
        TIME_OF_ALL = 400
    elif BONUS_SCORE > 600:
        TIME_OF_ALL = 200

    if LIVES == 2:
        pass
        if LIVES == 1:
            pass
            if LIVES == 0:
                pass

    screen.fill(BLACK)
    secret_alien_group.draw(screen)
    pygame.draw.rect(screen, BLACK, (0, 0, 20, WIDTH))
    pygame.draw.rect(screen, BLACK, (WIDTH - 19, 0, 20, WIDTH))

    myfont = pygame.font.SysFont(FONT, 20)
    label = myfont.render("Score: " + str(SCORE), 1, GREEN)
    screen.blit(label, (WIDTH - 150, 20))

    bullets.draw(screen)
    frame(screen)
    wall_group.draw(screen)
    aliens_bullet_group.draw(screen)
    all_aliens_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()

pygame.quit()
