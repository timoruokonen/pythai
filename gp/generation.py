"""
@project: Pythai - Artificial Intellegence Project with Python
@package: Genetic Programming
@author: Timo Ruokonen (timoruokonen)
"""
import random
from settings import settings
from code import code
from code_merger import code_merger


def code_compare(code1, code2):
    return int(code2.get_result() - code1.get_result())


#Code generation controls a population of codes. After codes are added
#to the generation and all have been execued (given fitness value) the
#next generation can be generated based on the old one.
class generation:
    
    def __init__(self):
        self.generation = list()
        self.generation_number = 1

    @staticmethod
    def clear_logs():
        try:
            fileHandle = open (settings.log_best_codes_filename, 'w' )
            fileHandle.close()        
        except IOError as e:
            print 'Could not open ' + settings.log_best_codes_filename + " for logging"

    def add_code(self, code):
        self.generation.append(code)

    def get_generation_number(self):
        return self.generation_number

    def get_codes(self):
        return self.generation

    #Selects code candinate from the current generation with tournament. Tournament
    #means taking certain amount of codes from the generation and selecing the best
    #from those.
    def select_with_tournament(self):
        best = self.generation[random.randrange(len(self.generation))]
        for i in range(settings.tournament_size):
            best_candinate = self.generation[random.randrange(len(self.generation))]
            if code_compare(best, best_candinate) > 0:
                best = best_candinate
        return best
        
    def log_best_codes(self, sorted_generation):
        try:
            fileHandle = open (settings.log_best_codes_filename, 'a' )
            fileHandle.write("Generation " + str(self.get_generation_number()) + " Best Scores:\n")
            for i in range(min(settings.log_best_codes_count, len(sorted_generation))):
                fileHandle.write("\t" + str(i) + ". result = " + str(sorted_generation[i].get_result()) + "\n")
            fileHandle.write(("-" * 40) +"\n")
            fileHandle.close()
        except IOError as e:
            print 'Could not open ' + settings.log_best_codes_filename + " for logging"

     

    #Returns the next code generation based on the current generation.
    #Note: All codes must have a fitness value before calling this.
    def get_next_generation(self):
        sorted_generation = sorted(self.generation, cmp=code_compare)
        if (settings.log_best_codes):
            self.log_best_codes(sorted_generation)

        next_generation = generation()
        next_generation.generation_number = self.generation_number + 1

        population = len(self.generation)
        
        #add best of the old generation "the king" always
        next_generation.add_code(sorted_generation[0])

        #add configured % of tournament winners directly
        for h in range(int(population * settings.best_programs_percentage / 100)):
            while (True):
                code_candinate = self.select_with_tournament()
                if ((code_candinate in next_generation.generation) == False):
                    next_generation.add_code(code_candinate)
                    break

        #merge configured % programs together
        for h in range(int(population * settings.crossover_percentage / 100)):
            next_generation.add_code(code_merger.merge(
                self.select_with_tournament(), self.select_with_tournament()))

        #then add rest with random branches
        left = population - len(next_generation.generation)
        for h in range(left):
            next_generation.add_code(code_merger.merge_with_random(self.select_with_tournament()))

        return next_generation

