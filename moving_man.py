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
    def __init__(self,color,size):
        super().__init__()
        self.image=pg.Surface(size)
        self.image.fill(color)
        self.rect=self.image.get_rect()
        self.rect.x=0
        self.rect.y=450-size[1]
        self.jumpPower=9

        self.grav = 0.4
        self.x_vel = 0
        self.y_vel = 0
        self.state = 0   #0:stationary 1:rising 2:falling


    def get_position(self):
        return self.rect

    def enter_jump(self):
        if(self.state!=1):
            self.state=1
            self.y_vel=-self.jumpPower



    def enter_fall(self):
        self.state=2
       # self.y_vel=0


    def tracking_key(self,keys):
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rect.move_ip(-3,0)
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rect.move_ip(3,0)


    def collision_below(self):
        if(pg.sprite.spritecollideany(player,grounds)):
            self.rect.y -=1   #this is not very good way of moving back one step
            self.state=0
            self.y_vel=0
        else:
            self.enter_fall()


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

player=Player(RED,(30,30))
grounds=pg.sprite.Group()
grounds.add(Block(BLACK,(100,50),(0,450)),Block(BLACK,(50,50),(650,450)))

all_sprites_list.add(player)
all_sprites_list.add(Block(BLACK,(100,50),(0,450)),Block(BLACK,(50,50),(650,450)))


font = pg.font.SysFont('Calibri', 25, True, False)
# Used to manage how fast the screen updates
clock = pg.time.Clock()



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


    print(player.state)

    all_sprites_list.update()
    all_sprites_list.draw(screen)

    pg.draw.line(screen, GREEN, [487,377], [557, 408], 5)

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
