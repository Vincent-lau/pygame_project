import pygame as pg
import random
import copy
import math
import queue


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARKGREY=(169,169,169)
GREY=(96,96,96)
RED = (255, 0, 0)
BLUE=(0,0,255)
INF=2**31

all_sprites_group=pg.sprite.Group()
pg.init()
font = pg.font.SysFont('Calibri', 25, True, False)
clock = pg.time.Clock()
screenSize = (700, 500)
screen = pg.display.set_mode(screenSize)


class Element(pg.sprite.Sprite):  # this class is the father class of all relevant classes in the game
    def __init__(self,pos,cor,size,color):
        super().__init__()
        self.image = pg.Surface(size)
        self.image.fill(color)
        self.centre = copy.deepcopy(pos)
        self.pos = [pos[0]-size[0]/2,pos[1]-size[1]/2]
        # pos parameter will be the top-left corner of the shape
        self.ori_pos = copy.deepcopy(self.pos)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.cor = cor  # cor[0] is the row number and cor[1] is the column number
        self.ori_cor = copy.deepcopy(cor) # any ori_cor must use deepcopy
        self.size = size

    def tracking_event(self,keys=None):
        pass

    def move(self,end_pos=None):
        pass

    def set_pos(self,pos):
        self.rect.x=pos[0]-self.size[0]/2
        self.rect.y=pos[1]-self.size[1]/2

    def set_cor(self,cor):
        self.cor=cor

    def set_size(self,size):
        self.size=size

    def get_cor(self):
        return self.cor

    def get_size(self):
        return self.size

    def get_pos(self):
        return self.pos

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
        self.solution = -1
        self.button_list = []

    def initialise(self):
        pass
    
    def get_solution(self): # find the optimum solution of a problem
        pass
    
    def display_info(self):  # display necessary information of the game, such as life, time steps
        pass
    
    def restart(self):  # start the game again
        pass

    def retry(self):    # reset the game while keeping the map the same
        pass

    def display_solution(self):
        pass

    def button_function(self):
        self.restart()
        self.retry()
        self.display_solution()
        for b in self.button_list:
            b.update()

    def pre_update(self): # pre_update will run outside the main program loop
        self.initialise()
        self.get_solution()

    def update(self):
        pass


class Level1(Level):
    maze=[]
    princessCor = [0, 0]
    nMazeNum = 0
    tile_list=[]    # tile_list[i][j] means the tile with cor (i,j)

    def __init__(self):
        super().__init__()
        self.retryButton = Button([screenSize[1] + 10, 400 + 10], [70, 40], GREY, "retry")
        self.button_list.append(self.retryButton)
        self.restartButton = Button([600 + 10, 400 + 10], [70, 40], GREY, "restart")
        self.button_list.append(self.restartButton)
        self.solutionButton = Button([500 + 10, 450 + 10], [170, 30], GREY, "display solution")
        self.button_list.append(self.solutionButton)
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
                    self.myPlayer = Player1(t.get_centre(), [i, j],size, BLUE)  # player is centred
                    all_sprites_group.add(self.myPlayer)

                elif Level1.maze[i][j] == 3:
                    size = [sideLength * 0.4, sideLength * 0.4]
                    princess = NPC(t.get_centre(), [i,j],size,RED)
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

    def display_info(self):
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
        if self.myPlayer.get_cor()==Level1.princessCor and self.myPlayer.get_step()==self.solution:
            screen.blit(font.render("You Win!", True, RED), [500 + 10, 200 + 10])
            screen.blit(font.render("Congratulations",True,RED),[500+10,200+10+30])
        elif self.myPlayer.get_cor()==Level1.princessCor:
            screen.blit(font.render("Well done!", True, RED), [500 + 10, 200 + 10])
            screen.blit(font.render("Try to do it with", True, RED), [500 + 10, 200 + 10 + 30])
            screen.blit(font.render("fewer moves", True, RED), [500 + 10, 200 + 10 + 30*2])

        screen.blit(font.render("steps taken: " + str(self.myPlayer.get_step()), True, BLACK), [500 + 10, 300 + 10])
        screen.blit(font.render("steps required: " + str(self.solution), True, BLACK), [500 + 10, 300 + 10+30])

    def retry(self):    # reset the player position and the maze stays unchanged
        if self.retryButton.isPressed():
            self.myPlayer.reset()

    def restart(self):  # the maze is re-generated
        if self.restartButton.isPressed():
            all_sprites_group.empty()
            self.tile_list=[]
            self.pre_update()

    def display_solution(self):
        if self.solutionButton.isPressed():
            for i in range(len(self.solution_list) - 1):
                s1 = self.solution_list[i]
                s2 = self.solution_list[i + 1]
                t1 = Level1.tile_list[s1[0]][s1[1]]
                t2 = Level1.tile_list[s2[0]][s2[1]]
                pg.draw.line(screen, GREEN, t1.get_centre(), t2.get_centre(), 3)

    def update(self):
        all_sprites_group.draw(screen)
        self.draw_tiles()
        self.button_function()
        self.display_info()


