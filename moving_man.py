"""
 pg base template for opening a window

 Sample Python/pg Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

 Explanation video: http://youtu.be/vRB_983kUMc
"""

import pygame as pg
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARKGREY=(169,169,169)
RED = (255, 0, 0)
BLUE=(0,0,255)

screenSize = (700, 500)
screen = pg.display.set_mode(screenSize)
pg.init()



class Block(pg.sprite.Sprite):
    def __init__(self,color,size,position):
        super().__init__()
        self.image=pg.Surface(size)
        self.image.fill(color)
        self.rect=self.image.get_rect(topleft=position)




class Player(pg.sprite.Sprite):

    def __init__(self,color,size,pos=(0,0)):
        super().__init__()
        self.image=pg.Surface(size)
        self.image.fill(color)
        self.oriPos=(0,0)
        self.rect=self.image.get_rect(topleft=pos)
        self.size=self.image.get_size()
        self.lives=3
        self.jumpPower=9

        self.grav = 0.4
        self.x_vel = 0
        self.y_vel = 0
        self.state = 0   #0:stationary 1:rising 2:falling


    def get_position(self):
        return self.rect
    def set_pos(self,pos):
        self.rect.x=pos[0]
        self.rect.y=pos[1]
    def get_size(self):
        return self.size
    def get_lives(self):
        return player.lives

    def hurt(self):
        self.lives-=1
        if(self.lives<=0):
           pass
        else:
            self.set_pos(self.oriPos)



    def enter_jump(self):
        if(self.state==0):
            self.state=1
            self.y_vel=-self.jumpPower



    def enter_fall(self):
        self.state=2



    def tracking_key(self,keys):
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rect.move_ip(-3,0)
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rect.move_ip(3,0)


    def collision_below(self):
        if(pg.sprite.spritecollideany(self,grounds)):
            self.rect.y -=1   #this is not very good way of moving back one step
            self.state=0
            self.y_vel=0


    def physics_update(self):
        if(self.rect.y>screenSize[1]):
            self.y_vel=0


        if(self.state==2):  #falling
            self.y_vel+=self.grav

        elif(self.state==1):  #rising
            if(self.y_vel>=0):
                self.enter_fall()
            else:
                self.y_vel+=self.grav

        else:
            self.y_vel=0


    def update(self):
        self.physics_update()
        self.collision_below()
        self.rect.move_ip(self.x_vel,self.y_vel)





all_sprites_list=pg.sprite.Group()
grounds=pg.sprite.Group()

player = Player(RED, (30, 30))





def level_control(level,player,grounds,update):
    if(level==1):
        if(update):
            grounds.empty()
            all_sprites_list.empty()
            player.oriPos=(0,450-player.get_size()[1])
            player.set_pos(player.oriPos)
            all_sprites_list.add(player)
            grounds.add(Block(BLACK, (100, 50), (0, 450)), Block(BLACK, (50, 50), (650, 450)))
            all_sprites_list.add(Block(BLACK, (100, 50), (0, 450)), Block(BLACK, (50, 50), (650, 450)))


        player.pos=player.get_position()
        if(player.pos.x>100 and player.pos.x+player.get_size()[0]<650):
            if(len(grounds.sprites())==2):
                player.enter_fall()
                if(player.rect.y>=screenSize[1]):
                    player.hurt()

        if(130<player.pos.x<150 and 400<player.pos.y<450):
            b=Block(GREEN,(550,10),(100,450))
            grounds.add(b)
            all_sprites_list.add(b)


    elif(level==2):
        if(update):
            grounds.empty()
            all_sprites_list.empty()
            b=Block(BLACK,(50,50),(0,450))
            grounds.add(b)
            all_sprites_list.add(b)
            b=Block(BLUE,(40,10),(50,450))

            all_sprites_list.add(b)
            b=Block(BLACK,(110,50),(90,450))
            grounds.add(b)
            all_sprites_list.add(b)
            b=Block(DARKGREY,(60,50),(200,450))
            grounds.add(b)
            all_sprites_list.add(b)
            b=Block(BLACK,(140,50),(260,450))
            grounds.add(b)
            all_sprites_list.add(b)
            b=Block(BLACK,(30,50),(400,450))
            grounds.add(b)
            all_sprites_list.add(b)
            b=Block(BLACK,(270,50),(430,450))
            grounds.add(b)
            all_sprites_list.add(b)
            player.set_pos(player.oriPos)
            all_sprites_list.add(player)

font = pg.font.SysFont('Calibri', 25, True, False)
# Used to manage how fast the screen updates
clock = pg.time.Clock()
update=True     # update indicates whether it is the first time to enter a level
level=1



# -------- Main Program Loop -----------
done=False

while not done:
    # --- Main event loop
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done =True
        if event.type==pg.KEYDOWN:
            if event.key==pg.K_UP:
                player.enter_jump()


    player.tracking_key(pg.key.get_pressed())
    screen.fill(WHITE)


    print(player.state,player.get_position())

    if(player.get_position()[0]>screenSize[0]):
        level+=1
        update=True
    level_control(level,player,grounds,update)

    update=False
    all_sprites_list.update()
    all_sprites_list.draw(screen)
    text_live=font.render("remaining lives: "+str(player.get_lives()),True,BLACK)
    screen.blit(text_live,(20,20))


    # viewport.center=player.rect.center
    # viewport.clamp_ip(level_rect)
    # --- Screen-clearing code goes here

    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.

    # If you want a background image, replace this clear with blit'ing the
    # background image.

    # --- Go ahead and update the screen with what we've drawn.
    pg.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pg.quit()
