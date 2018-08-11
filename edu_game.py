import pygame as pg
import random
import copy
import math


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARKGREY=(169,169,169)
GREY=(96,96,96)
RED = (255, 0, 0)
BLUE=(0,0,255)

all_sprites_group=pg.sprite.Group()
pg.init()
font = pg.font.SysFont('Calibri', 25, True, False)
clock = pg.time.Clock()
screenSize = (700, 500)
screen = pg.display.set_mode(screenSize)


class Character(pg.sprite.Sprite):  # this class is the father of player and NPC
    def __init__(self,pos,cor,size,color):
        super().__init__()
        self.image=pg.Surface(size)
        self.oriPos=pos
        self.rect=self.image.get_rect(topleft=pos)
        self.image.fill(color)
        self.oriCor=copy.deepcopy(cor) # any oriCor must use deepcopy
        self.cor=cor    # cor[0] is the row number and cor[1] is the column number
        self.size=size

    def tracking_key(self,keys):
        pass

    def move(self,endPos):
        pass

    def get_cor(self):
        return self.cor

    def reset(self):
        pass


class Tile(pg.sprite.Sprite):   # tile is specific to level1
    def __init__(self,pos,size):
        super().__init__()
        self.image=pg.Surface(size)
        self.rect=self.image.get_rect(topleft=pos)
        self.color=1
        self.centre=[pos[0]+size[0]/2,pos[1]+size[1]/2]

    def set_color(self,color):
        # this is just a representation, color=1 means that the tile does not need to be filled,
        # color=0 means it should be filled
        self.color=color

    def get_color(self):
        return self.color

    def get_centre(self):
        return self.centre

    def get_rect(self):
        return self.rect


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
        self.solutionButton=Button([500+10,450+10],[170,30],GREY,"display solution")

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

    def pre_update(self): # pre_update will run outside the main program loop
        pass

    def update(self):
        pass


