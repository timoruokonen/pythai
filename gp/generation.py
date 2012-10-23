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


class generation:
    '''
    Generation class controls a population of codes. After codes are added
    to the generation and all have been execued (and given a fitness value) the
    next generation can be generated based on the old one.

    The next generation is generated based on the gp settings found from the settings
    class. All codes must have a fittness value before getting the next generation. 
    '''
        
    def __init__(self):
        '''Creates a new empty code generation. '''
        self.generation = list()
        self.generation_number = 1

    @staticmethod
    def clear_logs():
        '''Clears the configured log files. See settings class for details.'''
        try:
            fileHandle = open (settings.log_best_codes_filename, 'w' )
            fileHandle.close()        
        except IOError as e:
            print 'Could not open ' + settings.log_best_codes_filename + " for logging"

    def add_code(self, code, moved_unchanged = False):
        '''Adds a code to the generation. 
        Parameters:
            code - Code to be added.
            moved_unchanged - Was the code moved unchanged. This can be used for optimizing the runs.
        '''
        code.set_moved_unchanged(moved_unchanged)
        self.generation.append(code)

    def get_generation_number(self):
        '''Returns the generation number (first generation is one and so on...) '''
        return self.generation_number

    def get_codes(self):
        '''Returns all the codes in the generation. List is unsorted. '''
        return self.generation

    def _select_with_tournament(self):
        '''
        Selects code candinate from the current generation with tournament. Tournament
        means taking certain amount of codes from the generation and selecing the best
        from those. Used internally.
        '''
        best = self.generation[random.randrange(len(self.generation))]
        for i in range(settings.tournament_size):
            best_candinate = self.generation[random.randrange(len(self.generation))]
            if code_compare(best, best_candinate) > 0:
                best = best_candinate
        return best
        
    def _log_best_codes(self, sorted_generation):
        '''Logs best codes of the generation. Used internally.'''
        try:
            fileHandle = open (settings.log_best_codes_filename, 'a' )
            fileHandle.write("Generation " + str(self.get_generation_number()) + " Best Scores:\n")
            for i in range(min(settings.log_best_codes_count, len(sorted_generation))):
                fileHandle.write("\t" + str(i) + ". result = " + str(sorted_generation[i].get_result()) + "\n")
            fileHandle.write(("-" * 40) +"\n")
            fileHandle.close()
        except IOError as e:
            print 'Could not open ' + settings.log_best_codes_filename + " for logging"

     
    def get_next_generation(self):
        '''
        Returns the next code generation based on the current generation.
        Note: All codes must have a fitness value before calling this.
        '''
        sorted_generation = sorted(self.generation, cmp=code_compare)
        if (settings.log_best_codes):
            self._log_best_codes(sorted_generation)

        next_generation = generation()
        next_generation.generation_number = self.generation_number + 1

        population = len(self.generation)
        
        #add best of the old generation "the king" always
        next_generation.add_code(sorted_generation[0], True)

        #add configured % of tournament winners directly
        for h in range(int(population * settings.best_programs_percentage / 100)):
            while (True):
                code_candinate = self._select_with_tournament()
                if ((code_candinate in next_generation.generation) == False):
                    next_generation.add_code(code_candinate, True)
                    break

        #merge configured % programs together
        for h in range(int(population * settings.crossover_percentage / 100)):
            next_generation.add_code(code_merger.merge(
                self._select_with_tournament(), self._select_with_tournament()))

        #then add rest with random branches
        left = population - len(next_generation.generation)
        for h in range(left):
            next_generation.add_code(code_merger.merge_with_random(self._select_with_tournament()))

        return next_generation

