from setting import *
RES  = WIDTH , HEIGHT = 1600 , 900
FPS = 60 
PLAYER_POS = 2.5 , 5 
PLAYER_ANGLE  = 0 
PLAYER_SPEED  = 0.004 
PLAYER_ROT_SPEED = 0.002 

import pygame as pg
import math

class Player :
    def __init__(self , game) :
        self.game =  game 
        self.x  , self.y = PLAYER_POS 
        self.angle  = PLAYER_ANGLE 
    def movement(self):
        sin_a  = math.sin(self.angle)
        cos_a =  math.cos(self.angle)
        dx , dy  =  0 , 0
        self.delta_time = 1
        speed   = PLAYER_SPEED*(self.game.delta_time)
        speed_sin  = speed*sin_a 
        speed_cos = speed*cos_a 
        keys  = pg.key.get_pressed()
        if keys[pg.K_w] :
            dx =  dx +speed_cos 
            dy = dy + speed_sin 
        if keys[pg.K_s] :
            dx =  dx -speed_cos 
            dy = dy -speed_sin 
        if keys[pg.K_a] :
            dx =  dx +speed_sin
            dy = dy  - speed_cos 
        if keys[pg.K_d] :
            dx =  dx - speed_sin
            dy = dy + speed_cos 

        self.check_wall_collision(dx , dy)
        if keys[pg.K_LEFT] :
            self.angle   = self.angle-(PLAYER_ROT_SPEED *self.game.delta_time)
        if keys[pg.K_RIGHT] :
            self.angle   = self.angle +(PLAYER_ROT_SPEED *self.game.delta_time)
        self.angle  = self.angle%math.tau 

    def check_wall(self , x , y):
        return (x,y) not in self.game.map.world_map
    
    def check_wall_collision(self  , dx , dy):
        if self.check_wall(int(self.x+dx) , int(self.y)) :
            self.x  = self.x+dx
        if self.check_wall(int(self.x) , int(self.y +dy)) :
            self.y  = self.y+dy 
    def draw(self):
        start_pos = (int(self.x * 100), int(self.y * 100))
       # end_pos = (
         #   (self.x * 100 + WIDTH * math.cos(self.angle)),
        #    (self.y * 100 + WIDTH * math.sin(self.angle)),
       # )
      #  pg.draw.line(self.game.screen, 'yellow', start_pos, end_pos, 2)
        pg.draw.circle(self.game.screen, 'green', start_pos, 15)


    def update(self):
        self.movement()
    
    @property
    def pos(self):
        return self.x  ,self.y 
    
    @property
    def map_pos(self) :
        return int(self.x) , int(self.y)
    


    
