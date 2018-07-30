import pygame as pg
import random
from collections import deque


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARKGREY=(169,169,169)
RED = (255, 0, 0)
BLUE=(0,0,255)

class Player(pg.sprite.Sprite):
    def __init__(self,pos,cor,size,color):
        super().__init__()
        self.image=pg.Surface(size)
        self.rect=self.image.get_rect(topleft=pos)
        self.image.fill(color)
        self.time=0
        self.cor=cor    # cor[0] is the row number and cor[1] is the column number


    def tracking_key(self,keys):
        dis=500/nMazeNum
        if keys==pg.K_RIGHT:
            self.move([self.rect.x+dis,self.rect.y])
        elif keys==pg.K_LEFT:
            self.move([self.rect.x-dis,self.rect.y])
        elif keys==pg.K_UP:
            self.move([self.rect.x,self.rect.y-dis])
        elif keys==pg.K_DOWN:
            self.move([self.rect.x,self.rect.y+dis])


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

        flag = (0<=newR<nMazeNum) and (0<=newC<nMazeNum) and (maze[newR][newC]!=1)

        if flag:
            if dirX:
                self.rect.move_ip(dirX , 0)
                self.cor[1]=newC
                self.time+=1
            if dirY:
                self.rect.move_ip(0 , dirY)
                self.cor[0]=newR
                self.time+=1

    def get_cor(self):
        return self.cor
    def get_time(self):
        return self.time

class Tile(pg.sprite.Sprite): # grid lines
    def __init__(self,pos,size,color):
        super().__init__()
        self.image=pg.Surface(size)
        self.rect=self.image.get_rect(topleft=pos)
        self.image.fill(color)


def generate_maze(): # in addition to generate the maze and add it to groups, also returns the myPlayer object
    # 1=wall 2=player 3=princess
    global maze
    nMazeNum=random.randrange(5,20)
    maze=[[0]*nMazeNum for i in range(nMazeNum)]
    princessPos=[0,0]

    nSpecialElement=random.randrange(0,int(nMazeNum*nMazeNum*0.5))  # randrange [a,b), 60% of the maze is wall
    playerCor=random.randrange(0,nMazeNum*nMazeNum)

    maze[playerCor//nMazeNum][playerCor%nMazeNum]=2

    while True:
        princessCor=random.randrange(0,nMazeNum*nMazeNum)
        if princessCor != playerCor:
            break
    maze[princessCor // nMazeNum][princessCor % nMazeNum] = 3
    nSpecialElement-=2
    print("nSpecialElemen=",nSpecialElement,"nMazeNum=",nMazeNum)
    for i in range(nSpecialElement):

        while True:
            wallCor = random.randrange(0,nMazeNum * nMazeNum )
            if wallCor!=princessCor and wallCor != playerCor:
                break

        maze[wallCor // nMazeNum][wallCor % nMazeNum] = 1
    
    print(maze)
    for i in range(nMazeNum+1): # +1 in oder to add grid lines of both ends
        sideLength=500/nMazeNum
        wall = Tile((0, i * sideLength), (500, 3), BLACK) # adding grid lines
        wall_group.add(wall)
        all_sprites_group.add(wall)



        for j in range(nMazeNum+1):
            if (i == 0):
                wall = Tile((j * sideLength, 0), (3, 500), BLACK)
                wall_group.add(wall)
                all_sprites_group.add(wall)

            if i == nMazeNum or j == nMazeNum:  # if it is the fringe of the maze, then go on
                continue

            if (maze[i][j] == 1):

                tile = Tile([j * sideLength, i * sideLength], [sideLength+0.8,sideLength+0.8], BLACK)
                # adding 0.8 is not a very good way but makes the maze look better
                tile_group.add(tile)
                all_sprites_group.add(tile)

            elif maze[i][j]==2:
                size = [sideLength * 0.4, sideLength * 0.4] # the size of the player will make up two fifths of a tile
                myPlayer = Player((j * sideLength + sideLength * 0.3, i * sideLength + sideLength * 0.3),[i,j], size, BLUE) # player is centred

            elif maze[i][j] == 3:
                size = [sideLength*0.4,sideLength*0.4]
                princess = Tile((j * sideLength + sideLength*0.3, i * sideLength + sideLength*0.3), size, RED)
                all_sprites_group.add(princess)
                princessPos = [i, j]

    return myPlayer,nMazeNum,princessPos


def Bfs(startPpos, endPos):
    global maze, nMazeNum
    q=deque() # every element in q is a list of three integers s[0]: row num, s[1]:column number, s[2]: number of steps
    visited=[[0]*nMazeNum for i in range(nMazeNum)]
    dir=[[0,1,0,-1],[1,0,-1,0]]
    q.append([startPpos[0],startPpos[1],0])
    while q:
        s=q.popleft()
        print("element in queue",s)
        if [s[0],s[1]]==endPos:
            return s[2]
        for i in range(4):
            newR=s[0]+dir[0][i]
            newC=s[1]+dir[1][i]
            if newR<0 or newR>=nMazeNum or newC<0 or newC>=nMazeNum or maze[newR][newC]==1 or visited[newR][newC]:
                continue
            q.append([newR,newC,s[2]+1])
            visited[newR][newC]=1
    return -1

def display_information():
    font = pg.font.SysFont('Calibri', 25, True, False)
    #game instruction
    gameInstruction = []
    gameInstruction.append(font.render("Game Instruction:", True, RED))
    gameInstruction.append(font.render("Move the player to", True, BLACK))
    gameInstruction.append(font.render("meet the princess", True, BLACK))
    gameInstruction.append(font.render("in minimum number", True, BLACK))
    gameInstruction.append(font.render("of moves", True, BLACK))
    for i in range(len(gameInstruction)):
        screen.blit(gameInstruction[i],[500+10,i*30])

    #game information
    if myPlayer.get_cor()==endPos and myPlayer.get_time()==solution:
        screen.blit(font.render("You Win!", True, RED), [500 + 10, 200 + 10])
        screen.blit(font.render("Congrtulations",True,RED),[500+10,200+10+30])
    elif myPlayer.get_cor()==endPos:
        screen.blit(font.render("Well done!", True, RED), [500 + 10, 200 + 10])
        screen.blit(font.render("Try to do it with", True, RED), [500 + 10, 200 + 10 + 30])
        screen.blit(font.render("fewer moves", True, RED), [500 + 10, 200 + 10 + 30*2])


    screen.blit(font.render("steps taken: "+str(myPlayer.get_time()),True,BLACK),[500+10,300+10])
    screen.blit(font.render("steps required: " + str(solution), True, BLACK), [500 + 10, 300 + 10+30])




tile_group=pg.sprite.Group()
wall_group=pg.sprite.Group()
all_sprites_group=pg.sprite.Group()

maze=[]
myPlayer,nMazeNum,endPos=generate_maze()

solution=Bfs(myPlayer.get_cor(),endPos)
print("steps required:",solution)
all_sprites_group.add(myPlayer)

pg.init()
clock = pg.time.Clock()
screenSize = (700, 500)
screen = pg.display.set_mode(screenSize)

done = False



while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done=True
        elif event.type == pg.KEYDOWN:
            myPlayer.tracking_key(event.key)





    screen.fill(WHITE)
    all_sprites_group.draw(screen)
    display_information()   # this line must be after the group draw code


    pg.display.flip()
    clock.tick(60)



