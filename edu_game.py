import pygame as pg
import random
import copy
from collections import deque


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARKGREY=(169,169,169)
GREY=(96,96,96)
RED = (255, 0, 0)
BLUE=(0,0,255)

tile_group=pg.sprite.Group()
wall_group=pg.sprite.Group()
all_sprites_group=pg.sprite.Group()
pg.init()
font = pg.font.SysFont('Calibri', 25, True, False)
clock = pg.time.Clock()
screenSize = (700, 500)
screen = pg.display.set_mode(screenSize)


class Player(pg.sprite.Sprite):
    def __init__(self,pos,cor,size,color):
        super().__init__()
        self.image=pg.Surface(size)
        self.oriPos=pos
        self.rect=self.image.get_rect(topleft=pos)
        self.image.fill(color)
        self.oriCor=copy.deepcopy(cor) # any oriCor must use deepcopy
        self.cor=cor    # cor[0] is the row number and cor[1] is the column number

    def tracking_key(self,keys):
        pass

    def move(self,endPos):
        pass

    def get_cor(self):
        return self.cor

    def reset(self):
        pass

class Tile(pg.sprite.Sprite): # grid lines
    def __init__(self,pos,size,color):
        super().__init__()
        self.image=pg.Surface(size)
        self.rect=self.image.get_rect(topleft=pos)
        self.image.fill(color)


class Button(object):
    def __init__(self,pos,size,color,word):
        self.image=pg.Surface(size)
        self.rect=self.image.get_rect(topleft=pos)
        self.image.fill(color)
        self.word=word
        self.size=size

    def isOver(self):
        mousePos=pg.mouse.get_pos()
        return self.rect.x<mousePos[0]<self.rect.x+self.size[0] and self.rect.y<mousePos[1]<self.rect.y+self.size[1]

    def isPressed(self):
        return self.isOver() and pg.mouse.get_pressed()[0] # mouse needs to be over a certain button

    def display(self):  # display word and the button on the screen
        screen.blit(self.image,self.rect)
        screen.blit(font.render(self.word,True,WHITE),[self.rect.x+5,self.rect.y+10])

    def switch(self,color): # switch the color of the button
        self.image.fill(color)

    def update(self):
        if self.isOver():
            self.switch(DARKGREY)
        else:
            self.switch(GREY)
        self.display()


class Level(object):
    def __init__(self): 
        self.solution=-1
        self.retryButton=Button([500+10,400+10],[70,40],GREY,"retry")
        self.restartButton=Button([600+10,400+10],[70,40],GREY,"restart")

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

    def update(self):
        pass


