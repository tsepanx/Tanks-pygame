# -*- coding: utf-8 -*-

# не забывай делать комиты и выполнять TODO

import random
from utils import *
import time

file_map = open(map_filenames[1], 'r')
blocks_arr = file_map.readlines()

def parse_map(map_arr):
    group_dict = dict()
    group_dict['HEARTS'] = pygame.sprite.Group()
    group_dict['PLAYER1'] = pygame.sprite.Group()
    group_dict['PLAYER2'] = pygame.sprite.Group()
    group_dict['BULLETS1'] = pygame.sprite.Group()
    group_dict['BULLETS2'] = pygame.sprite.Group()
    group_dict['BLOCKS'] = pygame.sprite.Group()

    x_block = 0
    y_block = 0
    for row in range(len(map_arr)):
        for char in map_arr[row]:
            if char == ' ':
                if random.randint(0, 10) == 0:
                    group_dict['HEARTS'].add(Heart((x_block + 15, y_block + 15), 'data/heart_black.png'))
            if char == '-':
                group_dict['BLOCKS'].add(DestroyableBlock((x_block, y_block), 'data/punch_brick.png', 1))
                if random.randint(0, 10) == 0:
                    group_dict['HEARTS'].add(Heart((x_block + 15, y_block + 15), 'data/heart_black.png'))
            elif char == '=':
                group_dict['BLOCKS'].add(Block((x_block, y_block), 'data/brick.png'))
            elif char == '1':
                player1.rect.x = x_block
                player1.rect.y = y_block
            elif char == '2':
                player2.rect.x = x_block
                player2.rect.y = y_block
            x_block += consts['BLOCK_SIZE']
        x_block = 0
        y_block += consts['BLOCK_SIZE']
    return group_dict

pygame.init()
pygame.display.set_caption(consts['CAPTION'])
screen = pygame.display.set_mode(consts['SCREEN_SIZE'])

player1 = Tank((2000, 2000), tank_filenames)
player2 = Tank((2000, 2000), tank_filenames)

group_dict = parse_map(blocks_arr)

group_dict['PLAYER1'].add(player1)
group_dict['PLAYER2'].add(player2)

done = False
clock = pygame.time.Clock()

pygame.mixer.init()
audio = pygame.mixer.Sound('undertale.ogg')
audio.play(-1)

while not done:
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            break
        elif event.type == pygame.KEYDOWN:
            key = event.key
            if key in dict_keys_player1:
                command = dict_keys_player1[key]
                if command == 'shot':
                       group_dict['BULLETS1'].add(player1.apply_command(command))
                else:
                    player1.apply_command(command)
            if key in dict_keys_player2:
                command = dict_keys_player2[key]
                if command == 'shot':
                    group_dict['BULLETS2'].add(player2.apply_command(command))
                else:
                    player2.apply_command(command)
            if key == pygame.K_v:
                if player2.quanity_bulls == 1:
                    player2.quanity_bulls = 2
                else:
                    player2.quanity_bulls = 1

            if key == pygame.K_DELETE:
                if player1.quanity_bulls == 1:
                    player1.quanity_bulls = 2
                else:
                    player1.quanity_bulls = 1
            if key == pygame.K_F1:
                if speed_rend != 5:
                    speed_rend -= 5
            if key == pygame.K_F2:
                if speed_rend != 65:
                    speed_rend += 5

        elif event.type == pygame.KEYUP:
            key = event.key
            if key in (pygame.K_RIGHT, pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT):
                if dict_keys_player1[key] == player1.direction:
                    player1.apply_command('stop')
            if key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d):
                if dict_keys_player2[key] == player2.direction:
                    player2.apply_command('stop')

    collide_dict = pygame.sprite.groupcollide(group_dict['PLAYER1'], group_dict['BULLETS2'], False, True)
    for player in collide_dict:
        for bullet in collide_dict[player]:
            player.apply_hit(bullet)
    collide_dict = pygame.sprite.groupcollide(group_dict['PLAYER2'], group_dict['BULLETS1'], False, True)
    for player in collide_dict:
        for bullet in collide_dict[player]:
            player.apply_hit(bullet)

    pygame.sprite.groupcollide(group_dict['BULLETS1'], group_dict['BULLETS2'], True, True)

    collide_dict = pygame.sprite.groupcollide(group_dict['BLOCKS'], group_dict['BULLETS1'], False, True)
    for block in collide_dict:
        for bullet in collide_dict[block]:
            if isinstance(block, DestroyableBlock):
                block.apply_hit(bullet)
                if block.kill_flag:
                    group_dict['BLOCKS'].remove(block)
    collide_dict = pygame.sprite.groupcollide(group_dict['BLOCKS'], group_dict['BULLETS2'], False, True)
    for block in collide_dict:
        for bullet in collide_dict[block]:
            if isinstance(block, DestroyableBlock):
                block.apply_hit(bullet)
                if block.kill_flag:
                    group_dict['BLOCKS'].remove(block)

    collide_dict = pygame.sprite.groupcollide(group_dict['PLAYER1'], group_dict['HEARTS'], False, True)
    for player in collide_dict:
        for heart in collide_dict[player]:
            player.apply_heart(heart)
    collide_dict = pygame.sprite.groupcollide(group_dict['PLAYER2'], group_dict['HEARTS'], False, True)
    for player in collide_dict:
        for heart in collide_dict[player]:
            player.apply_heart(heart)

    # --- Update ------------

    for key in group_dict:
        group_dict[key].update()
    # is
    #collide_obj(player1, player2)
    player2.collide(group_dict['BLOCKS'])
    player1.collide(group_dict['BLOCKS'])


    # --- Drawing Code
    screen.fill(BLACK)

    if player1.kill_flag and player2.kill_flag:
        group_dict['BULLETS1'].empty()
        group_dict['BULLETS2'].empty()
        size_font = 750
        text = font.render('TIE', True, RED)
        screen.blit(text, [100, 100])
        pygame.display.flip()
        time.sleep(1)
        pygame.quit()

    elif player2.kill_flag:
        group_dict['BULLETS1'].empty()
        group_dict['BULLETS2'].empty()
        size_font = 150
        text = font.render('PLAYER RIGHT WINS', True, RED)
        screen.blit(text, [70, 250])
        pygame.display.flip()
        time.sleep(1)
        pygame.quit()

    elif player1.kill_flag:
        size_font = 150
        text = font.render('PLAYER LEFT WINS', True, GREEN)
        screen.blit(text, [90, 250])
        pygame.display.flip()
        time.sleep(1)
        pygame.quit()
    else:
        for key in group_dict:
            group_dict[key].draw(screen)
        player1.draw_text(screen, RED)
        player2.draw_text(screen, BLUE)

    draw_zone(consts['SCREEN_SIZE'], screen)
    pygame.display.flip()
    clock.tick(speed_rend)

pygame.quit()
