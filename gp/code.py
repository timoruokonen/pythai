"""
@project: Pythai - Artificial Intellegence Project with Python
@package: Genetic Programming
@author: Timo Ruokonen (timoruokonen)
"""
import random
import copy
from settings import settings
from global_variable import global_variable
from if_statement import if_statement


class code:
    '''
    The class C{code} represents a block of code with defined global variables and possible multiple 
    inner blocks. The whole contents is generated based on the registered code parts (global_variable,
    literal, equation, command, if_statement).

    Generated code will be in the following format:
    1. Global variables
    2. List of if_statement blocks (that can have inner if_statement blocks)
    '''

    def __init__(self):
        '''Creates a new empty code instance. This method should not be used to generate code
        instances. Use static method generate instead.'''
        self.if_statements = list()
        self.result = None
        self.was_moved_unchanged = False
    
    @staticmethod
    def generate():
        '''Static method for generating a new code block. Creates and returns a new code block
        that is generated based on the registered code parts.'''
        retval = code()
        for i in range(1 + random.randrange(settings.maximumBlocks)):    
            retval.if_statements.append(if_statement.generate(1)) 
        return retval

    def get_random_branch(self):
        '''
        Returns a copy of random branch (if_statement) from the current code instance. The
        returned branch can be from any depth.
        '''
        branch = self.if_statements[random.randrange(len(self.if_statements))]
        branches = branch.get_all_branches()
        sub_branch = copy.deepcopy(branches[random.randrange(len(branches))])
        return sub_branch
        

    def replace_random_branch(self,branch):
        '''
        Replaces a randomly selected branch from the current code instance and replaces
        it with a random branch. The randomly selected branch that is replaced can be from
        any depth.

        Parameters:
            branch - Branch that is replaced to randomly selected branch of the current code.
        '''
        #first get random main if_statement branch
        target_branch_index = random.randrange(len(self.if_statements)) 
        #next get random sub branch from the main branch and do not make a copy of it!
        branches = self.if_statements[target_branch_index].get_all_branches()
        sub_branch = branches[random.randrange(len(branches))]

        sub_branch.assign(branch)

    def to_s(self):
        '''Returns the code block instance as "real code" string. This method is used to execute the
        generated code and for storing the results.'''
        retval = "";
        retval += global_variable.initial_definitions_to_s()
        for if_statement in self.if_statements:
            retval += if_statement.to_s()
            retval += "\n"
        return retval

    def set_result(self, result):
        '''
        Sets the result (fitness) of the generated code. This information is used when the next
        code generation is generated. It should be set for each code block in the generation. 

        Parameters:
            result - Result (fitness) of the code.
        '''
        self.result = result

    def get_result(self):
        '''Gets the result (fitness) for this code instance. '''
        return self.result

    def set_moved_unchanged(self, unchanged):
        '''
        Sets the property indicating wether the code was moved from the previous generation
        unchanged to the current generation. This property can be used for optimizing the runs
        if the domain does not change between different runs.

        Parameters:
            unchanged - Was the code moved unchanged from the previous generation.
        '''
        self.was_moved_unchanged = unchanged

    def get_moved_unchanged(self):
        '''Returns wether the code was moved unchanged from the previous generation to the current.'''
        return self.was_moved_unchanged

