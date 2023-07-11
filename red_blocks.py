import sys
import pygame
import time
import random

# Блоки
block_size = 50
margin = 5
block_amount_x = 10
block_amount_y = 10
fading_interval = 5
fading_bottom_border = 50

# Экран
screen_size = (block_size * block_amount_x + margin * (block_amount_x + 1),
                block_size * block_amount_y + margin * (block_amount_y + 1))
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Что-то несуразное')
clock = pygame.time.Clock()
FPS = 15

# Класс блока
class Block:
    def __init__(self, position, fading_speed, starting_btightness):
        self.position = position
        self.fading_speed = fading_speed
        self.color = [starting_btightness, 50, 50]
        self.last_fade = time.time_ns()

    # Угасание (отнимает от яркости блока определенное значение раз в определенный промежуток времени)
    def fade(self):
        tm = time.time_ns()
        if tm - self.last_fade > self.fading_speed:
            self.color[0] -= fading_interval
            if self.color[0] < 0: self.color[0] = 0
            self.last_fade = tm

    # Подсвечивание (выводит яркость на максимум)
    def light(self):
        if self.color[0] < fading_bottom_border:
            self.color[0] = 255

    # Подсвечивание по наведению мыши
    def light_point(self, mouse):
        if (mouse[0] > self.position[0] and mouse[0] < self.position[0] + block_size and
            mouse[1] > self.position[1] and mouse[1] < self.position[1] + block_size):
            self.color[0] = 255

    # Простая отрисовка
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.position[0], self.position[1], block_size, block_size))


# Инициализация блоков
block_list = []
for x in range(block_amount_x):
    for y in range(block_amount_y):
        block = Block((margin * (x + 1) + block_size * x, (margin * (y + 1) + block_size * y)), random.randint(10, 100000000), random.randint(0, 256))
        block_list.append(block)

mode = 'automode'
while True:
    screen.fill((0, 0, 0))
    clock.tick(FPS)

    # Обработка блоков (отрисовка, погашение, отрисовка)
    for block in block_list:
        if mode == 'automode': block.light()
        elif mode == 'pointmode': block.light_point(pygame.mouse.get_pos())
        block.fade()
        block.draw()

    pygame.display.flip()

    # Обработка событий
    for event in pygame.event.get():
        # Выход по нажатию ESC или по закрытию окна
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # Смена режима по нажатию 'm' (русская 'ь')
            if event.key == pygame.K_m:
                if mode == 'automode': mode = 'pointmode'
                elif mode == 'pointmode': mode = 'automode'
