"""
@project: Pythai - Artificial Intellegence Project with Python
@package: Genetic Programming
@author: Timo Ruokonen (timoruokonen)
"""
import random
from gp import *

class global_variable:
    '''
    Represents a global variable (or any variable that the commands can use). Global variable
    can be set to be declared in the beginning of the code or not.
    '''

    registered_global_variables = list()

    @staticmethod
    def register(name, typeof, value, init_needed):
        '''
        Static method for registering a new global variable.

        Parameters:
            name - Name of the global variable. The name is used every time the variable is
            referenced.
            typeof - Type of the variable. The type is used when code generator wants a specific
            type of input to be generated.
            value - Initial value of the variable. Has no effect if init_needed is false.
            init_needed - If true, the code block will assign the given value to the variable
            in the beginning of the code. If false, variable will not be assigned or introduced.
        '''
        global_variable.registered_global_variables.append([name, typeof, value, init_needed])

    @staticmethod
    def generate(typeof):
        '''
        Static method for generating a global variable with given type. The new variable will be
        randomly selected from the registered variables that have the given type.
        '''
        retval = global_variable()
        while(True):
            var = global_variable.registered_global_variables[random.randrange(len(global_variable.registered_global_variables))]
            #print "Comparing: " + str(var[1]) + " to " + str(typeof)
            if (var[1] == typeof):
                break
        retval.variable = var
        return retval
        
    @staticmethod
    def initial_definitions_to_s():
        '''
        Static method that returns all the initial assigment for all registered global
        variables.
        '''
        retval = ""
        for variable in global_variable.registered_global_variables:
            if (variable[3] == False):
                continue

            #get the type as string from type
            if (str(variable[1]).find("'")) > 0:
                #python basic types are in form of <type 'bool'>
                retval += variable[0] + " = " + str(variable[1]).split("'")[1] + "("
            else:
                #user types are python basic types <module.type>            
                retval += variable[0] + " = " + str(variable[1]).split(".")[1] + "("
            
            #if initial constructor parameters were given, set those
            if (variable[2] != None):
                first = True
                for parameter in variable[2]:
                    if first == False:
                        retval += ","
                    first = False
                    retval += str(parameter)
            retval += ")\n"
        return retval

    def to_s(self):
        '''Returns the global variable as string (code).'''
        return self.variable[0]

