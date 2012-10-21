"""
@project: Pythai - Artificial Intellegence Project with Python
@package: Genetic Programming
@author: Timo Ruokonen (timoruokonen)
"""
import random
from literal import literal
from command import command

class equation:
    '''
    Represents an equation in the code. Equation consists from the left side, an operator 
    and the right side. For example the following if statement contains two equations:
        if (a > 50 and b < a):
    '''

    registered_equations = list()

    @staticmethod
    def register(operator, typeof):
        '''
        Static method for registering a new equation type.
        Parameters:
            operator - Equation's operator as string, for example "<", ">", etc.
            typeof - Return type of the equation. 
        '''
        equation.registered_equations.append([operator, typeof])

    @staticmethod
    def generate(typeof):
        '''
        Static method for generating a new equation that returns the given type. The new
        equation instance is randomly selected from all the registered equations that have
        the given type as return type.
        '''
        retval = equation()
        while(True):
            var = equation.registered_equations[random.randrange(len(equation.registered_equations))]
            #print "Comparing: " + str(var[1]) + " to " + str(typeof)
            if (var[1] == typeof):
                break
        retval.equation= var
        retval.left_side = equation._generate_side(typeof)
        retval.right_side = equation._generate_side(typeof)
        return retval

    @staticmethod
    def _generate_side(typeof):
        '''Internal usage only.'''
        source = random.randrange(2)
        if (source == 0):
            side = literal.generate(typeof)
        else:
            side = command.generate_with_type(typeof)
        return side

        
    def to_s(self):
        '''Returns the equation as string (code).'''
        return "(" + self.left_side.to_s() + self.equation[0] + self.right_side.to_s() + ")"

