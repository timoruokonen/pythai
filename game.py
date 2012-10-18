#!/usr/bin/env python
import car
import math
import track
import pygame
from globals import *

class Game:
    game_over_score = -50.0
    max_score = 100.0
    check_point_reached_score = 10000.0
    lap_finished_score = 100000.0
    # Time resolution in seconds
        
    def __init__(self):
        self.time_res = 1/30.0
        self.time = 0.0
        self.thecar = car.Car()
        self.thetrack = track.Track()    
        self.curr_checkpoint = 0
        self.curr_lap_number = 0
        self.thecar.set_start_pos(50,300)
        self.start_time = pygame.time.get_ticks()
        self.total_score = 0.0
        self.game_over = False
        self.current_score = 0.0
    
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

        self.current_score = self.get_score() 
        if (self.current_score < Game.game_over_score):
            self.game_over = True

        self.total_score += self.current_score
        
        # Have we reached next checkpoint? If so, choose next one
        if self.checkpoint_reached(1, self.curr_checkpoint):
            print 'Checkpoint ', self.curr_checkpoint, ' reached!'
            self.total_score += Game.check_point_reached_score

            self.curr_checkpoint += 1
            if self.curr_checkpoint >= self.thetrack.get_num_checkpoints():
                self.end_time = pygame.time.get_ticks()
                lap_time = float((self.end_time - self.start_time)) / 1000.0
                print 'GOAL reached!!! Lap time: ', lap_time, 's'
                self.curr_lap_number += 1
                self.total_score += Game.lap_finished_score * self.curr_lap_number
                self.curr_checkpoint = 0
                self.start_time = pygame.time.get_ticks()

        
    # Set time resolution for simulation
    def set_time_res(self, resolution):
        time_res = resolution
        
    # Get current game score
    def get_score(self):
        car_distance = self.thetrack.distance_to_center(self.thecar.pos[x], self.thecar.pos[y])
        score = self.max_score - car_distance
        #score = score * (self.curr_checkpoint + 1) * (self.curr_lap_number + 1)
        #points are not for wimps, you gotta be moving to get some plus points!
        #print "Score: " + str(score) + " Speed: " + str(self.thecar.speed_kmh()) 
        if (score > 0 and self.thecar.speed_kmh() <= 5):
            score = score / 10
        return score / 5.0

    def get_track_side(self):
        side = self.thetrack.track_side(self.thecar.pos[x], self.thecar.pos[y])
        return side

    def get_total_score(self):
        return self.total_score

    def get_is_game_over(self):
        return self.game_over
        
    def print_debug(self):
        pass
        #print 'Current SCORE: ', self.get_score(), ' Side: ', self.get_track_side()
        #'  Checkpoint distance: ', \
        #        self.get_checkpoint_distance(1, self.curr_checkpoint)
        
    def get_checkpoint_distance(self, player, number):
        return self.thetrack.distance_to_checkpoint(self.thecar.pos[x], self.thecar.pos[y], number)
    
    def checkpoint_reached(self, player, number):
        if self.get_checkpoint_distance(player, number) < 100:
            return True
        else: return False
        
    def draw(self, screen):
        self.thetrack.draw(screen)
        self.thecar.draw(screen)

    
    
