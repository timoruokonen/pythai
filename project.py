import random


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
 


class if_statement:
    registered_if_statements = list()
    maximumCommands = 5

    @staticmethod
    def register(typeof):
        if_statement.registered_if_statements.append(typeof)
        print "Registered if statement: " + str(typeof)

    @staticmethod
    def generate():
        retval = if_statement()
        retval.if_statement = if_statement.registered_if_statements[random.randrange(len(if_statement.registered_if_statements))]

        #generate condition for the if clause
        retval.condition = global_variable.generate(retval.if_statement)

        #generate clauses inside the if block
        retval.commands = list()
        for i in range(1 + random.randrange(if_statement.maximumCommands)):
            retval.commands.append(command.generate())

        #generate clauses for possible else block
        retval.else_commands = list()
        if (random.randrange(2) == 1):
            retval.else_condition = global_variable.generate(retval.if_statement)        
            for i in range(1 + random.randrange(if_statement.maximumCommands)):
                retval.else_commands.append(command.generate())
            
        return retval
    
    def to_s(self):
        ret = "if (" + self.condition.to_s() + "):"
        for c in self.commands:
            ret += "\n\t" + c.to_s()
        if (len(self.else_commands) > 0):
            ret += "\nelif(" + self.else_condition.to_s() + "):"
            for c in self.else_commands:
                ret += "\n\t" + c.to_s()
        
        return ret


class code_generator:
    maximumBlocks = 5

    def __init__(self):
        self.if_statements = list()

    def generate(self):
        for i in range(1 + random.randrange(code_generator.maximumBlocks)):    
            self.if_statements.append(if_statement.generate()) 

    def to_s(self):
        retval = "";
        retval += global_variable.initial_definitions_to_s()
        for if_statement in self.if_statements:
            retval += if_statement.to_s()
            retval += "\n"
        return retval

class code_merger:
    def merge(self, code1, code2):
        return code1



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

        global_variable.register("fact1", bool, [True], True)
        global_variable.register("fact2", bool, [True], True)
        global_variable.register("lie", bool, [False], True)
        global_variable.register("dummy", dummy_class, None, True)
        command.register(["operation1", None, dummy_class, [str]])
        command.register(["operation2", None, dummy_class, [int]])

        literal.register("Kaljaa!!")
        literal.register("Kebabbia??")
        literal.register("Vodaa...?")
        literal.register("Jaloviinaa?")
        literal.register(1001)        
        if_statement.register(bool);
        command.register(["print", None, None, [str]])
        command.register(["print", None, None, [int]])

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

        merger = code_merger()
        merged = merger.merge(generator, generator)
        print "Merged Code:"
        print merged.to_s()


if __name__ == '__main__':
    print "This is the greatest project ever!"
    print "=" * 40
    proj = project()
    proj.start()

    
