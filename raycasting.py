import pygame as pg 
import math
from setting import*
RES  = WIDTH , HEIGHT = 1600 , 900
FPS = 60 
HALF_WIDTH  = WIDTH //2 
HALF_HEIGHT = HEIGHT  // 2 

PLAYER_POS = 1.5 , 5 
PLAYER_ANGLE  = 0 
PLAYER_SPEED  = 0.004 
PLAYER_ROT_SPEED = 0.002 

FOV  = math.pi /3 
HALF_FOV  = FOV /2 
NUM_RAYS = WIDTH //2 
HALF_NUM_RAYS = NUM_RAYS //2 
DELTA_ANGLE  = FOV / NUM_RAYS
MAX_DEPTH =  20 

SCREEN_DIST =  HALF_WIDTH / math.tan(HALF_FOV)
SCALE = WIDTH // NUM_RAYS
class RayCasting :
    def __init__(self , game) :
        self.game = game 
    def ray_cast(self) :
        ox ,  oy   = self.game.player.pos 
        x_map  , y_map  = self.game.player.pos
        ray_angle  = self.game.player.angle - HALF_FOV + 0.0001
        for ray in range(NUM_RAYS) :
            sin_a  = math.sin(ray_angle)
            cos_a  = math.cos(ray_angle)
            ##horizontal cross overs 
            y_hor , dy  = (y_map +1 , 1) if sin_a > 0 else (y_map -1e-6  , -1)

            depth_hor  = (y_hor - oy) / sin_a 
            x_hor =  ox + depth_hor  * cos_a 
            delta_depth  = dy / sin_a 
            dx  = delta_depth *cos_a 
            for i in range(MAX_DEPTH) :
                tile_hor = int(x_hor) , int(y_hor)
                if tile_hor in self.game.map.world_map :
                    break 
                x_hor  = x_hor + dx
                y_hor  = y_hor + dy 
                depth_hor =  depth_hor + delta_depth


            ## vertical cross sections 

            x_vert  , dx = (x_map+1, 1) if cos_a >0 else (x_map - 1e-6  , -1)
            depth_vert  = (x_vert-ox)/cos_a 
            y_vert = oy+depth_vert +sin_a

            delta_depth = dx/cos_a
            dy =  delta_depth *sin_a 

            for i in range(MAX_DEPTH) :
                tile_vert =  int(x_vert) , int(y_vert)
                if tile_vert in self.game.map.world_map  :
                    break
                x_vert = x_vert + dx 
                y_vert = y_vert + dy 
                depth_vert  = depth_vert  + delta_depth

            if depth_vert < depth_hor :
                depth = depth_vert 
            else :
                depth  = depth_hor

            depth  = depth * math.cos(self.game.player.angle -  ray_angle )
           # pg.draw.line(self.game.screen , 'yellow' , (100*ox , 100*oy) , (100*ox + 100*depth *cos_a , 100 *oy + 100*depth *sin_a) ,2)
            proj_height  = SCREEN_DIST / (depth +0.0001)
            color  = [255/(1+depth ** 5 *(0.00002))]*3 
            pg.draw.rect(self.game.screen , color , (ray *SCALE , HALF_HEIGHT - (proj_height //2) , SCALE , proj_height ))
            ray_angle =  ray_angle + DELTA_ANGLE
    
    def update(self):
        self.ray_cast()
