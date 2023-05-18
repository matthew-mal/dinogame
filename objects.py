import random
import pygame

display_width = 800
display_height = 600

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Dino run')

cactus_img = [pygame.image.load('images/cactus/Cactus0.png'), pygame.image.load('images/cactus/Cactus1.png'),
              pygame.image.load('images/cactus/Cactus2.png')]
cactus_options = [69, 449, 37, 410, 40, 420]

stone_img = [pygame.image.load('images/background/Stone0.png'), pygame.image.load('images/background/Stone1.png')]
cloud_img = [pygame.image.load('images/background/Cloud0.png'), pygame.image.load('images/background/Cloud1.png')]

dino_img = [pygame.image.load('images/dino/Dino0.png'), pygame.image.load('images/dino/Dino1.png'),
            pygame.image.load('images/dino/Dino2.png'),
            pygame.image.load('images/dino/Dino3.png'), pygame.image.load('images/dino/Dino4.png')]
img_counter = 0

# user data
user_width = 60
user_height = 100
user_x = display_width // 3
user_y = display_height - user_height - 100

# cactus data
cactus_weight = 20
cactus_height = 70
cactus_x = display_width - 50
cactus_y = display_height - cactus_height - 100

clock = pygame.time.Clock()

make_jump = False
jump_counter = 30

scores = 0
above_cactus = False
max_scores = 0


class Object:

    def __init__(self, x, y, width, image, speed):
        self.x = x
        self.y = y
        self.width = width
        self.image = image
        self.speed = speed

    def move(self):
        if self.x >= -self.width:
            display.blit(self.image, (self.x, self.y))

            self.x -= self.speed
            return True
        else:
            self.x = display_width + 100 + random.randrange(-80, 60)
            return False

    def return_self(self, radius, y, width, image):
        self.x = radius
        self.y = y
        self.width = width
        self.image = image
        display.blit(self.image, (self.x, self.y))
