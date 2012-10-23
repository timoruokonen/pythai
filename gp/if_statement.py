"""
@project: Pythai - Artificial Intellegence Project with Python
@package: Genetic Programming
@author: Timo Ruokonen (timoruokonen)
"""
import random
from settings import settings
from equation import equation
from command import command

class if_statement:
    '''
    Represents an if statement in the code. If statement can consists of multiple equations,
    else blocks and each of those can have inner if statements. Each block contains commands. The number
    of equations, commands, maximum block depth can be configured from the gp settings.

    Example if statement:
        if (equation1 and equation2):
            if (equation3):
                command1()
                command2()
            elif (equation4 or equation5 and equation6):
                command12()
    '''
    registered_if_statements = list()

    @staticmethod
    def register(typeof):
        '''
        Static method for registering an if statement.

        Parameters:
            typeof - If statements "compared to" type. For example int would produce if statements
            that have equations returning integers.
        '''
        if_statement.registered_if_statements.append(typeof)
        print "Registered if statement: " + str(typeof)

    @staticmethod
    def generate(depth):
        '''
        Static method for generating a new if statement. 

        Parameters:
            depth - The current code depth. Gp settings have a setting for maximum code depth.
        '''
        retval = if_statement()
        retval.depth = depth
        retval.if_statement = if_statement.registered_if_statements[random.randrange(len(if_statement.registered_if_statements))]

        #generate condition for the if clause
        retval.condition = equation.generate(retval.if_statement).to_s()
        equation_count = 1
        while (True):
            next_equation = random.randrange(3) 
            if (next_equation == 0 or equation_count >= settings.maximumEquationsPerCondition):
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
    
    def get_all_branches(self):
        '''Gets all sub branches (if statements) including the main branch of this if statement instance. '''
        branches = list()
        branches.append(self)
        for branch in self.commands:
            if isinstance(branch, if_statement):
                branches += branch.get_all_branches()
        return branches

    def get_depth(self):
        '''Returns the depth of the if statement. '''
        return self.depth
    
    def set_depth(self, depth):
        '''Sets depth to this instance and all its sub branches. '''
        self.depth = depth
        for branch in self.commands:
            if isinstance(branch, if_statement):
                branch.set_depth(depth + 1)

    def assign(self, branch):
        '''
        Assigns another if statement instance to the current instance. 

        Parameters:
            branch - if_statement instance that is set to this instance.
        '''
        branch.set_depth(self.depth)
        self.condition = branch.condition
        self.commands = branch.commands
        #A bit lame but else command list always exists but else condition does not if there is no
        #else branch... TODO: Improve.
        self.else_commands = branch.else_commands
        if (len(branch.else_commands) > 0):
            self.else_condition = branch.else_condition 
     
    def to_s(self):
        '''
        Returns the if statement as string (code) including all the inner blocks
        of the if statement.
        '''
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