class NPC(Element):
    def __init__(self,pos,cor,size,color):
        Element.__init__(self, pos, cor, size, color)


class Player1(Element):  # class Player1 is a friend of class Level1

    def __init__(self, pos, cor, size, color):
        Element.__init__(self, pos, cor, size, color)
        self.step = 0

    def tracking_event(self,keys):
        if keys == pg.K_RIGHT:
            self.move([self.cor[0], self.cor[1]+1])
        elif keys == pg.K_LEFT:
            self.move([self.cor[0], self.cor[1] -1])
        elif keys == pg.K_UP:
            self.move([self.cor[0]-1, self.cor[1]])
        elif keys == pg.K_DOWN:
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
            self.step+=1

    def get_step(self):
        return self.step

    def reset(self):
        self.cor=copy.deepcopy(self.ori_cor) # any ori_cor must be deeply copied
        self.rect.x=self.ori_pos[0]
        self.rect.y=self.ori_pos[1]
        self.step = 0


class Node(pg.sprite.Sprite):   # node is specific to level2
    def __init__(self,pos,size,num,color):
        super().__init__()
        self.radius=size
        self.centre=pos
        self.color=color
        self.num=num
        self.weight=0

    def isMouseOver(self):
        mousePos = pg.mouse.get_pos()
        return self.centre[0]-self.radius < mousePos[0] < self.centre[0] + self.radius and \
            self.centre[1]-self.radius < mousePos[1] < self.centre[1] + self.radius

    def get_centre(self):
        return self.centre

    def get_size(self):
        return self.radius

    def get_color(self):
        return self.color

    def set_weight(self,w):
        self.weight=w

    def get_num(self):
        return self.num

    def get_weight(self):
        return self.weight

    def __lt__(self,other):
        return self.weight<other.weight


class Player2(Element):
    def __init__(self,pos,cor,size,color):
        Element.__init__(self, pos, cor, size, color)
        self.path = 0

    def tracking_event(self,button):
        pass
        if button==1: # left key pressed
            for n in Level2.node_list:
                if n.isMouseOver():
                    self.move(n)

    def move(self,node):
        flag=False
        for n in Level2.graph[self.cor]:
            if n.num==node.num:
                flag=True
                break

        if flag:
            Level2.visited_node.append(node)
            self.path+=node.weight
            self.cor = node.num
            p=node.get_centre()
            newX = p[0]-self.size[0]/2
            newY = p[1]-self.size[1]/2
            self.rect.x = newX
            self.rect.y = newY

    def move_back(self):
        if len(Level2.visited_node) > 1:
            n2 = Level2.visited_node.pop()
            n1 = Level2.visited_node[-1]
            self.cor = n1.num
            p = n1.get_centre()
            newX = p[0] - self.size[0] / 2
            newY = p[1] - self.size[1] / 2
            self.rect.x = newX
            self.rect.y = newY
            for n in Level2.graph[n1.num]:
                if n2.num == n.num:
                    self.path -= n.weight
                    break

    def reset(self):
        self.cor = copy.deepcopy(self.ori_cor)  # any ori_cor must be deeply copied
        self.rect.x = self.ori_pos[0]
        self.rect.y = self.ori_pos[1]
        self.path=0

    def get_path(self):
        return self.path


