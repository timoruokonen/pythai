"""
@project: Pythai - Artificial Intellegence Project with Python
@package: Genetic Programming
@author: Timo Ruokonen (timoruokonen)
"""
import random
from literal import literal
from global_variable import global_variable

class command:
    '''
    Represents a command (function call) in the generated code. Commands can take parameters
    and have a return value. 
    '''

    registered_commands = list()

    @staticmethod
    def register(name, return_type, typeof, parameters, state_only):
        '''
        Static method for registering a new command type.

        Parameters:
            name - Name of the command. Must be the actual method/function name.
            return_type - The return type of the command, can be None.
            typeof - Type of the class that has this command. For example str. Type can be
            also None which means that command is executed in global namespace.
            parameters - Array of parameters that the command requires. Can be empty list.
            state_only - Is the command only about the state. If true, this command will no be
            used in the blocks where the actual commands are executed. It will only be used 
            in the equations. If false, this command can ne used in both places.
        '''
        command.registered_commands.append([name, return_type, typeof, parameters, state_only])
        print "Registered command: " + name

    @staticmethod
    def generate():
        '''
        Static method for generating a command instance. Generated command instance
        will be randomly selected from the all registered commands. Returns the generated
        command. 
        '''
        new_command = command()

        #Find a command that is not a status command
        while (True):
            new_command.command = command.registered_commands[random.randrange(len(command.registered_commands))]
            if (new_command.command[4] == False):
                break

        #create parameters to command if needed
        new_command.parameters = []
        if (len(new_command.command[3]) > 0):
            for param in new_command.command[3]:
                new_command.parameters.append(literal.generate(param))
        return new_command    

    @staticmethod
    def generate_with_type(typeof):
        '''
        Static method for generating a command with specific return type. The new generated
        command is randomly selected from all registered commands that have the given return
        type.
        '''
        new_command = command()
        while True:
            cmd = command.registered_commands[random.randrange(len(command.registered_commands))]
            if (cmd[1] == typeof):
                break
        new_command.command = cmd

        #create parameters to command if needed
        new_command.parameters = []
        if (len(new_command.command[3]) > 0):
            for param in new_command.command[3]:
                new_command.parameters.append(literal.generate(param))
        return new_command    
        
    def to_s(self):
        '''Returns the command as string (code). '''
        retval = ""
        #if object was given, add that to the call
        if (self.command[2] != None):
            variable = global_variable.generate(self.command[2])
            retval += variable.to_s() + "."
        retval += self.command[0] + '('
        #add parameters to the call
        first = True
        for param in self.parameters:
            if (first == False):
                retval += ', '
            else:
                first = False
            retval +=  param.to_s() 

        retval += ')'
        return retval

