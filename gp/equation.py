"""
@project: Pythai - Artificial Intellegence Project with Python
@package: Genetic Programming
@author: Timo Ruokonen (timoruokonen)
"""
import random
from literal import literal
from command import command

class equation:
    registered_equations = list()

    @staticmethod
    def register(operator, typeof):
        equation.registered_equations.append([operator, typeof])

    @staticmethod
    def generate(typeof):
        retval = equation()
        while(True):
            var = equation.registered_equations[random.randrange(len(equation.registered_equations))]
            #print "Comparing: " + str(var[1]) + " to " + str(typeof)
            if (var[1] == typeof):
                break
        retval.equation= var
        retval.left_side = equation.generate_side(typeof)
        retval.right_side = equation.generate_side(typeof)
        return retval

    @staticmethod
    def generate_side(typeof):
        source = random.randrange(2)
        if (source == 0):
            side = literal.generate(typeof)
        else:
            side = command.generate_with_type(typeof)
        return side

        
    def to_s(self):
        return "(" + self.left_side.to_s() + self.equation[0] + self.right_side.to_s() + ")"