class Level2(Level):
    nNodeNum=0
    graph=[]    # graph is adjacency list where each element is [nodeNum,weight]
    node_list=[]
    visited_node=[]
    princessCor=0

    def __init__(self):
        super().__init__()
        self.myPlayer=Player2([0,0],0,[0,0],BLUE)
        self.retryButton=Button([screenSize[1]+10,350],[85,40],GREY,"retry")
        self.button_list.append(self.retryButton)
        self.restartButton=Button([screenSize[1]+100,350],[85,40],GREY,"restart")
        self.button_list.append(self.restartButton)
        self.backButton=Button([screenSize[1]+10,400],[85,40],GREY,"back")
        self.button_list.append(self.backButton)
        self.allEdgesButton=Button([screenSize[1]+100,400],[88,40],GREY,"all edges")
        self.button_list.append(self.allEdgesButton)
        self.solutionButton=Button([screenSize[1]+10,450],[180,40],GREY,"display solution")
        self.button_list.append(self.solutionButton)
        self.solution_list=[]

    def initialise(self):
        Level2.nNodeNum=random.randrange(3,30)
        # generate the position of every node
        num=int(math.sqrt(Level2.nNodeNum))+1
        sep=500/num
        i = 0
        j = 0
        minR=500
        for k in range(Level2.nNodeNum):
            start_x=int((j+0.1)*sep)  # leave some blank space
            end_x=int((j+0.9)*sep)
            start_y=int((i+0.1)*sep)
            end_y=int((i+0.9)*sep)
            circlePos=[random.randint(int(start_x+sep*0.2),int(end_x-sep*0.2)),random.randint(int(start_y+sep*0.2),int(end_y-sep*0.2))]
            # make sure the node is not too small
            radius=min(circlePos[0]-start_x,end_x-circlePos[0],circlePos[1]-start_y,end_y-circlePos[1])
            minR=min(radius,minR)
            Level2.node_list.append(Node(circlePos,radius,k,DARKGREY))
            j+=1
            if j == num:
                i += 1
                j %= num

        # generate the graph in a adjacency list
        Level2.graph = [[] for i in range(Level2.nNodeNum)]
        for i in range(Level2.nNodeNum):
            used = [0] * (Level2.nNodeNum + 1)
            used[i]=1
            outDegree = random.randrange(1, int(Level2.nNodeNum*0.8))
            j=0
            while j < outDegree:
                n = random.randrange(0, Level2.nNodeNum)
                if used[n]:
                    continue
                used[n]=1
                j+=1
                w = random.randrange(1, 100)
                node=Level2.node_list[n]
                node.set_weight(w)
                Level2.graph[i].append(node)

        # initialise the player
        n1=Level2.node_list[random.randrange(0, Level2.nNodeNum)]
        self.myPlayer=Player2(n1.get_centre(),n1.num,[minR,minR],BLUE)
        Level2.visited_node.append(n1)
        all_sprites_group.add(self.myPlayer)
        while True:
            n2=Level2.node_list[random.randrange(0,Level2.nNodeNum)]
            if n2.num!=n1.num:
                princess=NPC(n2.get_centre(),n2.num,[n2.get_size(),n2.get_size()],RED)
                all_sprites_group.add(princess)
                Level2.princessCor=n2.num
                break

    @staticmethod
    def draw_nodes():
        for i in range(Level2.nNodeNum):
            n=Level2.node_list[i]
            pg.draw.circle(screen,n.get_color(),n.get_centre(),n.get_size())

    @staticmethod
    def draw_visited_edges():
        for i in range(len(Level2.visited_node)-1):
            n1=Level2.visited_node[i]
            n2=Level2.visited_node[i+1]
            pg.draw.line(screen,GREEN,n1.get_centre(),n2.get_centre(),3)

    def draw_edges(self):
        for n in Level2.node_list:
            if n.isMouseOver():
                self.draw_edges_from_node(n)

        n=Level2.node_list[self.myPlayer.get_cor()]
        self.draw_edges_from_node(n)

    @staticmethod
    def draw_all_edges():
        for i in range(Level2.nNodeNum):
            for j in range(len(Level2.graph[i])):
                n1=Level2.node_list[i]
                n2=Level2.graph[i][j]
                pg.draw.aaline(screen,GREEN,n1.get_centre(),n2.get_centre())
                # p1 = n1.get_centre()
                # p2 = n2.get_centre()
                # screen.blit(font.render(str(n2.weight), True, BLACK), [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2])

    @staticmethod
    def draw_edges_from_node(node):
        font = pg.font.SysFont('Calibri', 20, True, False)
        for i in range(len(Level2.graph[node.num])):
            n1=node
            n2=Level2.graph[n1.num][i]
            p1 = n1.get_centre()
            p2 = n2.get_centre()
            screen.blit(font.render(str(n2.weight),True,BLACK),[(p1[0]+p2[0])/2,(p1[1]+p2[1])/2])
            pg.draw.aaline(screen, GREEN, p1,p2)

    def get_solution(self):  # find the optimum solution of a problem
        self.solution_list=[]
        visited=[0]*Level2.nNodeNum
        dist=[INF]*Level2.nNodeNum
        prev=[0]*Level2.nNodeNum
        pq=queue.PriorityQueue()
        nd=copy.deepcopy(Level2.node_list[self.myPlayer.get_cor()])
        nd.set_weight(0)
        pq.put(nd)
        prev[nd.num]=-1
        dist[nd.num]=0
        while not pq.empty():
            nd=pq.get()
            if visited[nd.num]:
                continue
            if nd.num == Level2.princessCor:
                self.solution=dist[nd.num]
                father=nd.num
                while True:
                    self.solution_list.append(father)
                    if prev[father] == -1:
                        break
                    father = prev[father]
                self.solution_list.reverse()
                print(self.solution_list)
                break
            visited[nd.num]=1
            for n in Level2.graph[nd.num]:
                if visited[n.num]:
                    continue
                if dist[n.num] > dist[nd.num] + n.weight:
                    dist[n.num] = dist[nd.num] + n.weight
                    prev[n.num] = nd.num
                    pq.put(n)

    def display_info(self):  # display necessary information of the game, such as life, time steps
        # game instruction
        gameInstruction = []
        gameInstruction.append(font.render("Game Instruction:", True, RED))
        gameInstruction.append(font.render("Click a node to move", True, BLACK))
        gameInstruction.append(font.render("the player to meet", True, BLACK))
        gameInstruction.append(font.render("the princess by the", True, BLACK))
        gameInstruction.append(font.render("shortest path", True, BLACK))
        for i in range(len(gameInstruction)):
            screen.blit(gameInstruction[i], [500 + 10, i * 30])

        # game information
        if self.myPlayer.get_cor() == Level2.princessCor and self.myPlayer.get_path() == self.solution:
            screen.blit(font.render("You Win!", True, RED), [screenSize[1] + 10, 200 + 10])
            screen.blit(font.render("Congratulations", True, RED), [screenSize[1] + 10, 200 + 10 + 30])
        elif self.myPlayer.get_cor() == Level2.princessCor:
            screen.blit(font.render("Well done!", True, RED), [screenSize[1] + 10, 200 + 10])
            screen.blit(font.render("Try to do it with", True, RED), [screenSize[1] + 10, 200 + 10 + 20])
            screen.blit(font.render("fewer moves", True, RED), [screenSize[1] + 10, 200 + 10 + 20 * 2])

        screen.blit(font.render("path length: " + str(self.myPlayer.get_path()), True, BLACK), [screenSize[1] + 10, 275 + 10])
        screen.blit(font.render("shortest path: " + str(self.solution), True, BLACK), [screenSize[1] + 10, 275 + 10 + 30])

    def restart(self):  # start the game again
        if self.restartButton.isPressed():
            all_sprites_group.empty()
            Level2.graph=[]
            Level2.node_list=[]
            Level2.visited_node=[]
            self.pre_update()
            self.myPlayer.reset()

    def back(self):
        if self.backButton.isPressed():
            self.myPlayer.move_back()

    def retry(self):  # reset the game while keeping the map the same
        if self.retryButton.isPressed():
            Level2.visited_node=[]
            self.myPlayer.reset()

    def display_all_edges(self):
        if self.allEdgesButton.isPressed():
            self.draw_all_edges()

    def display_solution(self):
        if self.solutionButton.isPressed():
            for i in range(len(self.solution_list)-1):
                n1=Level2.node_list[self.solution_list[i]]
                n2=Level2.node_list[self.solution_list[i+1]]
                pg.draw.line(screen, RED, n1.get_centre(), n2.get_centre(), 3)

    def update(self):
        self.draw_nodes()
        self.draw_edges()
        self.draw_visited_edges()
        self.display_info()
        self.button_function()
        self.display_all_edges()
        self.back()
        all_sprites_group.draw(screen)


