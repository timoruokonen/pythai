import random
from literal import literal
from global_variable import global_variable

class command:
    registered_commands = list()

    @staticmethod
    def register(name, return_type, typeof, parameters):
        command.registered_commands.append([name, return_type, typeof, parameters])
        print "Registered command: " + name

    @staticmethod
    def generate():
        #create a new command and randomize its type
        new_command = command()
        new_command.command = command.registered_commands[random.randrange(len(command.registered_commands))]

        #create parameters to command if needed
        new_command.parameters = []
        if (len(new_command.command[3]) > 0):
            for param in new_command.command[3]:
                new_command.parameters.append(literal.generate(param))
        return new_command    

    @staticmethod
    def generate_with_type(typeof):
        #create a new command and randomize its type
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

