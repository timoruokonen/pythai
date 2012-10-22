"""
@project: Pythai - Artificial Intellegence Project with Python
@package: Genetic Programming
@author: Timo Ruokonen (timoruokonen)
"""
import copy
import random
from if_statement import if_statement

class code_merger:
    '''Code merger class which is used to merge to instances of code class together.'''

    @staticmethod
    def merge(target_code, source_code):
        '''
        Merges target code with the source code so that the target will have one 
        randomly selected branch from the source. Merged code is returned. 
        
        Parameters:
            target_code - Target code block that will be used as the main code block
            after merge. 
            source_code - Source code from which a random branch is selected and merged 
            with target code.
        '''
        #get random branches from target code and replace those to the target code
        merged = copy.deepcopy(target_code)
        branch = source_code.get_random_branch()

        merged.replace_random_branch(branch)

        return merged

    @staticmethod
    def merge_with_random(code):
        '''
        Merges given code instance with a new random block that is generate. Merged
        code instance is returned.

        Parameters:
            code - Code block that is merged with a randomly generated branch.
        '''
        merged = copy.deepcopy(code)
        branch = if_statement.generate(1)
        merged.replace_random_branch(branch)
        return merged

