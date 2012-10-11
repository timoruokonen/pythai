import random

class global_variable:
    registered_global_variables = list()

    @staticmethod
    def register(name, typeof):
        global_variable.registered_global_variables.append([name, typeof])

    @staticmethod
    def generate(typeof):
        while(True):
            var = global_variable.registered_global_variables[random.randrange(len(global_variable.registered_global_variables))]
            print "Comparing: " + str(var[1]) + " to " + str(typeof)
            if (var[1] == typeof):
                break
        return var[0]
        
    @staticmethod
    def to_s():
        retval = ""
        for variable in global_variable.registered_global_variables:
            #get the type as string from type
            print str(variable[1])
            retval += variable[0] + " = " + str(variable[1]).split(".")[1] + "()"
            retval += "\n"
        return retval


class literal:
    registered_literals = list()

    @staticmethod
    def register(new_literal):
        literal.registered_literals.append(new_literal)
        print "Registered literal: " + str(new_literal)

    @staticmethod
    def generate(typeof):
        while(True):
            lit = literal.registered_literals[random.randrange(len(literal.registered_literals))]
            #print "Comparing: " + str(type(lit)) + " to " + str(typeof)
            if (type(lit) == typeof):
                break
        new_literal = literal()
        new_literal.literal = lit
        return new_literal
    
    def to_s(self):
        if (type(self.literal) == str):
            return '"' + self.literal + '"' 
        else:
            return str(self.literal)

class command:
    registered_commands = list()

    @staticmethod
    def register(new_command):
        command.registered_commands.append(new_command)
        print "Registered command: " + new_command[0]

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
        
    def to_s(self):
        retval = ""
        #if object was given, add that to the call
        if (self.command[2] != None):
            variable = global_variable.generate(self.command[2])
            retval += variable + "."
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
 


class block:
    registered_blocks = list()
    maximumCommands = 5

    @staticmethod
    def register(new_block):
        block.registered_blocks.append(new_block)
        print "Registered block: " + new_block

    def __init__(self):
        self.block = block.registered_blocks[random.randrange(len(self.registered_blocks))]

        self.commands = list()
        for i in range(1 + random.randrange(block.maximumCommands)):
            self.commands.append(command.generate())
    
    def to_s(self):
        ret = self.block + ":"
        for c in self.commands:
            ret += "\n\t" + c.to_s()
        return ret


class code_generator:
    maximumBlocks = 2

    def __init__(self):
        self.blocks = list()

    def generate(self):
        for i in range(1 + random.randrange(code_generator.maximumBlocks)):    
            self.blocks.append(block()) 

    def to_s(self):
        retval = "";
        retval += global_variable.to_s()
        for block in self.blocks:
            retval += block.to_s()
            retval += "\n"
        return retval


class dummy_class:
    @staticmethod
    def operation1(text):
        print "dummy_class: operation1 " + text

    @staticmethod
    def operation2(number):
        print "dummy_calss: operation2 " + str(number)

class project:

    def start(self):
        print "Starting..." 

        gv1 = global_variable.register("dummy", dummy_class)

        literal.register("Kaljaa!!")
        literal.register("Kebabbia??")
        literal.register("Vodaa...?")
        literal.register("Jaloviinaa?")
        literal.register(1001)        
        block.register("if (True)");
        #block.register("if (False)");
        command.register(["print", None, None, [type("a")]])
        command.register(["print", None, None, [type(1)]])
        command.register(["operation1", None, dummy_class, [type("a")]])
        #command.register(["dummy.operation2", None, None, [type(1)]])

        print "Generating code for generation one:"
        generator = code_generator()
        generator.generate()
        code = generator.to_s()
        print "Code:"
        print "-" * 40
        print code 
        print "-" * 40

        print "Executing code:"
        print "-" * 40
        exec code
        print "-" * 40

if __name__ == '__main__':
    print "This is the greatest project ever!"
    print "=" * 40
    proj = project()
    proj.start()

    
