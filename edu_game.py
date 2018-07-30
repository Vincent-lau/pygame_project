import pygame as pg
import random
from collections import deque


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARKGREY=(169,169,169)
RED = (255, 0, 0)
BLUE=(0,0,255)


tile_group=pg.sprite.Group()
wall_group=pg.sprite.Group()
all_sprites_group=pg.sprite.Group()
pg.init()
clock = pg.time.Clock()
screenSize = (700, 500)
screen = pg.display.set_mode(screenSize)

class Player(pg.sprite.Sprite):
    def __init__(self,pos,cor,size,color):
        super().__init__()
        self.image=pg.Surface(size)
        self.rect=self.image.get_rect(topleft=pos)
        self.image.fill(color)
        self.time=0
        self.cor=cor    # cor[0] is the row number and cor[1] is the column number


    def tracking_key(self,keys):

        dis=500/self.nMazeNum
        if keys==pg.K_RIGHT:
            self.move([self.rect.x+dis,self.rect.y])
        elif keys==pg.K_LEFT:
            self.move([self.rect.x-dis,self.rect.y])
        elif keys==pg.K_UP:
            self.move([self.rect.x,self.rect.y-dis])
        elif keys==pg.K_DOWN:
            self.move([self.rect.x,self.rect.y+dis])


    def move(self,endPos):
        pass

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


class Level(object):
    font = pg.font.SysFont('Calibri', 25, True, False)

    def __init__(self): 
        self.solution=-1

    def initialise(self):
        pass
    
    def get_solution(self): # find the optimum solution of a problem
        pass
    
    def display_information(self):  # display necessary information of the game, such as life, time steps
        pass
    
    def restart(self):  # start the game again
        pass

    def retry(self):    # reset the game while keeping the map the same
        pass


