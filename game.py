import random
import pygame
from objects import Object

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


def run_game():
    global make_jump
    game = True
    cactus_arr = []
    create_cactus_arr(cactus_arr)
    land = pygame.image.load(r'images/background/Land.jpg')

    stone, cloud = open_random_objects()

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            make_jump = True

        if keys[pygame.K_ESCAPE]:
            pause()

        if make_jump:
            jump()

        count_scores(cactus_arr)

        display.blit(land, (0, 0))
        print_text('Scoreboard:' + str(scores), 550, 10)
        draw_array(cactus_arr)
        move_objects(stone, cloud)

        draw_dino()

        if check_collision(cactus_arr):
            game = False

        pygame.display.update()
        clock.tick(60)
    return game_over()


def jump():
    global user_y, jump_counter, make_jump
    if jump_counter >= -30:
        user_y -= jump_counter / 2.5
        jump_counter -= 1
    else:
        jump_counter = 30
        make_jump = False


def create_cactus_arr(array):
    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 20, height, width, img, 4))

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 300, height, width, img, 4))

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 600, height, width, img, 4))


def find_radius(array):
    maximum = max(array[0].x, array[1].x, array[2].x)

    if maximum < display_width:
        radius = display_width
        if radius - maximum < 50:
            radius += 150
    else:
        radius = maximum

        choice = random.randrange(0, 5)
        if choice == 0:
            radius += random.randrange(10, 15)
        else:
            radius += random.randrange(200, 250)

        return radius


def draw_array(array):
    for cactus in array:
        check = cactus.move()
        if not check:
            radius = find_radius(array)

            choice = random.randrange(0, 3)
            img = cactus_img[choice]
            width = cactus_options[choice * 2]
            height = cactus_options[choice * 2 + 1]

            cactus.return_self(radius, height, width, img)


def open_random_objects():
    choice = random.randrange(0, 2)
    img_of_stone = stone_img[choice]

    choice = random.randrange(0, 2)
    img_of_cloud = cloud_img[choice]

    stone = Object(display_width, display_height - 80, 10, img_of_stone, 4)
    cloud = Object(display_width, 80, 70, img_of_cloud, 2)

    return stone, cloud


def move_objects(stone, cloud):
    check = stone.move()
    if not check:
        choice = random.randrange(0, 2)
        img_of_stone = stone_img[choice]
        stone.return_self(display_width, 500 + random.randrange(10, 80), stone.width, img_of_stone)

    check = cloud.move()
    if not check:
        choice = random.randrange(0, 2)
        img_of_cloud = cloud_img[choice]
        cloud.return_self(display_width, random.randrange(10, 200), stone.width, img_of_cloud)


def draw_dino():
    global img_counter
    if img_counter == 25:
        img_counter = 0

    display.blit(dino_img[img_counter // 5], (user_x, user_y))
    img_counter += 1


def print_text(message, x, y, font_color=(0, 0, 0), font_type='PingPong.ttfф', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))


def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('Paused. Press Enter to continue', 160, 300)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False

        pygame.display.update()
        clock.tick(15)


def check_collision(barriers):
    for barrier in barriers:
        if barrier.y == 449:  # small cactus
            if not make_jump:
                if barrier.x <= user_x + user_width - 30 <= barrier.x + barrier.width:
                    return True
            elif jump_counter >= 0:
                if user_y + user_height - 5 >= barrier.y:
                    if barrier.x <= user_x + user_width - 30 <= barrier.x + barrier.width:
                        return True
            else:
                if user_y + user_height - 10 >= barrier.y:
                    if barrier.x <= user_x <= barrier.x + barrier.width:
                        return True
        else:
            if not make_jump:
                if barrier.x <= user_x + user_width - 5 <= barrier.x + barrier.width:
                    return True
            elif jump_counter == 10:
                if user_y + user_height - 5 >= barrier.y:
                    if barrier.x <= user_x + user_width - 5 <= barrier.x + barrier.width:
                        return True
            elif jump_counter >= -1:
                if user_y + user_height - 5 >= barrier.y:
                    if barrier.x <= user_x + user_width - 30 <= barrier.x + barrier.width:
                        return True
                else:
                    if user_y + user_height - 10 >= barrier.y:
                        if barrier.x <= user_x + 5 <= barrier.x + barrier.width:
                            return True

    return False


def count_scores(barriers):
    global scores, above_cactus

    if not above_cactus:
        for barrier in barriers:
            if barrier.x <= user_x + user_width / 2 <= barrier.x + barrier.width:
                if user_y + user_height - 5 <= barrier.y:
                    above_cactus = True
                    break
    else:
        if jump_counter == -30:
            scores += 1
            above_cactus = False


def game_over():
    global scores, max_scores
    if scores > max_scores:
        max_scores = scores

    stopped = True
    while stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('Game over. Press Enter to try again, Esc to quit', 50, 300)
        print_text('Max scores: ' + str(max_scores), 300, 350)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return True
        if keys[pygame.K_ESCAPE]:
            return False

        pygame.display.update()
        clock.tick(15)


while run_game():
    scores = 0
    make_jump = False
    jump_counter = 30
    user_y = display_height - user_height - 100

if __name__ == '__main__':
    run_game()
