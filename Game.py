import os
import pygame

WIDTH = 800  # width of our game window
HEIGHT = 800 # height of our game window
FPS = 30 # frames per second

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

SCORE = 0
BONUS_SCORE = 0
ALI_X = 50
ALI_Y = 40

pygame.init()
pygame.mixer.init()  # for sound
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

# game_folder = os.path.dirname('/home/xeno/ciuchcio/')
# img_folder = os.path.join(game_folder, 'img')
# player_img = pygame.image.load(os.path.join(img_folder, 'player.png')).convert()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 30

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


class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


player = Player()

alien11 = Aliens(20, 50)
alien12 = Aliens(40, 50)
alien13 = Aliens(60, 50)
alien14 = Aliens(80, 50)
alien15 = Aliens(100, 50)
alien16 = Aliens(120, 50)
alien17 = Aliens(140, 50)
alien18 = Aliens(160, 50)
alien19 = Aliens(180, 50)
alien110 = Aliens(200, 50)
alien111 = Aliens(220, 50)

aliens5 = [alien11, alien12, alien13, alien14, alien15, alien16, alien17, alien18, alien19, alien110, alien111]

aliens_all = [aliens5]

all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
aliens_row5_group = pygame.sprite.Group()

player_group.add(player)
aliens_row5_group.add(aliens_all)
tmp = []

running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    if ALI_X >= WIDTH-400:
        ALI_Y += 20
    if ALI_Y % 2 == 0:
        ALI_X += 2


    # Update
    player_group.update()

    for i in range(len(aliens_all)):
        for j in range(len(aliens_all[i])):
            aliens_all[i][j].rect.x = (40 * j)+ALI_X
            aliens_all[i][j].rect.y = ALI_Y

    # Draw / render
    screen.fill(BLACK)
    # *after* drawing everything, flip the display
    aliens_row5_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()

pygame.quit()

