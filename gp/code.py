"""
@project: Pythai - Artificial Intellegence Project with Python
@package: Genetic Programming
@author: Timo Ruokonen (timoruokonen)
"""
import random
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
    
    @staticmethod
    def generate():
        '''Static method for generating a new code block. Creates and returns a new code block
        that is generated based on the registered code parts.'''
        retval = code()
        for i in range(1 + random.randrange(settings.maximumBlocks)):    
            retval.if_statements.append(if_statement.generate(1)) 
        return retval

    def get_random_branch(self):
        '''Returns a random branch from the current code instance. '''
        return self.if_statements[random.randrange(len(self.if_statements))]

    def replace_random_branch(self,branch):
        '''
        Replaces a randomly selected branch from the current code instance and replaces
        it with a random branch.

        Parameters:
            branch - Branch that is replaced to randomly selected branch of the current code.
        '''
        self.if_statements[random.randrange(len(self.if_statements))] = branch

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