class Level1(Level):
    maze=[]
    princessPos = [0, 0]
    nMazeNum = 0
    
    def __init__(self):
        super().__init__()
        self.myPlayer=Player1([0,0],[0,0],[0,0],BLACK)
        
    def initialise(self):
        # 1=wall 2=player 3=princess

        Level1.nMazeNum = random.randrange(5, 30)
        Level1.maze = [[0] * Level1.nMazeNum for i in range(Level1.nMazeNum)]
        
        nSpecialElement = random.randrange(0,
                                           int(Level1.nMazeNum * Level1.nMazeNum * 0.5))  # randrange [a,b), 60% of the Level1.maze is wall
        playerCor = random.randrange(0, Level1.nMazeNum * Level1.nMazeNum)

        Level1.maze[playerCor // Level1.nMazeNum][playerCor % Level1.nMazeNum] = 2

        while True:
            princessCor = random.randrange(0, Level1.nMazeNum * Level1.nMazeNum)
            if princessCor != playerCor:
                break
        Level1.maze[princessCor // Level1.nMazeNum][princessCor % Level1.nMazeNum] = 3
        nSpecialElement -= 2
        print("nSpecialElemen=", nSpecialElement, "Level1.nMazeNum=", Level1.nMazeNum)
        for i in range(nSpecialElement):

            while True:
                wallCor = random.randrange(0, Level1.nMazeNum * Level1.nMazeNum)
                if wallCor != princessCor and wallCor != playerCor:
                    break

            Level1.maze[wallCor // Level1.nMazeNum][wallCor % Level1.nMazeNum] = 1

        print(Level1.maze)
        for i in range(Level1.nMazeNum + 1):  # +1 in oder to add grid lines of both ends
            sideLength = 500 / Level1.nMazeNum
            wall = Tile((0, i * sideLength), (500, 3), BLACK)  # adding grid lines
            wall_group.add(wall)
            all_sprites_group.add(wall)

            for j in range(Level1.nMazeNum + 1):
                if i == 0:
                    wall = Tile((j * sideLength, 0), (3, 500), BLACK)
                    wall_group.add(wall)
                    all_sprites_group.add(wall)

                if i == Level1.nMazeNum or j == Level1.nMazeNum:  # if it is the fringe of the Level1.maze, then go on
                    continue

                if Level1.maze[i][j] == 1:

                    tile = Tile([j * sideLength, i * sideLength], [sideLength + 0.8, sideLength + 0.8], BLACK)
                    # adding 0.8 is not a very good way but makes the Level1.maze look better
                    tile_group.add(tile)
                    all_sprites_group.add(tile)

                elif Level1.maze[i][j] == 2:
                    size = [sideLength * 0.4,
                            sideLength * 0.4]  # the size of the player will make up two fifths of a tile
                    self.myPlayer = Player1((j * sideLength + sideLength * 0.3, i * sideLength + sideLength * 0.3), [i, j],
                                      size, BLUE)  # player is centred
                    all_sprites_group.add(self.myPlayer)

                elif Level1.maze[i][j] == 3:
                    size = [sideLength * 0.4, sideLength * 0.4]
                    princess = Tile((j * sideLength + sideLength * 0.3, i * sideLength + sideLength * 0.3), size, RED)
                    all_sprites_group.add(princess)
                    Level1.princessPos = [i, j]

    def get_solution(self):
        self.solution=-1
        q = deque()
        # every element in q is a list of three integers s[0]: row num, s[1]:column number, s[2]: number of steps
        visited = [[0] * Level1.nMazeNum for i in range(Level1.nMazeNum)]
        dir = [[0, 1, 0, -1], [1, 0, -1, 0]]
        startPos=self.myPlayer.get_cor()
        endPos=Level1.princessPos
        q.append([startPos[0], startPos[1], 0])
        while q:
            s = q.popleft()
            if [s[0], s[1]] == endPos:
                self.solution=s[2]
                break
            for i in range(4):
                newR = s[0] + dir[0][i]
                newC = s[1] + dir[1][i]
                if newR < 0 or newR >= Level1.nMazeNum or newC < 0 or newC >= Level1.nMazeNum or Level1.maze[newR][
                    newC] == 1 or visited[newR][newC]:
                    continue
                q.append([newR, newC, s[2] + 1])
                visited[newR][newC] = 1



    def display_information(self):
        # game instruction
        gameInstruction = []
        gameInstruction.append(font.render("Game Instruction:", True, RED))
        gameInstruction.append(font.render("Move the player to", True, BLACK))
        gameInstruction.append(font.render("meet the princess", True, BLACK))
        gameInstruction.append(font.render("in minimum number", True, BLACK))
        gameInstruction.append(font.render("of moves", True, BLACK))
        for i in range(len(gameInstruction)):
            screen.blit(gameInstruction[i],[500+10,i*30])

        # game information
        if self.myPlayer.get_cor()==Level1.princessPos and self.myPlayer.get_time()==self.solution:
            screen.blit(font.render("You Win!", True, RED), [500 + 10, 200 + 10])
            screen.blit(font.render("Congrtulations",True,RED),[500+10,200+10+30])
        elif self.myPlayer.get_cor()==Level1.princessPos:
            screen.blit(font.render("Well done!", True, RED), [500 + 10, 200 + 10])
            screen.blit(font.render("Try to do it with", True, RED), [500 + 10, 200 + 10 + 30])
            screen.blit(font.render("fewer moves", True, RED), [500 + 10, 200 + 10 + 30*2])

        screen.blit(font.render("steps taken: "+str(self.myPlayer.get_time()),True,BLACK),[500+10,300+10])
        screen.blit(font.render("steps required: " + str(self.solution), True, BLACK), [500 + 10, 300 + 10+30])

    def retry(self):
        if self.retryButton.isPressed():
            self.myPlayer.reset()

    def restart(self):
        if self.restartButton.isPressed():
            all_sprites_group.empty()
            wall_group.empty()
            tile_group.empty()

            self.pre_update()

    def pre_update(self):
        self.initialise()
        self.get_solution()

    def update(self):
        self.retryButton.update()
        self.retry()
        self.restart()
        self.restartButton.update()
        self.display_information()



class Player1(Player):  # class Player1 is a friend of class Level1

    def __init__(self, pos, cor, size, color):
        Player.__init__(self,pos, cor, size, color)
        self.oriTime=self.time=0

    def tracking_key(self,keys):
        dis=500/Level1.nMazeNum
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

        flag = (0<=newR<Level1.nMazeNum) and (0<=newC<Level1.nMazeNum) and (Level1.maze[newR][newC]!=1)

        if flag:
            if dirX:
                self.rect.move_ip(dirX , 0)
                self.cor[1]=newC
                self.time+=1
            if dirY:
                self.rect.move_ip(0 , dirY)
                self.cor[0]=newR
                self.time+=1

    def get_time(self):
        return self.time

    def reset(self):
        self.cor=copy.deepcopy(self.oriCor) # any oriCor must be deeply copied
        self.rect.x=self.oriPos[0]
        self.rect.y=self.oriPos[1]
        self.time=self.oriTime


done = False

l1=Level1()
l1.pre_update()

while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done=True
        elif event.type == pg.KEYDOWN:
            l1.myPlayer.tracking_key(event.key)




    screen.fill(WHITE)
    all_sprites_group.draw(screen)
    l1.update()   # this line must be after the group draw code


    pg.display.flip()
    clock.tick(60)



