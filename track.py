#!/usr/bin/env python
import pygame
import math
from globals import *

class Track:
    
    radius = 300
    center = [400, 300]
    checkpoints = [[400, 50], [750, 300], [400, 550], [50, 300]]
    
    def __init__(self):
        pass
    
    def draw(self, screen):
        #rect = pygame.Rect(0, 0, 800, 600)
        pygame.draw.circle(screen, color_black, self.center, self.radius, 30)
        #pygame.gfxdraw.ellipse(screen, 400, 300, 350, 250, color)
        
    def distance_to_center(self, posx, posy):
        distance = math.sqrt((posx - self.center[x])**2 + (posy - self.center[y])**2)
        return math.fabs(self.radius-distance)
    
    def distance_to_checkpoint(self, posx, posy, number):
        checkpoint = self.checkpoints[number]
        distance = calc_distance(posx, posy, checkpoint[x], checkpoint[y])
        return distance
    
    def get_num_checkpoints(self):
        return len(self.checkpoints)