class Item(Element):
    def __init__(self,pos,size,color,cor,v,w):
        Element.__init__(self, pos, cor,size, color)
        self.volume=v
        self.weight=w
        self.selected = False

    def get_weight(self):
        return self.weight

    def get_volume(self):
        return self.volume

    def is_mouse_over(self):
        mousePos = pg.mouse.get_pos()
        return self.centre[0]-self.size[0]/2 < mousePos[0] < self.centre[0] + self.size[0]/2 and \
            self.centre[1]-self.size[1]/2 < mousePos[1] < self.centre[1] + self.size[1]/2

    def mouse_pressed(self): # detects if the item is left or right clicked
        if self.is_mouse_over():
            if pg.mouse.get_pressed()[0]:
                return 1
            elif pg.mouse.get_pressed()[2]:
                return 2
        return 0

    def clicked(self):
        if self.mouse_pressed() == 1 and not self.selected:
            self.selected = True
            return 1
        elif self.mouse_pressed() == 2 and self.selected:
            self.selected = False
            return -1
        else:
            return 0

    def highlight(self,color):
        pg.draw.rect(screen, color, [self.pos, self.size], 4)

    def deselect(self):
        self.selected = False

class Bag(Element):
    def __init__(self,pos,size,color,cor,v):
        Element.__init__(self,pos,cor,size,color)
        self.volume=v
        self.ori_v = v
        self.weight=0

    def set_weight(self,w):
        self.weight=w

    def set_volume(self,v):
        self.volume=v

    def get_volume(self):
        return self.volume

    def get_weight(self):
        return self.weight

    def reset(self):
        self.weight = 0
        self.volume = self.ori_v


