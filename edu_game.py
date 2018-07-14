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

maze=[[0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
   [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],]

tile_group=pg.sprite.Group()
wall_group=pg.sprite.Group()
all_sprites_group=pg.sprite.Group()



# font = pg.font.SysFont('Calibri', 25, True, False)
# Used to manage how fast the screen updates
clock = pg.time.Clock()
screenSize = (700, 500)
screen = pg.display.set_mode(screenSize)
pg.init()
done = False

for i in range(10):
    wall=Tile((0,i*50),(500,3),BLACK)
    wall_group.add(wall)
    all_sprites_group.add(wall)
    all_sprites_group.add(Tile((500,0),(3,500),BLACK))
    all_sprites_group.add(Tile((0, 500), (500, 3), BLACK))
    for j in range(10):
        if(i==0):
            wall = Tile((j*50,0), (3,500), BLACK)
            wall_group.add(wall)
            all_sprites_group.add(wall)

        if(maze[i][j]):


            size=(500/10,500/10)
            tile=Tile((j*50,i*50),size,BLACK)
            tile_group.add(tile)
            all_sprites_group.add(tile)


while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done=True



    screen.fill(WHITE)
    all_sprites_group.draw(screen)


    pg.display.flip()
    clock.tick(60)



