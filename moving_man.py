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
screen_width=700
screen_height=500
# Set the width and height of the screen [width, height]
size = (700, 500)
screen = pg.display.set_mode(size)
pg.init()



class Player(pg.sprite.Sprite):
    def __init__(self,color,width,height):
        super().__init__()
        self.image=pg.Surface([width,height])
        self.image.fill(color)
        self.rect=self.image.get_rect()
        self.rect.x=10
        self.rect.y=380
        self.jumpPower=9

        self.grav = 0.4
        self.x_vel = 0
        self.y_vel = 0
        self.state = 0




    def enter_jump(self):
        self.state=1
        self.y_vel=-self.jumpPower



    def enter_fall(self):
        self.state=2
        self.y_vel=0


    def tracking_key(self,keys):
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rect.move_ip(-3,0)
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rect.move_ip(3,0)


    def platform(self):
        if(0<self.rect.x<211 and self.rect.y>380):
            self.rect.y=380
        if(344<self.rect.x<494 and self.rect.y>381):
            self.oriY=self.rect.y=381-30
        if(559<self.rect.x<697-30 and (408-30-20>self.rect.y or self.rect.y>408-30)):
            self.oriY=self.rect.y=408-30



    def physics_update(self):
        if(self.rect.y+50>size[1]):
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
        self.rect.move_ip(self.x_vel,self.y_vel)
        self.physics_update()



player=Player(RED,30,30)
all_sprites_list=pg.sprite.Group()
all_sprites_list.add(player)

font = pg.font.SysFont('Calibri', 25, True, False)
# Used to manage how fast the screen updates
clock = pg.time.Clock()
#pg.mouse.set_visible(False)
background_image = pg.image.load("generic_platformer_tiles.png").convert()
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


    screen.blit(background_image, [0,0])
    all_sprites_list.update()
    all_sprites_list.draw(screen)
    bridge=False
    if(340>player.rect.x>270 and player.rect.y>350):
        bridge=True
        pg.draw.line(screen, GREEN, [210,409], [347, 381], 5)
    if(210<player.rect.x<340 and player.rect.y>=380 and not bridge):
        player.fall()
    if(500<player.rect.x<550 and player.rect.y+30>380):
        player.fall()
    pg.draw.line(screen, GREEN, [487,377], [557, 408], 5)
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
