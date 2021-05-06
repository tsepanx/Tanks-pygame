# -*- coding: utf-8 -*-
import pygame

pygame.init()

tank_filenames = dict()
tank_filenames['up'] = 'data/tank_up.png'
tank_filenames['down'] = 'data/tank_down.png'
tank_filenames['right'] = 'data/tank_right.png'
tank_filenames['left'] = 'data/tank_left.png'

map_filenames = [
    'maps/map1.txt',
    'maps/map2.txt',
]

dict_keys_player1 = dict()
dict_keys_player2 = dict()

dict_keys_player1[pygame.K_UP] = 'up'
dict_keys_player1[pygame.K_DOWN] = 'down'
dict_keys_player1[pygame.K_RIGHT] = 'right'
dict_keys_player1[pygame.K_LEFT] = 'left'
dict_keys_player1[pygame.K_BACKSPACE] = 'shot'

dict_keys_player2[pygame.K_w] = 'up'
dict_keys_player2[pygame.K_s] = 'down'
dict_keys_player2[pygame.K_d] = 'right'
dict_keys_player2[pygame.K_a] = 'left'
dict_keys_player2[pygame.K_SPACE] = 'shot'

consts = dict()
consts['BLOCK_SIZE'] = 30
consts['SCREEN_SIZE'] = [1200, 660]
consts['CAPTION'] = 'Tanks'
speed_rend = 50

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
AQUA = (0, 255, 255)
YELLOW = (255, 255, 0)
size_font = 25
font = pygame.font.Font(None, size_font)

speed_tank = 5
speed_bull = 20


def draw_zone(size, screen):
    pygame.draw.line(screen, AQUA, [10, 10], [size[0] - 10, 10], 5)
    pygame.draw.line(screen, AQUA, [size[0] - 10, 10], [size[0] - 10, size[1] - 10], 5)
    pygame.draw.line(screen, AQUA, [size[0] - 10, size[1] - 10], [10, size[1] - 10], 5)
    pygame.draw.line(screen, AQUA, [10, size[1] - 10], [10, 10], 5)


def collide_obj(obj, obj2):
        if pygame.sprite.collide_rect(obj2, obj):
            if obj2.direction == 'right':
                obj2.rect.right = obj.rect.left
                obj.rect.left = obj2.rect.right
            elif obj2.direction == 'left':
                obj2.rect.left = obj.rect.right
                obj.rect.right = obj2.rect.left
            elif obj2.direction == 'up':
                obj2.rect.top = obj.rect.bottom
                obj.rect.bottom = obj2.rect.top
            else:
                obj2.rect.bottom = obj.rect.top
                obj.rect.top = obj2.rect.bottom

# TODO сделать класс мин и еще использовать speed_red
log_error = lambda x: f"Couldn't open {x}"

class Tank(pygame.sprite.Sprite):
    bullets = 2000
    __speed = 0
    direction = 'up'
    life = 100
    kill_flag = False
    images = dict()
    quanity_bulls = 1

    def __init__(self, pos, filenames):
        pygame.sprite.Sprite.__init__(self)
        for key in filenames:
            self.images[key] = pygame.image.load(filenames[key]).convert()
            self.images[key].set_colorkey(WHITE)
        try:
            self.image = self.images['up']
        except pygame.error:
            print(log_error(filename))
            exit()
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.image.set_colorkey(WHITE)

    def get_speed(self):
        return self.__speed

    def draw_text(self, screen, color):
        text = font.render(str(self.life), True, color)
        screen.blit(text, [self.rect.x + 10, self.rect.y - 15])
        text = font.render(str(self.bullets), True, color)
        screen.blit(text, [self.rect.x, self.rect.y + 30])

    def update(self):
        if self.direction == 'up':
            self.rect.move_ip(0, -self.__speed)
        if self.direction == 'down':
            self.rect.move_ip(0, self.__speed)
        if self.direction == 'right':
            self.rect.move_ip(self.__speed, 0)
        if self.direction == 'left':
            self.rect.move_ip(-self.__speed, 0)
        self.image = self.images[self.direction]

    def collide(self, group_objects):
        for obj in group_objects:
            if pygame.sprite.collide_rect(self, obj):
                if self.direction == 'right':
                    self.rect.right = obj.rect.left
                elif self.direction == 'left':
                    self.rect.left = obj.rect.right
                elif self.direction == 'up':
                    self.rect.top = obj.rect.bottom
                else:
                    self.rect.bottom = obj.rect.top
                return True

    def apply_command(self, command):
        if command in ('up', 'down', 'right', 'left'):
            self.direction = command
            self.__speed = speed_tank
        if command == 'shot' and self.bullets > 0:
            if self.quanity_bulls == 1:
                self.bullets -= 1
                bullet_start_pos = (0, 0)
                if self.direction == 'right':
                    bullet_start_pos = self.rect.midright
                if self.direction == 'left':
                    bullet_start_pos = self.rect.midleft
                if self.direction == 'up':
                    bullet_start_pos = self.rect.midtop
                if self.direction == 'down':
                    bullet_start_pos = self.rect.midbottom
                return [Bullet(bullet_start_pos, self.direction, 'data/bull.png')]
            else:
                self.bullets -= 2
                bullet_start_pos = (0, 0)
                if self.direction == 'right':
                    bullet_start_pos = [self.rect.midright[0], self.rect.midright[1] - 10]
                    bullet_start_pos_2 = [self.rect.midright[0], self.rect.midright[1] + 10]
                if self.direction == 'left':
                    bullet_start_pos = [self.rect.midleft[0], self.rect.midleft[1] - 10]
                    bullet_start_pos_2 = [self.rect.midleft[0], self.rect.midleft[1] + 10]
                if self.direction == 'up':
                    bullet_start_pos = [self.rect.midtop[0] - 10, self.rect.midtop[1]]
                    bullet_start_pos_2 = [self.rect.midtop[0] + 10, self.rect.midtop[1]]
                if self.direction == 'down':
                    bullet_start_pos = [self.rect.midbottom[0] - 10, self.rect.midbottom[1]]
                    bullet_start_pos_2 = [self.rect.midbottom[0] + 10, self.rect.midbottom[1]]
                return [Bullet(bullet_start_pos, self.direction, 'data/bull.png'),
                        Bullet(bullet_start_pos_2, self.direction, 'data/bull.png')]
        if command == 'stop':
            self.__speed = 0
        if command == 'move_back':
            self.__speed = -speed_tank
            self.update()
            self.__speed = 0

    def apply_hit(self, bullet):
        self.life -= bullet.damage
        if self.life <= 0:
            self.kill_flag = True

    def apply_heart(self, heart):
        self.life += heart.life_count
        self.bullets += heart.bullets_count


