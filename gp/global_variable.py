"""
@project: Pythai - Artificial Intellegence Project with Python
@package: Genetic Programming
@author: Timo Ruokonen (timoruokonen)
"""
import random
from gp import *

class global_variable:
    registered_global_variables = list()

    @staticmethod
    def register(name, typeof, value, init_needed):
        global_variable.registered_global_variables.append([name, typeof, value, init_needed])

    @staticmethod
    def generate(typeof):
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
        return self.variable[0]

