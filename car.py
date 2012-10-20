#!/usr/bin/env python
from __future__ import division
import math
from numpy  import *
import pygame
from decimal import Decimal

# Array position 0 is X
# Array position 1 is Y
x = 0
y = 1
# Air resistance (drag) constant
C_drag = 0.48
# Traction constant
C_traction = 12.8

pygame.init()

class Car:

    img = pygame.image.load("images/car_top_small.png")
    rect = img.get_rect()
    rect = rect.move([400, 500])
    max_throttle = float(10)
    max_brake = 10
    max_steer = 2
    DEBUG = True
    
    def __init__(self):
        self.max_power = float(4000) # N
        self.mass = float(1200) # kg

        self.max_brake_power = float(5000) # N
        self.throttle = float(0)
        self.brake_status = float(0)
        self.steer = float(0)
        
        self.fbrake = array([0,0], dtype=float)
        self.trac = array([0,0], dtype=float)
        self.acc = array([0,0], dtype=float) 
        self.vel = array([0,0], dtype=float)
        self.pos = array([400,500], dtype=float)
        self.rot = 0
        
        self.font = pygame.font.Font(None, 17)
        
    #
    # API calls for controlling the car
    #   
    def set_throttle(self, amount):
        #self.dprint('Setting throttle to ' + str(amount))
        self.throttle = amount
        
    def set_brake(self, amount):
        #self.dprint('Setting brake to ' + str(amount))
        self.brake_status = amount
    
    def set_steer(self, amount):
        self.steer = float(amount)

    def get_steer(self):
        return self.steer
       
    def accelerate(self):
        self.set_throttle(10)
        self.set_brake(0)
        
    def brake(self):
        self.set_throttle(0)
        self.set_brake(10)
        
    def steer_right(self):
        self.steer -= 0.40
        if self.steer < -self.max_steer:
            self.steer = -self.max_steer
            
    def steer_left(self):
        self.steer += 0.40
        if self.steer > self.max_steer:
            self.steer = self.max_steer
    
    def set_start_pos(self, xpos, ypos):
        self.pos[x] = xpos
        self.pos[y] = ypos
    #
    # Internal physics functions
    #
    def get_trac_power(self):
        rad = self.rot * math.pi / 180
        self.trac[y] = math.cos(rad)*(self.throttle / self.max_throttle) * float(self.max_power)
        self.trac[x] = -math.sin(rad)*(self.throttle / self.max_throttle) * float(self.max_power)
        return self.trac
    
    def get_drag(self):
        totaldrag = C_drag * math.pow(math.sqrt((self.vel[x]**2 + self.vel[y]**2)), 2)
        rad = self.rot * math.pi / 180
        drag_x = float(totaldrag*(-1)*math.sin(rad))
        drag_y = float(totaldrag*math.cos(rad))
        drag = array([-drag_x, -drag_y], dtype=float)
        return drag
    
    def get_roll(self):    
        totalroll = (C_traction * math.sqrt(self.vel[x]**2 + self.vel[y]**2))
        rad = self.rot * math.pi / 180
        roll_x = float(totalroll*(-1)*math.sin(rad))
        roll_y = float(totalroll*math.cos(rad))
        roll = array([-roll_x, -roll_y], dtype=float)
        return roll
    
    def get_brake_power(self):
        totalbrake = (self.brake_status / self.max_brake) * float(self.max_brake_power)
        rad = self.rot * math.pi / 180
        brake_x = float(totalbrake*(-1)*math.sin(rad))
        brake_y = float(totalbrake*math.cos(rad))
        brake = array([-brake_x, -brake_y], dtype=float)
        return brake;
    
    def get_abs_vel(self):
        return math.sqrt(self.vel[x]**2 + self.vel[y]**2)
        
    # Time passed in seconds
    def update_position(self, time):
        #print 'Trac: ', self.get_trac_power(), ' drag: ', self.get_drag(), ' roll: ', self.get_roll()
        f_total = self.get_trac_power() + self.get_drag() + self.get_roll()
        if (self.speed_kmh() > 1):
            f_total += self.get_brake_power()
            
        self.acc = (f_total / self.mass);       
        self.vel = self.vel + (float(time) * self.acc)
        rad = self.rot * math.pi / 180
        self.vel[x] = -math.sin(rad)*self.get_abs_vel()
        self.vel[y] = math.cos(rad)*self.get_abs_vel()
        dx = self.vel[x]
        dy = self.vel[y]
        self.pos[x] = self.pos[x] + (float(time) * dx * 10.0)
        self.pos[y] = self.pos[y] - (float(time) * dy * 10.0)
        if (self.speed_kmh() > 1):
            self.rot += self.steer
        
    def print_debug(self, screen):
        debugtext = 'Speed: ' + self.twodec(self.speed_kmh()) + 'kmh/h, vel: ' \
        + str(self.vel) + str(self.acc) + ', Pos: ' + str(self.pos) + ' (ESC to quit)'

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
        
    def twodec(self, dec):
        TWOPLACES = Decimal(10) ** -2
        return str(Decimal(dec).quantize(TWOPLACES))
        
    def speed_kmh(self):
        total_speed = math.sqrt(math.pow(self.vel[x], 2) + math.pow(self.vel[y], 2))
        return total_speed * 3.6

    def dprint(self, msg):
        if self.DEBUG == True:
            print msg
    
    def draw(self, screen):
        # RENDERING
        self.img = self.img.convert_alpha(screen)
        # TODO Rotatoi kaantoympyran keskipisteen mukaan
        rotated = pygame.transform.rotate(self.img, self.rot)
        # .. position the car on screen
        self.rect = rotated.get_rect()
        self.rect.center = self.pos
        # .. render the car to screen
        screen.blit(rotated, self.rect)
        
        #self.print_debug(screen)

         
