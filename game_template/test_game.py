import pygame
from pygame.locals import *
import sys
import math

clock = pygame.time.Clock()

pygame.init()
# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
LIGHT_GRAY = (150, 150, 150)
MID_GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
LIGHT_BLUE = (176, 224, 230)
RED = (255, 0, 0)
LIGHT_GREEN = (100, 214, 30)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
# window
TITLE = "Game Template"
WINDOW_SIZE = (600, 400)
FPS = 60
TILE_SIZE = 16
pygame.display.set_caption(TITLE)
wn = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((300, 200))
font = pygame.font.SysFont('arial', 18)

player_height = 16
player_width = 14
# clouds
background_objects = [[0.25, [0, 0, 70, 25]], [0.25, [10, -10, 40, 25]], [0.25, [130, 10, 80, 20]], [0.25, [150, -5, 50, 25]]]


# renders the level
def create_level(path):
    """Opens a file and extracts all the data to form a level, returns the game_map"""
    file = open(path, 'r')
    text = file.read()
    game = text.split('\n')
    game_map = []
    for i in range(len(game)):
        game_map.append([])
        for letter in game[i]:
            game_map[i].append(letter)
    file.close()
    return game_map


def collision_test(rect, tiles):
    """returns all of the tiles that the player collides with"""
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles):
    """moves the player according to the collisions."""
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    e_collisions(player_rect, enemies)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] >= 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types


def e_collisions(rect, enemy_list):
    """checks the collisions of the top of enemies and bottom of the player"""
    for enemy in enemy_list:
        if rect.colliderect(enemy[1]) and rect.bottom - 4 < enemy[1].top:
            dropped_objects.append([[enemy[1].x, enemy[1].y], heart_img, [0, 0], 45])
            enemy_list.remove(enemy)


def coin_collision(rect, coin_list, coin_value):
    """checks the collisions with coins and adds to the coin value"""
    for coin in coin_list:
        if rect.colliderect(coin):
            coin_list.remove(coin)
            coin_value += 1
    return coin_value


def reset_objects(new_game_map):
    """resets all the objects in a new level"""
    new_coins = []
    new_enemies = []
    y_val = 0
    for row in new_game_map:
        x_val = 0
        for tile in row:
            if tile == '3':
                new_coins.append(pygame.Rect((x_val * TILE_SIZE), (y_val * TILE_SIZE), TILE_SIZE, TILE_SIZE))
            if tile == '4':
                new_enemies.append([[0, 0], pygame.Rect((x_val * TILE_SIZE), (y_val * TILE_SIZE), TILE_SIZE, TILE_SIZE), 1, True, ['enemy_move', 0]])
            x_val += 1
        y_val += 1
    return new_coins, new_enemies, []


global animation_frames
animation_frames = {}

def load_animations(path, frame_durations):
    """loads the animations with a path and frames per each image."""
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        animation_img = pygame.image.load(img_loc).convert()
        animation_img.set_colorkey(WHITE)
        animation_frames[animation_frame_id] = animation_img.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data


def change_action(action_var, frame, new_action):
    """changes what animation is playing."""
    if action_var != new_action:
        action_var = new_action
        frame = 0
    return action_var, frame

# all the animations are stored inside the animation database.
animation_database = {}
animation_database['idle'] = load_animations('./assets/player_idle', [7, 7, 7, 7, 12])
animation_database['run'] = load_animations('./assets/player_run', [5, 5, 5, 5, 5])
animation_database['enemy_move'] = load_animations('./assets/enemy_movement', [5, 5, 5, 5])
# current player actions
player_action = 'idle'
player_frame = 0
player_flip = False
# the text file that stores the level.
level_index = 0
game_map = create_level(f'./text_data/level_{level_index}.txt')
# all the movement variables
move_left = False
move_right = False
double_jumped = False
# sprites
# platform
platform_img = pygame.image.load('assets/tiles/platform.png')
platform_img.set_colorkey(WHITE)
platform_left_img = pygame.image.load('assets/tiles/platform_left.png')
platform_left_img.set_colorkey(WHITE)
platform_right_img = pygame.image.load('assets/tiles/platform_right.png')
platform_right_img.set_colorkey(WHITE)
# grass_imgs
grass_img = pygame.image.load('assets/tiles/grass_tile.png')
grass_left_img = pygame.image.load('assets/tiles/grass_tile_left.png')
grass_right_img = pygame.image.load('assets/tiles/grass_tile_right.png')
# dirt imgs
dirt_img = pygame.image.load('assets/tiles/dirt_tile.png')
dirt_left_img = pygame.image.load('assets/tiles/dirt_tile_left.png')
dirt_right_img = pygame.image.load('assets/tiles/dirt_tile_right.png')
# coin imgs
coin_img = pygame.image.load('assets/tiles/coin.png')
coin_img.set_colorkey(WHITE)
heart_img = pygame.image.load('assets/tiles/heart.png')
heart_img.set_colorkey(WHITE)
dead_heart_img = pygame.image.load('assets/tiles/heart_hit.png')
dead_heart_img.set_colorkey(WHITE)
# the player and scroll vars
player_rect = pygame.Rect(50, 50, player_width, player_height)
player_y_momentum = 0
air_timer = 0
true_scroll = [0, 0]
# enemies
enemies = []
enemy_speed = 1
# coins
coins = []
coins_collected = 0
# creates objects
coins, enemies, dropped_objects = reset_objects(game_map)
# hearts
INVIS_FRAMES = 30
no_hit_frames = 0
hearts = 3
heart_list = []
for i in range(hearts):
    heart_list.append([heart_img, [display.get_width() - (i * 18 + 20), 7]])
