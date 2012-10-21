"""
@project: Pythai - Artificial Intellegence Project with Python
@package: Genetic Programming
@author: Timo Ruokonen (timoruokonen)
"""
import random

class literal:
    '''
    Represents a literal in the code. Literals have a type and value.
    Example literals: 1, 0.57, "Kalja"
    '''

    registered_literals = list()

    @staticmethod
    def register(new_literal):
        '''
        Static method for registering a new literal.

        Parameters:
            new_literal - Literals value and type.
        '''
        literal.registered_literals.append(new_literal)
        print "Registered literal: " + str(new_literal)

    @staticmethod
    def generate(typeof):
        '''
        Static method for generating a literal instance with given type. The new literal
        instance is selected randomly from the registered literals that have the given
        type.

        Parameters:
            typeof - Type of the literal to be created.
        '''
        while(True):
            lit = literal.registered_literals[random.randrange(len(literal.registered_literals))]
            #print "Comparing: " + str(type(lit)) + " to " + str(typeof)
            if (type(lit) == typeof):
                break
        new_literal = literal()
        new_literal.literal = lit
        return new_literal
    
    def to_s(self):
        '''Returns the literal as string (code). '''
        if (type(self.literal) == str):
            return '"' + self.literal + '"' 
        else:
            return str(self.literal)

