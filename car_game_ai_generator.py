from project import global_variable, literal, command, if_statement, code_generator 
import math
import car
import getopt
import sys
import time
import curses
import game
import pygame
from pygame.locals import *

# How many "codes" is generated during each generation
number_of_codes = 30
# How many game loops each generated code is executed
number_of_rounds = 500
# Show best code with graphics
show_best_graphics = True
# Show all generated codes
show_all_generated_code = False
# Set true/false whether to draw graphics or not
use_graphics = False
# Set true/false whether to simulate real time or not
use_realtime = False

print "Initializing game"
pygame.init()
#if (use_graphics):
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Pythai!')
pygame.key.set_repeat(1, 50)
white = 255, 255, 255
clock = pygame.time.Clock()
FPS = 30
thegame = game.Game()


def intialize_code_generator():
    global_variable.register("thegame", game.Game, [None], False)
    global_variable.register("thegame.get_car()", car.Car, [None], False)

    global_variable.register("thegame.get_score() > 0", bool, [None], False)
    global_variable.register("thegame.get_score() == 0", bool, [None], False)
    global_variable.register("thegame.get_score() < 0", bool, [None], False)
    global_variable.register("thegame.get_car().speed_kmh() <= 0", bool, [None], False)
    global_variable.register("thegame.get_car().speed_kmh() > 0", bool, [None], False)
    global_variable.register("thegame.get_car().speed_kmh() > 90", bool, [None], False)

    literal.register(1)        
    literal.register(0)        
    command.register(["accelerate", None, car.Car, []])
    command.register(["brake", None, car.Car, []])
    #command.register(["speed_kmh", None, car.Car, []])
    command.register(["steer_left", None, car.Car, []])
    command.register(["steer_right", None, car.Car, []])
    
    if_statement.register(bool);
    

def generate_code():
    #print "Generating Controlling Code:"
    generator = code_generator()
    generator.generate()
    code = generator.to_s()
    if (show_all_generated_code):
        print "-" * 40
        print code 
        print "-" * 40
    return code


def main(): 
    intialize_code_generator() 

    best_score = None
    best_code = None
    for i in range(number_of_codes):
        code = generate_code()
        score = do_simulation(code)
        if (i == 0 or score > best_score):
            best_score = score
            best_code = code
    print "Best score was: " + str(best_score)
    print "Best code was"
    print code
    if (show_best_graphics):
        print "showing best code graphically!"
        global use_graphics
        use_graphics = True
        do_simulation(best_code)
    
def draw_screen():
    screen.fill(white)
    thegame.draw(screen)
    pygame.display.flip()
    
def do_simulation(code):
    print "Starting simulation"
    global thegame
    thegame = game.Game()
    
    simulation_on = True
    thegame.set_car_throttle(10)
    simulation_rounds = 0

    while simulation_on and simulation_rounds < number_of_rounds:
        simulation_rounds += 1

        if use_realtime:
            clock.tick(FPS)

        thegame.advance()
        thegame.print_debug()
        
        if use_graphics:
            draw_screen()

        exec code

        if (thegame.get_is_game_over()):
            simulation_on = False

    print "Simulation ended"
    print "Resulting score: " + str(thegame.get_total_score())
    return thegame.get_total_score()
            

if __name__ == "__main__":
    main()

