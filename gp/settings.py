"""
@project: Pythai - Artificial Intellegence Project with Python
@package: Genetic Programming
@author: Timo Ruokonen (timoruokonen)
"""

class settings:
    '''
    Global settings for genetic programming. All classes inside the gp package use
    these values.
    '''

    '''How many commands there can be in total inside one block.'''
    maximumCommandsPerBlock = 4

    '''How many equations one condition (in if clause) can have.'''
    maximumEquationsPerCondition = 2

    '''How many inner if clauses there can be. Be carefull with this...'''
    maximumCodeDepth = 2

    '''How many blocks in total the code can have.'''
    maximumBlocks = 5

    '''How many programs are taken into tournament when selecting candinates.'''
    tournament_size = 7

    '''
    How many percentage of the best codes in the old generation are taken in to the
    next generation through tournaments.
    '''
    best_programs_percentage = 10
    
    '''
    How many percentage of the codes are crossfitted with each other (child codes).
    Note: rest of the generation is filled with tournament winners with random new branches.
    '''
    crossover_percentage = 85

    '''Log best codes to a file after each generation.'''
    log_best_codes = True

    '''How many best codes are logged per generation (if logging is enabled).'''
    log_best_codes_count = 5

    '''The log file for best codes (if enabled). '''
    log_best_codes_filename = "best_codes.txt"


