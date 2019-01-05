import os
import pygame

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

pygame.init()
pygame.mixer.init()  # for sound
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 1000)

# game_folder = os.path.dirname('/home/xeno/ciuchcio/')
# img_folder = os.path.join(game_folder, 'img')
# player_img = pygame.image.load(os.path.join(img_folder, 'player.png')).convert()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((1, 4))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 70

    def update(self):
        speed_x = 5
        key_stat = pygame.key.get_pressed()
        if key_stat[pygame.K_LEFT]:
            self.rect.x -= speed_x
        if key_stat[pygame.K_RIGHT]:
            self.rect.x += speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        bullets.add(bullet)


class Aliens(pygame.sprite.Sprite):
    def __init__(self, x=-20, y=-20):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill(GREEN)
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


player = Player()

alien11 = Aliens()
alien12 = Aliens()
alien13 = Aliens()
alien14 = Aliens()
alien15 = Aliens()
alien16 = Aliens()
alien17 = Aliens()
alien18 = Aliens()
alien19 = Aliens()
alien110 = Aliens()

aliens5 = [alien11, alien12, alien13, alien14, alien15, alien16, alien17, alien18, alien19, alien110]

alien21 = Aliens()
alien22 = Aliens()
alien23 = Aliens()
alien24 = Aliens()
alien25 = Aliens()
alien26 = Aliens()
alien27 = Aliens()
alien28 = Aliens()
alien29 = Aliens()
alien210 = Aliens()

aliens4 = [alien21, alien22, alien23, alien24, alien25, alien26, alien27, alien28, alien29, alien210]

alien31 = Aliens()
alien32 = Aliens()
alien33 = Aliens()
alien34 = Aliens()
alien35 = Aliens()
alien36 = Aliens()
alien37 = Aliens()
alien38 = Aliens()
alien39 = Aliens()
alien310 = Aliens()

aliens3 = [alien31, alien32, alien33, alien34, alien35, alien36, alien37, alien38, alien39, alien310]

alien21 = Aliens()
alien22 = Aliens()
alien23 = Aliens()
alien24 = Aliens()
alien25 = Aliens()
alien26 = Aliens()
alien27 = Aliens()
alien28 = Aliens()
alien29 = Aliens()
alien210 = Aliens()

aliens2 = [alien21, alien22, alien23, alien24, alien25, alien26, alien27, alien28, alien29, alien210]

alien11 = Aliens()
alien12 = Aliens()
alien13 = Aliens()
alien14 = Aliens()
alien15 = Aliens()
alien16 = Aliens()
alien17 = Aliens()
alien18 = Aliens()
alien19 = Aliens()
alien110 = Aliens()

aliens1 = [alien11, alien12, alien13, alien14, alien15, alien16, alien17, alien18, alien19, alien110]

aliens_all = [aliens5, aliens4, aliens3, aliens2, aliens1]

bullets = pygame.sprite.Group()
player_group = pygame.sprite.Group()
all_aliens_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()

player_group.add(player)
all_aliens_group.add(aliens_all)


def draw_the_wall(x_cor):
    for y in range(6, 1, -1):
        for x in range(12, 1, -1):
            brick = Brick()
            if (y < 3 and x < 3) or (y < 3 and x > 11):
                pass
            else:
                brick.rect.x = x*10 + x_cor
                brick.rect.y = y*10 + 390
                wall_group.add(brick)


draw_the_wall(50)
draw_the_wall(225)
draw_the_wall(400)


running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT:
            # Aliens mowing
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

    # Update
    player_group.update()
    bullets.update()
    for i in range(len(aliens_all)):
        for j in range(len(aliens_all[i])):
            aliens_all[i][j].rect.x = 75+((40 * j)+ALI_X)
            aliens_all[i][j].rect.y = (40 * i)+ALI_Y

    # Collisions
    hits = pygame.sprite.groupcollide(all_aliens_group, bullets, True, True)
    for hit in hits:
        a = Aliens()
        all_aliens_group.add(a)

    hits = pygame.sprite.groupcollide(bullets, wall_group, True, True)
    for hit in hits:
        w = Brick()
        wall_group.add(w)

    hits = pygame.sprite.groupcollide(all_aliens_group, wall_group, False, True)
    for hit in hits:
        w = Brick()
        wall_group.add(w)

    # Draw / render
    screen.fill(BLACK)
    # *after* drawing everything, flip the display

    pygame.draw.line(screen, YELLOW, [20, HEIGHT-50], [WIDTH-20, HEIGHT-50], 1)
    pygame.draw.line(screen, YELLOW, [20, 50], [20, HEIGHT-50], 1)
    pygame.draw.line(screen, YELLOW, [20, 50], [WIDTH-20, 50], 1)
    pygame.draw.line(screen, YELLOW, [WIDTH-20, 50], [WIDTH-20, HEIGHT-50], 1)

    bullets.draw(screen)
    wall_group.draw(screen)
    all_aliens_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()

pygame.quit()

