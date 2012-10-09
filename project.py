import random

class literal:
    registered_literals = list()

    @staticmethod
    def register_literal(new_literal):
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
    def register_command(new_command):
        command.registered_commands.append(new_command)
        print "Registered command: " + new_command[0]

    @staticmethod
    def generate():
        #create a new command and randomize its type
        new_command = command()
        new_command.command = command.registered_commands[random.randrange(len(command.registered_commands))]

        #create parameters to command if needed
        new_command.parameters = []
        if (len(new_command.command[2]) > 0):
            for param in new_command.command[2]:
                new_command.parameters.append(literal.generate(param))
        return new_command    
        
    def to_s(self):
        retval = self.command[0] + '('
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

    @staticmethod
    def register_block(new_block):
        block.registered_blocks.append(new_block)
        print "Registered block: " + new_block

    def __init__(self):
        self.block = block.registered_blocks[random.randrange(len(self.registered_blocks))]

        self.commands = list()
        self.commands.append(command.generate())
        self.commands.append(command.generate())
        self.commands.append(command.generate())
    
    def to_s(self):
        ret = self.block + ":"
        for c in self.commands:
            ret += "\n\t" + c.to_s()
        return ret


class code_generator:
    def __init__(self):
        self.blocks = block()

    def generate(self):
        return self.blocks.to_s() 

class project:

    def start(self):
        print "Starting..." 

        literal.register_literal("Kaljaa!!")
        literal.register_literal("Kebabbia??")
        literal.register_literal(1001)        
        block.register_block("if (True)");
        block.register_block("if (False)");
        command.register_command(["print", None, [type("a")]])
        command.register_command(["print", None, [type(1)]])

        print "Generating code for generation one:"
        generator = code_generator()
        code = generator.generate()
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

    
