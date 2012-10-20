import random
from settings import settings
from equation import equation
from command import command

class if_statement:
    registered_if_statements = list()

    @staticmethod
    def register(typeof):
        if_statement.registered_if_statements.append(typeof)
        print "Registered if statement: " + str(typeof)

    @staticmethod
    def generate(depth):
        retval = if_statement()
        retval.depth = depth
        retval.if_statement = if_statement.registered_if_statements[random.randrange(len(if_statement.registered_if_statements))]

        #generate condition for the if clause
        retval.condition = equation.generate(retval.if_statement).to_s()
        equation_count = 1
        while (True):
            next_equation = random.randrange(3) 
            if (next_equation == 0 or equation_count > settings.maximumEquationsPerCondition):
                break
            if (next_equation == 1):
                retval.condition += " and " +  equation.generate(retval.if_statement).to_s()
            if (next_equation == 2):
                retval.condition += " or " +  equation.generate(retval.if_statement).to_s()
            equation_count += 1

        #generate clauses inside the if block
        retval.commands = list()
        commands_count = 1 + random.randrange(settings.maximumCommandsPerBlock) 
        for i in range(commands_count):
            if (depth < settings.maximumCodeDepth and random.randrange(5) == 0):
                retval.commands.append(if_statement.generate(depth + 1))
            else:
                retval.commands.append(command.generate())

        #generate clauses for possible else block
        retval.else_commands = list()
        if (random.randrange(2) == 1):
            retval.else_condition = equation.generate(retval.if_statement)        
            for i in range(1 + random.randrange(settings.maximumCommandsPerBlock)):
                retval.else_commands.append(command.generate())
            
        return retval
    
    def to_s(self):
        indent = ""
        for i in range(self.depth - 1):
            indent += "\t"

        ret = "\r" + indent + "if (" + self.condition + "):"
        for c in self.commands:
            ret += "\n\t" + indent + c.to_s()
        if (len(self.else_commands) > 0):
            ret += "\n" + indent + "elif(" + self.else_condition.to_s() + "):"
            for c in self.else_commands:
                ret += "\n\t" + indent + c.to_s()
        
        return ret

