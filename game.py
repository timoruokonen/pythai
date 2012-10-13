#!/usr/bin/env python
import car
import math
import track
import pygame
from globals import *

class Game:
    
    max_score = 100.0
    thecar = car.Car()
    thetrack = track.Track()    
    # Time resolution in seconds
    time_res = 1/30.0
    
    curr_checkpoint = 0
    
    time = 0.0
    
    def __init__(self):
        self.thecar.set_start_pos(50,300)
        self.start_time = pygame.time.get_ticks()
    
    def set_car_throttle(self, amount):
        self.thecar.set_throttle(amount)
        
    def set_car_brake(self, amount):
        self.thecar.set_brake(amount)
        
    def set_car_steer(self, amount):
        self.thecar.set_steer(amount)
        
    def get_car(self):
        return self.thecar
        
    # Advance game simulation
    def advance(self):
        self.time += self.time_res
        self.thecar.update_position(self.time_res)
        
        # Have we reached next checkpoint? If so, choose next one
        if self.checkpoint_reached(1, self.curr_checkpoint):
            print 'Checkpoint ', self.curr_checkpoint, ' reached!'
            self.curr_checkpoint += 1
            if self.curr_checkpoint >= self.thetrack.get_num_checkpoints():
                self.end_time = pygame.time.get_ticks()
                lap_time = float((self.end_time - self.start_time)) / 1000.0
                print 'GOAL reached!!! Lap time: ', lap_time, 's'
                self.curr_checkpoint = 0
                self.start_time = pygame.time.get_ticks()
        
    # Set time resolution for simulation
    def set_time_res(self, resolution):
        time_res = resolution
        
    # Get current game score
    def get_score(self):
        car_distance = self.thetrack.distance_to_center(self.thecar.pos[x], self.thecar.pos[y])
        return self.max_score - car_distance
        
    def print_debug(self):
        #print 'Current SCORE: ', self.get_score(), ' Checkpoint distance: ', \
        self.get_checkpoint_distance(1, self.curr_checkpoint)
        
    def get_checkpoint_distance(self, player, number):
        return self.thetrack.distance_to_checkpoint(self.thecar.pos[x], self.thecar.pos[y], number)
    
    def checkpoint_reached(self, player, number):
        if self.get_checkpoint_distance(player, number) < 100:
            return True
        else: return False
        
    def draw(self, screen):
        self.thetrack.draw(screen)
        self.thecar.draw(screen)

    
    