class Level1(Level):
    
    
    def __init__(self):
        super().__init__()
        self.maze=[]
        self.princessPos=[0,0]
        self.nMazeNum = 0
        
    def initialise(self):
        # 1=wall 2=player 3=princess

        self.nMazeNum = random.randrange(5, 20)
        self.maze = [[0] * self.nMazeNum for i in range(self.nMazeNum)]
        
        nSpecialElement = random.randrange(0,
                                           int(self.nMazeNum * self.nMazeNum * 0.5))  # randrange [a,b), 60% of the self.maze is wall
        playerCor = random.randrange(0, self.nMazeNum * self.nMazeNum)

        self.maze[playerCor // self.nMazeNum][playerCor % self.nMazeNum] = 2

        while True:
            princessCor = random.randrange(0, self.nMazeNum * self.nMazeNum)
            if princessCor != playerCor:
                break
        self.maze[princessCor // self.nMazeNum][princessCor % self.nMazeNum] = 3
        nSpecialElement -= 2
        print("nSpecialElemen=", nSpecialElement, "self.nMazeNum=", self.nMazeNum)
        for i in range(nSpecialElement):

            while True:
                wallCor = random.randrange(0, self.nMazeNum * self.nMazeNum)
                if wallCor != princessCor and wallCor != playerCor:
                    break

            self.maze[wallCor // self.nMazeNum][wallCor % self.nMazeNum] = 1

        print(self.maze)
        for i in range(self.nMazeNum + 1):  # +1 in oder to add grid lines of both ends
            sideLength = 500 / self.nMazeNum
            wall = Tile((0, i * sideLength), (500, 3), BLACK)  # adding grid lines
            wall_group.add(wall)
            all_sprites_group.add(wall)

            for j in range(self.nMazeNum + 1):
                if (i == 0):
                    wall = Tile((j * sideLength, 0), (3, 500), BLACK)
                    wall_group.add(wall)
                    all_sprites_group.add(wall)

                if i == self.nMazeNum or j == self.nMazeNum:  # if it is the fringe of the self.maze, then go on
                    continue

                if self.maze[i][j] == 1:

                    tile = Tile([j * sideLength, i * sideLength], [sideLength + 0.8, sideLength + 0.8], BLACK)
                    # adding 0.8 is not a very good way but makes the self.maze look better
                    tile_group.add(tile)
                    all_sprites_group.add(tile)

                elif self.maze[i][j] == 2:
                    size = [sideLength * 0.4,
                            sideLength * 0.4]  # the size of the player will make up two fifths of a tile
                    self.myPlayer = Player((j * sideLength + sideLength * 0.3, i * sideLength + sideLength * 0.3), [i, j],
                                      size, BLUE)  # player is centred
                    all_sprites_group.add(self.myPlayer)

                elif self.maze[i][j] == 3:
                    size = [sideLength * 0.4, sideLength * 0.4]
                    princess = Tile((j * sideLength + sideLength * 0.3, i * sideLength + sideLength * 0.3), size, RED)
                    all_sprites_group.add(princess)
                    self.princessPos = [i, j]

    def get_solution(self):

        q = deque()  # every element in q is a list of three integers s[0]: row num, s[1]:column number, s[2]: number of steps
        visited = [[0] * self.nMazeNum for i in range(self.nMazeNum)]
        dir = [[0, 1, 0, -1], [1, 0, -1, 0]]
        startPos=self.myPlayer.get_cor()
        endPos=self.princessPos
        q.append([startPos[0], startPos[1], 0])
        while q:
            s = q.popleft()

            if [s[0], s[1]] == endPos:
                self.solution=s[2]
            for i in range(4):
                newR = s[0] + dir[0][i]
                newC = s[1] + dir[1][i]
                if newR < 0 or newR >= self.nMazeNum or newC < 0 or newC >= self.nMazeNum or self.maze[newR][
                    newC] == 1 or visited[newR][newC]:
                    continue
                q.append([newR, newC, s[2] + 1])
                visited[newR][newC] = 1
        self.solution=-1


    def display_information(self):
        # game instruction
        gameInstruction = []
        gameInstruction.append(self.font.render("Game Instruction:", True, RED))
        gameInstruction.append(self.font.render("Move the player to", True, BLACK))
        gameInstruction.append(self.font.render("meet the princess", True, BLACK))
        gameInstruction.append(self.font.render("in minimum number", True, BLACK))
        gameInstruction.append(self.font.render("of moves", True, BLACK))
        for i in range(len(gameInstruction)):
            screen.blit(gameInstruction[i],[500+10,i*30])

        # game information
        if self.myPlayer.get_cor()==self.princessPos and self.myPlayer.get_time()==self.solution:
            screen.blit(self.font.render("You Win!", True, RED), [500 + 10, 200 + 10])
            screen.blit(self.font.render("Congrtulations",True,RED),[500+10,200+10+30])
        elif self.myPlayer.get_cor()==self.princessPos:
            screen.blit(self.font.render("Well done!", True, RED), [500 + 10, 200 + 10])
            screen.blit(self.font.render("Try to do it with", True, RED), [500 + 10, 200 + 10 + 30])
            screen.blit(self.font.render("fewer moves", True, RED), [500 + 10, 200 + 10 + 30*2])

        screen.blit(self.font.render("steps taken: "+str(self.myPlayer.get_time()),True,BLACK),[500+10,300+10])
        screen.blit(self.font.render("steps required: " + str(self.solution), True, BLACK), [500 + 10, 300 + 10+30])


class Player1(Player):  # class Player1 is a friend of class Level1

    def __init__(self, pos, cor, size, color,l1):
        Player().__init__(pos, cor, size, color)
        self.l1=l1

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

        flag = (0<=newR<l1.nMazeNum) and (0<=newC<l1.nMazeNum) and (l1.maze[newR][newC]!=1)

        if flag:
            if dirX:
                self.rect.move_ip(dirX , 0)
                self.cor[1]=newC
                self.time+=1
            if dirY:
                self.rect.move_ip(0 , dirY)
                self.cor[0]=newR
                self.time+=1



done = False

l1=Level1()
l1.initialise()
l1.get_solution()

while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done=True
        elif event.type == pg.KEYDOWN:
            l1.myPlayer.tracking_key(event.key)





    screen.fill(WHITE)
    all_sprites_group.draw(screen)
    l1.display_information()   # this line must be after the group draw code


    pg.display.flip()
    clock.tick(60)



