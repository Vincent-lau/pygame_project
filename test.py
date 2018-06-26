#background_image_filename = 'sushiplate.jpg'
sprite_image_filename = 'fugu.png'

import pygame
from pygame.locals import *
from sys import exit

pygame.init()

screen = pygame.display.set_mode((1000,1000), 0, 32)
clock=pygame.time.Clock()

#background = pygame.image.load(background_image_filename).convert()
sprite = pygame.image.load("/Users/liuliu/myDocuments/Python/pygame_project/generic_platformer_tiles.png").convert()
# sprite的起始x坐标
x = 0.

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    screen.fill((0,0,0))
   # screen.blit(background, (0, 0))
    time_passed=clock.tick()/1000.0
    print(time_passed)
    distance_moved=time_passed*250

    screen.blit(sprite, (x, 100))
    x += distance_moved  # 如果你的机器性能太好以至于看不清，可以把这个数字改小一些

    # 如果移动出屏幕了，就搬到开始位置继续
    if x > 1000.:
        x -= 1000.

    pygame.display.update()