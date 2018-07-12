import pygame as pg

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARKGREY=(169,169,169)
RED = (255, 0, 0)
BLUE=(0,0,255)


class Tile(pg.sprite.Sprite):
    def __init__(self,pos,size,color):
        super().__init__()
        self.image=pg.Surface(size)
        self.rect=self.image.get_rect(topleft=pos)
        self.image.fill(color)

maze=[[0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
   [0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
   [0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
   [0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
   [0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
   [0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
   [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
   [0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
   [0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
   [0, 0, 1, 0, 0, 0, 0, 0, 1, 0],]

wall_group=pg.sprite.Group()
all_sprites_group=pg.sprite.Group()

for i in range(10):
    for j in range(10):
        if(maze[i][j]):
            x=i*50
            y=j*50
            size=(500/10,500/10)
            tile=Tile((x,y),size,BLUE)
            wall_group.add(tile)
            all_sprites_group.add(tile)


# font = pg.font.SysFont('Calibri', 25, True, False)
# Used to manage how fast the screen updates
clock = pg.time.Clock()
screenSize = (700, 500)
screen = pg.display.set_mode(screenSize)
pg.init()
done = False
while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done=True

    screen.fill(WHITE)
    all_sprites_group.draw(screen)


    pg.display.flip()
    clock.tick(60)