class Bullet(pygame.sprite.Sprite):
    __speed = speed_bull
    damage = 10

    def __init__(self, pos, direction, filename):
        pygame.sprite.Sprite.__init__(self)
        try:
            self.image = pygame.image.load(filename).convert()
        except pygame.error:
            print(log_error(filename))
            exit()
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.image.set_colorkey(WHITE)
        self.direction = direction

    def update(self):
        if self.direction == 'up':
            self.rect.move_ip(0, -self.__speed)
        if self.direction == 'down':
            self.rect.move_ip(0, self.__speed)
        if self.direction == 'right':
            self.rect.move_ip(self.__speed, 0)
        if self.direction == 'left':
            self.rect.move_ip(-self.__speed, 0)


class Heart(pygame.sprite.Sprite):
    life_count = 5
    bullets_count = 5

    def __init__(self, pos, filename):
        pygame.sprite.Sprite.__init__(self)
        try:
            self.image = pygame.image.load(filename).convert()
        except pygame.error:
            print(log_error(filename))
            exit()
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.image.set_colorkey(BLACK)


class Block(pygame.sprite.Sprite):
    def __init__(self, pos, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert()
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.image.set_colorkey(WHITE)


class DestroyableBlock(Block):
    def __init__(self, pos, filename, life_count):
        Block.__init__(self, pos, filename)
        self.__life_count = life_count
        self.kill_flag = False

    def apply_hit(self, bullet):
        self.__life_count -= bullet.damage
        if self.__life_count <= 0:
            self.kill_flag = True


class Button(pygame.sprite.Sprite):
    def __init__(self, pos, filename, text):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert()
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.text = text

    def draw_rect(self, screen, between):
        # 1 2
        # 3 4

        # 1 to 2
        pygame.draw.line(screen, RED, [self.rect.x - between, self.rect.y - between],
                         [self.rect.x + self.rect.width + between, self.rect.y - between])
        # 2 to 4
        pygame.draw.line(screen, RED, [self.rect.x + self.rect.width + between, self.rect.y - 5],
                         [self.rect.x + self.rect.width + between, self.rect.y + between + self.rect.height])
        # 4 to 3
        pygame.draw.line(screen, RED, [self.rect.x + self.rect.width + between, self.rect.y + between + self.rect.height],
                         [self.rect.x - between, self.rect.y + between + self.rect.height])
        # 1 to 3
        pygame.draw.line(screen, RED, [self.rect.x - between, self.rect.y + between + self.rect.height],
                         [self.rect.x - between, self.rect.y - between])

    def collide(self, mouse_pos):
        if self.rect.x < mouse_pos[0] < self.rect.x + self.rect.width:
            if self.rect.y < mouse_pos[1] < self.rect.y + self.rect.height:
                return True
        return False


class Menu(pygame.sprite.Sprite):
    def __init__(self, list_of_buttons):
        pygame.sprite.Sprite.__init__(self)
        self.buttons = list_of_buttons

    def start(self, list_buttons, screen):
        group_buttons = pygame.sprite.Group()
        screen.fill((255, 0, 0))
        for b in list_buttons:
            text = b[0:b.find(' ')]
            pos = eval(b[b.find(' '):])
            group_buttons.add(Button(pos, 'button.png', text))
        group_buttons.draw(screen)