# ui objects
ui_objects = [[coin_img, [5, 7]]]
# main game loop
running = True
while running:
    display.fill(LIGHT_BLUE)
    # gets the true scroll, then coverts the true scroll into an int.
    true_scroll[0] += (player_rect.x - true_scroll[0] - display.get_width() / 2 + player_width / 2)/20
    true_scroll[1] += (player_rect.y - true_scroll[1] - display.get_height() / 2 + player_height / 2)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    # displays the background objects in a specific format.
    for obj in background_objects:
        obj_rect = pygame.Rect(obj[1][0]-scroll[0]*obj[0], obj[1][1]-scroll[1]*obj[0], obj[1][2], obj[1][3])
        pygame.draw.rect(display, WHITE, obj_rect)
    # displays the platforms for the player to go onto.
    tile_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(grass_img, ((x * TILE_SIZE) - scroll[0], (y * TILE_SIZE) - scroll[1]))
            elif tile == '2':
                display.blit(dirt_img, ((x * TILE_SIZE) - scroll[0], (y * TILE_SIZE) - scroll[1]))
            elif tile == '5':
                display.blit(dirt_left_img, ((x * TILE_SIZE) - scroll[0], (y * TILE_SIZE) - scroll[1]))
            elif tile == '6':
                display.blit(dirt_right_img, ((x * TILE_SIZE) - scroll[0], (y * TILE_SIZE) - scroll[1]))
            elif tile == '7':
                display.blit(grass_left_img, ((x * TILE_SIZE) - scroll[0], (y * TILE_SIZE) - scroll[1]))
            elif tile == '8':
                display.blit(grass_right_img, ((x * TILE_SIZE) - scroll[0], (y * TILE_SIZE) - scroll[1]))
            elif tile == 'p':
                display.blit(platform_img, ((x * TILE_SIZE) - scroll[0], (y * TILE_SIZE) - scroll[1]))
            elif tile == 'l':
                display.blit(platform_left_img, ((x * TILE_SIZE) - scroll[0], (y * TILE_SIZE) - scroll[1]))
            elif tile == 'r':
                display.blit(platform_right_img, ((x * TILE_SIZE) - scroll[0], (y * TILE_SIZE) - scroll[1]))
            if tile != '0' and tile != '3' and tile != '4' and tile != 'p' and tile != 'l' and tile != 'r':
                tile_rects.append(pygame.Rect((x * TILE_SIZE), (y * TILE_SIZE), TILE_SIZE, TILE_SIZE))
            if tile == 'p' or tile == 'r' or tile == 'l':
                tile_rects.append(pygame.Rect((x * TILE_SIZE), (y * TILE_SIZE) + TILE_SIZE / 3, TILE_SIZE, TILE_SIZE / 3))
            x += 1
        y += 1

    for coin in coins:
        display.blit(coin_img, (coin.x - scroll[0], coin.y - scroll[1]))

    no_hit_frames += 1
    player_movement = [0, 0]

    for enemy in enemies:
        enemy[0] = [0, 0]
        enemy[0][0] += enemy[2]
        enemy_length = len(enemies)
        
        enemy[4][1] += 1
        if enemy[4][1] >= len(animation_database[enemy[4][0]]):
            enemy[4][1] = 0
        enemy_img_id = animation_database[enemy[4][0]][enemy[4][1]]
        enemy_img_id = animation_frames[enemy_img_id]
        enemy_img_id.set_colorkey(WHITE)

        enemy_rect, enemy_collisions = move(enemy[1], enemy[0], tile_rects)
        if enemy_collisions['bottom']:
            enemy[0][1] = 0
        if enemy_collisions['left'] or enemy_collisions['right']:
            enemy[3] = not enemy[3]
            enemy[2] = -enemy[2]
        if player_rect.colliderect(enemy[1]) and player_rect.bottom  > enemy[1].top and no_hit_frames > INVIS_FRAMES:
            if enemy_length == len(enemies):
                heart_list[hearts - 1] = [dead_heart_img, [heart_list[hearts - 1][1][0], heart_list[hearts - 1][1][1]]]
                hearts -= 1
                no_hit_frames = 0
                if player_rect.x > enemy[1].x:
                    player_movement[0] += 10
                    player_movement[1] -= 10
                else:
                    player_movement[0] -= 10
                    player_movement[1] -= 10

        display.blit(pygame.transform.flip(enemy_img_id, enemy[3], False), (enemy_rect.x - scroll[0], enemy_rect.y - scroll[1]))

    if move_right:
        player_movement[0] += 2
    elif move_left:
        player_movement[0] -= 2
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 4:
        player_y_momentum = 4
        if player_rect.y > 278:
            heart_list[hearts - 1] = [dead_heart_img, [heart_list[hearts - 1][1][0], heart_list[hearts - 1][1][1]]]
            hearts -= 1
            player_rect.x = 0
            player_rect.y = 0
    elif player_movement[0] == 0:
        player_action, player_frame = change_action(player_action, player_frame, 'idle')
    elif player_movement[0] > 0:
        player_action, player_frame = change_action(player_action, player_frame, 'run')
        player_flip = False
    elif player_movement[0] < 0:
        player_action, player_frame = change_action(player_action, player_frame, 'run')
        player_flip = True

    player_rect, collisions = move(player_rect, player_movement, tile_rects)
    coins_collected = coin_collision(player_rect, coins, coins_collected)
    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
        double_jumped = False
    else:
        air_timer += 1
    if collisions['top']:
        player_y_momentum += 0.75

    # pygame.draw.rect(display, BLUE, pygame.Rect(player_rect.x - scroll[0], player_rect.y - scroll[1], TILE_SIZE, TILE_SIZE))
    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_img = animation_frames[player_img_id]
    player_img.set_colorkey(WHITE)
    display.blit(pygame.transform.flip(player_img, player_flip, False), (player_rect.x - scroll[0], player_rect.y - scroll[1]))
    # render ui objects
    for obj in dropped_objects:
        obj[2][1] += 0.2
        drop = pygame.Rect(obj[0][0], obj[0][1], 8, 8)
        drop, drop_collisions = move(drop, obj[2], tile_rects)
        obj[3] -= 1
        if drop_collisions['bottom']:
            obj[2][1] -= 0.5
        if drop.colliderect(player_rect) and obj[3] < 0 and hearts < 3:
            heart_list[hearts] = [heart_img, [heart_list[hearts][1][0], heart_list[hearts][1][1]]]
            hearts += 1
            dropped_objects.remove(obj)
        display.blit(pygame.transform.scale(obj[1], (8, 8)), (drop.x - scroll[0], drop.y - scroll[1]))
    for obj in ui_objects:
        display.blit(obj[0], (obj[1][0], obj[1][1]))
    for heart in heart_list:
        display.blit(heart[0], (heart[1][0], heart[1][1]))
    if hearts <= 0:
        hearts = 3

    display.blit(font.render(f'{coins_collected}', True, BLACK), (21, 5))

    # input events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                move_left = True
            if event.key == K_RIGHT:
                move_right = True
            if event.key == K_UP:
                if air_timer < 6:
                    player_y_momentum = -5
                if not double_jumped and air_timer > 6:
                    player_y_momentum = -4
                    double_jumped = True
            if event.key == K_r:
                level_index += 1
                if level_index >= 2:
                    level_index = 0
                game_map.clear()
                game_map = create_level(f'./text_data/level_{level_index}.txt')
                coins, enemies, dropped_objects = reset_objects(game_map)
                player_rect.x = 0
                player_rect.y = 0
        if event.type == KEYUP:
            if event.key == K_LEFT:
                move_left = False
            if event.key == K_RIGHT:
                move_right = False

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    wn.blit(surf, (0, 0))
    pygame.display.update()
    clock.tick(FPS)
