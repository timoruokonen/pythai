#!/usr/bin/env python
import car
import math
import track
import pygame
from globals import *

class Game:
    checkpoint_reach_tolerance = 130
    game_over_score = -500.0
    game_over_distance = 400
    max_score = 100.0
    check_point_reached_score = 8000.0
    lap_finished_score = 100000.0
    # Time resolution in seconds
        
    def __init__(self):
        self.time_res = 1/30.0
        self.time = 0.0
        self.thecar = car.Car()
        self.thetrack = track.Track()    
        self.curr_checkpoint = 0
        self.curr_lap_number = 0
        self.thecar.set_start_pos(110,300)
        self.start_time = pygame.time.get_ticks()
        self.total_score = 0.0
        self.game_over = False
        self.current_score = 0.0

        self.font = pygame.font.Font(None, 20)
    
    def set_car_throttle(self, amount):
        self.thecar.set_throttle(amount)
        
    def set_car_brake(self, amount):
        self.thecar.set_brake(amount)
        
    def set_car_steer(self, amount):
        self.thecar.set_steer(amount)
        
    def get_car(self):
        return self.thecar

    def set_game_over(self):
        self.game_over = True
        print 'Game over!'
        
    # Advance game simulation
    def advance(self):
        self.time += self.time_res
        self.thecar.update_position(self.time_res)

        #optimize by calculating and storing values to self
        self.distance_to_center = self.thetrack.distance_to_center(self.thecar.pos[x], self.thecar.pos[y])
        self.checkpoint_distance = self.thetrack.distance_to_checkpoint(self.thecar.pos[x], self.thecar.pos[y], self.curr_checkpoint) 
        self.track_side = self.thetrack.track_side(self.thecar.pos[x], self.thecar.pos[y])
         

        self.current_score = self.get_score() 
        if (self.total_score < Game.game_over_score):
            self.set_game_over()

        if (self.distance_to_center > Game.game_over_distance):
            self.set_game_over()

        self.total_score += self.current_score
        
        # Have we reached next checkpoint? If so, choose next one
        if self.checkpoint_reached(1, self.curr_checkpoint):
            self.print_current_time('Checkpoint ' + str(self.curr_checkpoint) + ' reached!')
            #give points based on how closely the checkpoint was reached 
            tol_percentage = (Game.checkpoint_reach_tolerance - self.checkpoint_distance) / Game.checkpoint_reach_tolerance
            self.total_score += (1 + tol_percentage) * Game.check_point_reached_score
            self.curr_checkpoint += 1

            if self.curr_checkpoint >= self.thetrack.get_num_checkpoints():
                self.end_time = pygame.time.get_ticks()
                lap_time = float((self.end_time - self.start_time)) / 1000.0
                self.print_current_time('GOAL reached!!!')
                self.curr_lap_number += 1
                self.total_score += Game.lap_finished_score * self.curr_lap_number
                self.curr_checkpoint = 0
                self.start_time = pygame.time.get_ticks()

        
    def print_current_time(self, remark):
        current_real_time = float((pygame.time.get_ticks() - self.start_time)) / 1000.0
        print remark, ' Real time: ', twodec(current_real_time), 's  Simulation time: ', twodec(self.time), 's'

    # Set time resolution for simulation
    def set_time_res(self, resolution):
        time_res = resolution
        
    # Get current game score
    def get_score(self):
        # You get points for being close to track center
        # but being offroad will drop points in factor of 2
        score = self.max_score
        score -= 0.02 * (self.distance_to_center ** 2.0)
        # Closer to next checkpoint will gain more points
        score -= self.checkpoint_distance / 4.3
        #score = score * (self.curr_checkpoint + 1) * (self.curr_lap_number + 1)
        #points are not for wimps, you gotta be moving to get some plus points!
        #even more, punish the still-standing car, and award for speed!
        #print "Score: " + str(score) + " Speed: " + str(self.thecar.speed_kmh()) 
        
        if (score > 0 and self.thecar.speed_kmh() <= 3):
            score = score / 10
            score = score - 100
        else:
            score = score + (self.thecar.speed_kmh() / 2.0)
        
        return score / 5.0

    def get_track_side(self):
        return self.track_side

    def get_total_score(self):
        #Don't let the bad end ruin the whole game. At least give half of the points gathered
        #from checkpoints and laps...
        if (self.curr_lap_number > 0 or self.curr_checkpoint > 0): 
            points_from_checkpoints = self.curr_lap_number * (Game.lap_finished_score + self.curr_lap_number * Game.check_point_reached_score * self.thetrack.get_num_checkpoints()) + self.curr_checkpoint * Game.check_point_reached_score
            return max(self.total_score, points_from_checkpoints / 2)

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
        if self.checkpoint_distance < Game.checkpoint_reach_tolerance:
            return True
        return False
        
    def draw(self, screen):
        self.thetrack.draw(screen)
        self.thecar.draw(screen)
        self.print_debug_onscreen(screen)

    def print_debug_onscreen(self, screen):
        debugtext = 'Score: ' + twodec(self.current_score) + '  Total: ' \
        + twodec(self.total_score) + ' (ESC to quit)'

        # Render the text
        text = self.font.render(debugtext, True, (0,
        0, 0), (200, 200, 200))

        # Create a rectangle
        textRect = text.get_rect()

        # Center the rectangle
        textRect.centerx = 400
        textRect.centery = 10

        # Blit the text
        screen.blit(text, textRect)

    
    
