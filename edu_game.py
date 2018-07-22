import pygame as pg

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARKGREY=(169,169,169)
RED = (255, 0, 0)
BLUE=(0,0,255)

class Player(pg.sprite.Sprite):
    def __init__(self,pos,size,color):
        super().__init__()
        self.image=pg.Surface(size)
        self.rect=self.image.get_rect(topleft=pos)
        self.image.fill(color)
        self.time=0
        self.cor=[0,0]      # cor[0] is the row number and cor[1] is the column number


    def tracking_key(self,keys):
        if keys==pg.K_RIGHT:
            self.move([self.rect.x+50,self.rect.y])
        elif keys==pg.K_LEFT:
            self.move([self.rect.x-50,self.rect.y])
        elif keys==pg.K_UP:
            self.move([self.rect.x,self.rect.y-50])
        elif keys==pg.K_DOWN:
            self.move([self.rect.x,self.rect.y+50])

    def move(self,endPos):
        endX=endPos[0]
        endY=endPos[1]
        dirX = endX - self.rect.x
        dirY = endY - self.rect.y
        newR = self.cor[0]
        newC = self.cor[1]


        if dirX > 0:
            newC=self.cor[1] + 1
        elif dirX < 0:
            newC=self.cor[1] - 1

        if dirY > 0:
            newR=self.cor[0] + 1
        elif dirY<0:
            newR=self.cor[0] - 1

        flag = (0<=newR<10) and (0<=newC<10) and (maze[newR][newC]!=1)


        if flag:
            if dirX:
                self.rect.move_ip(dirX , 0)
                self.cor[1]=newC
            if dirY:
                self.rect.move_ip(0 , dirY)
                self.cor[0]=newR


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
   [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
   [0, 0, 0, 0, 0, 0, 0, 0, 2, 0],]

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

        if(maze[i][j]==1):


            size=(500/10,500/10)
            tile=Tile((j*50,i*50),size,BLACK)
            tile_group.add(tile)
            all_sprites_group.add(tile)

        elif maze[i][j]==2:
            size = (20,20)
            princess = Tile((j * 50+15, i * 50+15), size, RED)

            all_sprites_group.add(princess)


myPlayer=Player([15,15],[20,20],BLUE)
all_sprites_group.add(myPlayer)

while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done=True
        elif event.type == pg.KEYDOWN:
            myPlayer.tracking_key(event.key)

    # print(myPlayer.cor,maze[myPlayer.cor[0]][myPlayer.cor[1]])

    screen.fill(WHITE)
    all_sprites_group.draw(screen)


    pg.display.flip()
    clock.tick(60)