class Level3(Level):
    n_item_num = 0
    item_list = []

    def __init__(self):
        super().__init__()
        self.myPlayer=Bag([250,65],[100,70],RED,0,random.randint(10,100))
        all_sprites_group.empty()
        self.retryButton = Button([screenSize[1] + 10, 330], [85, 50], GREY, "retry")
        self.button_list.append(self.retryButton)
        self.restartButton = Button([screenSize[1] + 100, 330], [85, 50], GREY, "restart")
        self.button_list.append(self.restartButton)
        self.solutionButton = Button([screenSize[1] + 10, 400], [180, 60], GREY, "display solution")
        self.button_list.append(self.solutionButton)
        self.solution_list = []

    def initialise(self):
        Level3.n_item_num=random.randrange(4,30)
        self.myPlayer = Bag([250, 65], [100, 70], RED, 0, random.randint(10, 100))
        all_sprites_group.add(self.myPlayer)
        num_x = int(math.sqrt(10/7*Level3.n_item_num))+1
        num_y = int(math.sqrt(7/10*Level3.n_item_num))+1
        sep_x = 500/num_x
        sep_y = 350/num_y
        i = 0
        j = 0
        for k in range(Level3.n_item_num):
            start_x = int((j+0.3)*sep_x)
            end_x = int((j+0.7)*sep_x)
            start_y = 150+int((i + 0.3) * sep_y)
            end_y = 150 + int((i + 0.7) * sep_y)
            item_pos = [start_x,start_y]
            size = [end_x-start_x,end_y-start_y]
            v = random.randrange(5,50)
            w = random.randrange(1,100)
            item = Item(item_pos,size,BLACK,k,v,w)
            Level3.item_list.append(item)
            all_sprites_group.add(item)
            j += 1
            if j == num_x:
                i += 1
                j %= num_x

    def display_weight_and_volume(self):
        p = self.myPlayer.get_pos()
        s = self.myPlayer.get_size()
        pos = [p[0], p[1]+s[1]]
        font = pg.font.SysFont('Calibri', 25, True, False)
        screen.blit(font.render("V   =   "+str(self.myPlayer.get_volume()), True, BLACK), pos)
        screen.blit(font.render("W   =   "+str(self.myPlayer.get_weight()),True,BLACK), [pos[0],pos[1]+20])

        for item in Level3.item_list:
            p = item.get_pos()
            s = item.get_size()
            pos = [p[0], p[1]+s[1]+5]
            font = pg.font.SysFont('Calibri', int(s[0]*0.7), True, False)
            screen.blit(font.render("V=" + str(item.get_volume()), True, BLUE), pos)
            screen.blit(font.render("W=" + str(item.get_weight()), True, BLUE), [pos[0], pos[1] + s[0]*0.5])

    def item_highlight(self):
        for item in Level3.item_list:
            added = item.clicked()
            if item.selected:
                item.highlight(GREEN)
            if added == 1:
                self.myPlayer.weight += item.get_weight()
                self.myPlayer.volume -= item.get_volume()
            elif added == -1:
                self.myPlayer.weight -= item.get_weight()
                self.myPlayer.volume += item.get_volume()

    def get_solution(self):  # find the optimum solution of a problem
        w = [0]*(Level3.n_item_num+1)
        v = [0]*(Level3.n_item_num+1)
        for i in range(1,Level3.n_item_num+1):
            w[i] = Level3.item_list[i-1].get_weight() # i-1 is because index starts from 0 in the item_list
            v[i] = Level3.item_list[i-1].get_volume()

        dp = [[0]*(self.myPlayer.volume+1) for i in range(Level3.n_item_num+1)]
        choices = [[[]] * (self.myPlayer.volume + 1) for i in range(Level3.n_item_num + 1)]
        # store how items are selected for dp[i][j]
        for i in range(1,Level3.n_item_num+1):
            for j in range(1,self.myPlayer.get_volume()+1):
                dp[i][j] = dp[i-1][j]
                choices[i][j] = choices[i-1][j]
                if j >= v[i] and dp[i-1][j-v[i]]+w[i] > dp[i-1][j]:
                    dp[i][j] = dp[i-1][j-v[i]]+w[i]
                    choices[i][j] = choices[i-1][j-v[i]] + [i]

        self.solution = dp[Level3.n_item_num][self.myPlayer.get_volume()]
        print(Level3.n_item_num,choices[Level3.n_item_num][self.myPlayer.get_volume()])
        self. solution_list = choices[Level3.n_item_num][self.myPlayer.get_volume()]

    def display_info(self):  # display necessary information of the game, such as life, time steps
        # game instruction
        gameInstruction = []
        gameInstruction.append(font.render("Game Instruction:", True, RED))
        gameInstruction.append(font.render("Select items that ", True, BLACK))
        gameInstruction.append(font.render("will have maximum", True, BLACK))
        gameInstruction.append(font.render("overall weight with a", True, BLACK))
        gameInstruction.append(font.render("given volume", True, BLACK))
        for i in range(len(gameInstruction)):
            screen.blit(gameInstruction[i], [500 + 10, i * 30])

        # game information
        if self.myPlayer.get_weight() == self.solution:
            screen.blit(font.render("You Win!", True, RED), [500 + 10, 200 + 10])
            screen.blit(font.render("Congratulations", True, RED), [500 + 10, 200 + 10 + 30])

        if self.myPlayer.get_volume() < 0:
            screen.blit(font.render("Whoops! Right lick ", True, RED), [500 + 10, 200 + 10])
            screen.blit(font.render("selected item again", True, RED), [500 + 10, 200 + 10 + 20])
            screen.blit(font.render("to deselect it", True, RED), [500 + 10, 200 + 10 + 20 + 20])

        screen.blit(font.render("Largest weight: " + str(self.solution), True, BLACK), [500 + 10, 280])

    def restart(self):  # start the game again
        if self.restartButton.isPressed():
            all_sprites_group.empty()
            Level3.item_list = []
            self.pre_update()
            self.myPlayer.reset()

    def retry(self):  # reset the game while keeping the map the same
        if self.retryButton.isPressed():
            for item in Level3.item_list:
                item.deselect()
            self.myPlayer.reset()

    def display_solution(self):
        if self.solutionButton.isPressed():
            for s in self.solution_list:
                Level3.item_list[s-1].highlight(RED)

    def update(self):
        self.display_weight_and_volume()
        self.display_info()
        self.item_highlight()
        self.button_function()
        all_sprites_group.draw(screen)



done = False

curLevel=Level3()
curLevel.pre_update()

while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done=True
        elif event.type == pg.KEYDOWN:
            curLevel.myPlayer.tracking_event(event.key)
        elif event.type==pg.MOUSEBUTTONDOWN:
            curLevel.myPlayer.tracking_event(event.button)

    screen.fill(WHITE)
    curLevel.update()   # this line must be after the group draw code

    pg.display.flip()
    clock.tick(60)