class Level1(Level):
    maze=[]
    princessCor = [0, 0]
    nMazeNum = 0
    tile_list=[]    # tile_list[i][j] means the tile with cor (i,j)

    def __init__(self):
        super().__init__()
        self.myPlayer=Player1([0,0],[0,0],[0,0],BLACK)
        self.solution_list=[]   # records each step taken in the optimum solution

    def initialise(self):
        # 1=wall 2=player 3=princess
        all_sprites_group.empty()
        Level1.nMazeNum = random.randrange(5, 30)
        Level1.maze = [[0] * Level1.nMazeNum for i in range(Level1.nMazeNum)]
        Level1.tile_list = [[Tile([0,0],[0,0])] * Level1.nMazeNum for i in range(Level1.nMazeNum)]

        nSpecialElement = random.randrange(0,
                                           int(Level1.nMazeNum * Level1.nMazeNum * 0.5))
        # randrange [a,b), 60% of the Level1.maze is wall
        playerCor = random.randrange(0, Level1.nMazeNum * Level1.nMazeNum)

        Level1.maze[playerCor // Level1.nMazeNum][playerCor % Level1.nMazeNum] = 2

        while True:
            princessCor = random.randrange(0, Level1.nMazeNum * Level1.nMazeNum)
            if princessCor != playerCor:
                break
        Level1.maze[princessCor // Level1.nMazeNum][princessCor % Level1.nMazeNum] = 3
        nSpecialElement -= 2
        for i in range(nSpecialElement):

            while True:
                wallCor = random.randrange(0, Level1.nMazeNum * Level1.nMazeNum)
                if wallCor != princessCor and wallCor != playerCor:
                    break

            Level1.maze[wallCor // Level1.nMazeNum][wallCor % Level1.nMazeNum] = 1

        sideLength = 500 / Level1.nMazeNum
        for i in range(Level1.nMazeNum):
            for j in range(Level1.nMazeNum):

                t = Tile((j * sideLength, i * sideLength), (sideLength, sideLength))

                if Level1.maze[i][j] == 1:
                    t.set_color(0)

                elif Level1.maze[i][j] == 2:
                    size = [sideLength * 0.4,
                            sideLength * 0.4]  # the size of the player will make up two fifths of a tile
                    self.myPlayer = Player1((t.get_centre()[0] - size[0] /2,  + t.get_centre()[1] - size[1]/2), [i, j],
                                      size, BLUE)  # player is centred
                    all_sprites_group.add(self.myPlayer)

                elif Level1.maze[i][j] == 3:
                    size = [sideLength * 0.4, sideLength * 0.4]
                    princess = NPC((t.get_centre()[0] - size[0] /2,  + t.get_centre()[1] - size[1]/2), [i,j],size,RED)
                    all_sprites_group.add(princess)
                    Level1.princessCor = [i, j]

                Level1.tile_list[i][j] = t

    def get_solution(self):
        self.solution=-1
        self.solution_list = []
        q = []
        qHead=0
        qTail=0
        # every element in q is a list of three integers s[0]: row num, s[1]:column number;
        # s[2]: number of steps, s[3]: father
        visited = [[0] * Level1.nMazeNum for i in range(Level1.nMazeNum)]
        dir = [[0, 1, 0, -1], [1, 0, -1, 0]]
        startPos=self.myPlayer.get_cor()
        endPos=Level1.princessCor
        q.append([startPos[0], startPos[1], 0, -1])
        qTail+=1
        while qHead!=qTail:
            s = q[qHead]
            if [s[0], s[1]] == endPos:
                self.solution=s[2]
                father = qHead
                while True:
                    self.solution_list.append([q[father][0],q[father][1]])
                    father=q[father][3]
                    if father==-1:
                        break
                self.solution_list.reverse()
                break
            for i in range(4):
                newR = s[0] + dir[0][i]
                newC = s[1] + dir[1][i]
                if newR < 0 or newR >= Level1.nMazeNum or newC < 0 or newC >= Level1.nMazeNum or Level1.maze[newR][
                    newC] == 1 or visited[newR][newC]:
                    continue
                q.append([newR, newC, s[2] + 1,qHead])
                qTail+=1
                visited[newR][newC] = 1
            qHead += 1

    def draw_tiles(self): # draw all tiles onto the screen in the tile_list
        for i in range(Level1.nMazeNum):
            for j in range(Level1.nMazeNum):
                t=Level1.tile_list[i][j]
                pg.draw.rect(screen,BLACK,t.get_rect(),t.get_color()*1)

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
        if self.myPlayer.get_cor()==Level1.princessCor and self.myPlayer.get_time()==self.solution:
            screen.blit(font.render("You Win!", True, RED), [500 + 10, 200 + 10])
            screen.blit(font.render("Congrtulations",True,RED),[500+10,200+10+30])
        elif self.myPlayer.get_cor()==Level1.princessCor:
            screen.blit(font.render("Well done!", True, RED), [500 + 10, 200 + 10])
            screen.blit(font.render("Try to do it with", True, RED), [500 + 10, 200 + 10 + 30])
            screen.blit(font.render("fewer moves", True, RED), [500 + 10, 200 + 10 + 30*2])

        screen.blit(font.render("steps taken: "+str(self.myPlayer.get_time()),True,BLACK),[500+10,300+10])
        screen.blit(font.render("steps required: " + str(self.solution), True, BLACK), [500 + 10, 300 + 10+30])

    def retry(self):    # reset the player position and the maze stays unchanged
        if self.retryButton.isPressed():
            self.myPlayer.reset()

    def restart(self):  # the maze is re-generated
        if self.restartButton.isPressed():
            all_sprites_group.empty()
            self.tile_list=[]
            self.pre_update()

    def pre_update(self):
        self.initialise()
        self.get_solution()

    def visualise_solution(self): # draw the solution onto the screen
        for i in range(len(self.solution_list)-1):
            s1=self.solution_list[i]
            s2=self.solution_list[i+1]
            t1=Level1.tile_list[s1[0]][s1[1]]
            t2=Level1.tile_list[s2[0]][s2[1]]
            pg.draw.line(screen,GREEN,t1.get_centre(),t2.get_centre(),3)

    def display_solution(self): # detect if the solution is pressed
        if self.solutionButton.isPressed():
            self.visualise_solution()

    def update(self):
        self.draw_tiles()
        self.retry()
        self.restart()
        self.display_solution()
        self.retryButton.update()
        self.restartButton.update()
        self.solutionButton.update()
        self.display_information()


class NPC(Character):
    def __init__(self,pos,cor,size,color):
        Character.__init__(self,pos,cor,size,color)


class Player1(Character):  # class Player1 is a friend of class Level1

    def __init__(self, pos, cor, size, color):
        Character.__init__(self,pos, cor, size, color)
        self.oriTime=self.time=0

    def tracking_key(self,keys):
        if keys==pg.K_RIGHT:
            self.move([self.cor[0],self.cor[1]+1])
        elif keys==pg.K_LEFT:
            self.move([self.cor[0], self.cor[1] -1])
        elif keys==pg.K_UP:
            self.move([self.cor[0]-1, self.cor[1]])
        elif keys==pg.K_DOWN:
            self.move([self.cor[0]+1, self.cor[1]])

    def move(self,endCor):
        newR=endCor[0]
        newC=endCor[1]
        flag = (0<=newR<Level1.nMazeNum) and (0<=newC<Level1.nMazeNum) and (Level1.maze[newR][newC]!=1)

        if flag:
            newCentre = Level1.tile_list[newR][newC].get_centre()
            newX = newCentre[0] - self.size[0] / 2
            newY = newCentre[1] - self.size[1] / 2
            self.rect.x=newX
            self.rect.y=newY
            self.cor[0]=newR
            self.cor[1]=newC
            self.time+=1

    def get_time(self):
        return self.time

    def reset(self):
        self.cor=copy.deepcopy(self.oriCor) # any oriCor must be deeply copied
        self.rect.x=self.oriPos[0]
        self.rect.y=self.oriPos[1]
        self.time=self.oriTime


class Node(pg.sprite.Sprite):   # node is specific to level2
    def __init__(self,pos,size,color):
        super().__init__()
        self.radius=size
        self.centre=pos
        self.color=color

    def get_centre(self):
        return self.centre

    def get_size(self):
        return self.radius

    def get_color(self):
        return self.color


class Level2(Level):
    nNodeNum=0
    graph=[]    # graph is adjacency list where each element is [nodeNum,weight]
    node_list=[]

    def __init__(self):
        super().__init__()


    def initialise(self):
        # randomly generate graph
        Level2.nNodeNum=random.randrange(3,30)
        Level2.graph=[[] for i in range(Level2.nNodeNum)]
        for i in range(Level2.nNodeNum):
            outDegree=random.randrange(1,Level2.nNodeNum)
            for j in range(outDegree):
                n=random.randrange(0,Level2.nNodeNum)
                w=random.randrange(1,100)
                Level2.graph[i].append([n,w])

        # generate the position of every node
        num=int(math.sqrt(Level2.nNodeNum))+1
        sep=500/num
        i = 0
        j = 0
        for k in range(Level2.nNodeNum):
            startX=int((j+0.1)*sep)  # leave some blank space
            endX=int((j+0.9)*sep)
            startY=int((i+0.1)*sep)
            endY=int((i+0.9)*sep)
            circlePos=[random.randint(int(startX+sep*0.2),int(endX-sep*0.2)),random.randint(int(startY+sep*0.2),int(endY-sep*0.2))]
            # make sure the node is not too small
            radius=min(circlePos[0]-startX,endX-circlePos[0],circlePos[1]-startY,endY-circlePos[1])
            Level2.node_list.append(Node(circlePos,radius,DARKGREY))
            j+=1
            if j == num:
                i += 1
                j %= num

    def draw_nodes(self):
        for i in range(Level2.nNodeNum):
            n=Level2.node_list[i]
            pg.draw.circle(screen,n.get_color(),n.get_centre(),n.get_size())

    def draw_edges(self):
        for i in range(Level2.nNodeNum):
            for j in range(len(Level2.graph[i])):
                c=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
                n1=Level2.node_list[i]
                n2=Level2.node_list[Level2.graph[i][j][0]]
                pg.draw.line(screen,c,n1.get_centre(),n2.get_centre(),3)


    def get_solution(self):  # find the optimum solution of a problem
        pass

    def display_information(self):  # display necessary information of the game, such as life, time steps
        pass

    def restart(self):  # start the game again
        pass

    def retry(self):  # reset the game while keeping the map the same
        pass

    def pre_update(self):  # pre_update will run outside the main program loop
        self.initialise()
        # print("node num",Level2.nNodeNum)
        # for i in range(Level2.nNodeNum):
        #     for j in range(len(Level2.graph[i])):
        #         print(Level2.graph[i][j],end=' ')
        #     print()

    def update(self):
        self.draw_nodes()
        self.draw_edges()

done = False

curLevel=Level2()
curLevel.pre_update()

while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done=True
        elif event.type == pg.KEYDOWN:
            curLevel.myPlayer.tracking_key(event.key)


    screen.fill(WHITE)
    all_sprites_group.draw(screen)
    curLevel.update()   # this line must be after the group draw code


    pg.display.flip()
    clock.tick(60)



