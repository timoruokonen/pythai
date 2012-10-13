#!/usr/bin/env python

import math
import car
import getopt
import sys
import time
import curses
import game
import pygame
from pygame.locals import *

# Set true/false whether to draw graphics or not
use_graphics = True
# Set true/false whether to simulate real time or not
use_realtime = True

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Pythai!')
pygame.key.set_repeat(1, 50)
thegame = game.Game()
white = 255, 255, 255
clock = pygame.time.Clock()
FPS = 30

def main():
    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit(0)
    # process arguments
    for arg in args:
        pass
    
    do_simulation()
    
def draw_screen():
    screen.fill(white)
    thegame.draw(screen)
    pygame.display.flip()
    
def do_simulation():
    simulation_on = True
    thegame.set_car_throttle(10)
    
    while simulation_on:
        if use_realtime:
            clock.tick(FPS)
            
        for event in pygame.event.get():
            if not hasattr(event, 'key'): continue
            down = event.type == KEYDOWN     # key down or up?
            if (down == False): continue
            if event.key == K_RIGHT:
                thegame.get_car().steer_right()
            elif event.key == K_LEFT:
                thegame.get_car().steer_left()
            elif event.key == K_UP:
                thegame.set_car_throttle(10)
                thegame.set_car_brake(0)
            elif event.key == K_DOWN:
                thegame.set_car_brake(10)
                thegame.set_car_throttle(0)
            elif event.key == K_f:
                screen = pygame.display.set_mode((800, 600), FULLSCREEN)
            elif event.key == K_e:
                screen = pygame.display.set_mode((800, 600))
            elif event.key == K_ESCAPE:
                screen = pygame.display.set_mode((800, 600))
                sys.exit(0)     # quit the game

            
        thegame.advance()
        thegame.print_debug()
        
        if use_graphics:
            draw_screen()

if __name__ == "__main__":
    #curses.wrapper(main)
    main()