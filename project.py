import random
import copy


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
 


class if_statement:
    registered_if_statements = list()
    maximumCommands = 4
    maximumEquationsPerCondition = 2
    maximumCodeDepth = 2

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
            if (next_equation == 0 or equation_count > if_statement.maximumEquationsPerCondition):
                break
            if (next_equation == 1):
                retval.condition += " and " +  equation.generate(retval.if_statement).to_s()
            if (next_equation == 2):
                retval.condition += " or " +  equation.generate(retval.if_statement).to_s()
            equation_count += 1

        #generate clauses inside the if block
        retval.commands = list()
        commands_count = 1 + random.randrange(if_statement.maximumCommands) 
        for i in range(commands_count):
            if (depth < if_statement.maximumCodeDepth and random.randrange(5) == 0):
                retval.commands.append(if_statement.generate(depth + 1))
            else:
                retval.commands.append(command.generate())

        #generate clauses for possible else block
        retval.else_commands = list()
        if (random.randrange(2) == 1):
            retval.else_condition = equation.generate(retval.if_statement)        
            for i in range(1 + random.randrange(if_statement.maximumCommands)):
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


class code_generator:
    maximumBlocks = 5

    def __init__(self):
        self.if_statements = list()
        self.result = None
    
    @staticmethod
    def generate():
        retval = code_generator()
        for i in range(1 + random.randrange(code_generator.maximumBlocks)):    
            retval.if_statements.append(if_statement.generate(1)) 
        return retval

    def get_random_branch(self):
        return self.if_statements[random.randrange(len(self.if_statements))]

    def replace_random_branch(self,branch):
        self.if_statements[random.randrange(len(self.if_statements))] = branch

    def to_s(self):
        retval = "";
        retval += global_variable.initial_definitions_to_s()
        for if_statement in self.if_statements:
            retval += if_statement.to_s()
            retval += "\n"
        return retval

    def set_result(self, result):
        self.result = result

    def get_result(self):
        return self.result


class code_merger:

    @staticmethod
    def merge(target_code, source_code):
        #get random branches from target code and replace those to the target code
        merged = copy.deepcopy(target_code)
        branch = source_code.get_random_branch()
        merged.replace_random_branch(branch)
        return merged

    @staticmethod
    def merge_with_random(code):
        merged = copy.deepcopy(code)
        branch = if_statement.generate(1)
        merged.replace_random_branch(branch)
        return merged

def code_compare(code1, code2):
    return int(code2.get_result() - code1.get_result())


#Code generation controls a population of codes. After codes are added
#to the generation and all have been execued (given fitness value) the
#next generation can be generated based on the old one.
class code_generation:
    #How many programs are taken into tournament when selecting candinates.
    tournament_size = 7
    
    #How many percentage of the best codes in the old generation are taken in to the
    #next generation through tournaments.
    best_programs_percentage = 10
    
    #How many percentage of the codes are crossfitted with each other (child codes).
    crossover_percentage = 85

    #Note: rest of the generation is filled with tournament winners with random new branches.

    def __init__(self):
        self.generation = list()

    def add_code(self, code):
        self.generation.append(code)

    def get_codes(self):
        return self.generation

    #Selects code candinate from the current generation with tournament. Tournament
    #means taking certain amount of codes from the generation and selecing the best
    #from those.
    def select_with_tournament(self):
        best = self.generation[random.randrange(len(self.generation))]
        for i in range(code_generation.tournament_size):
            best_candinate = self.generation[random.randrange(len(self.generation))]
            if code_compare(best, best_candinate) > 0:
                best = best_candinate
        return best 

    #Returns the next code generation based on the current generation.
    #Note: All codes must have a fitness value before calling this.
    def get_next_generation(self):
        sorted_generation = sorted(self.generation, cmp=code_compare)
        next_generation = code_generation()
        population = len(self.generation)
        
        #add best of the old generation "the king" always
        next_generation.add_code(sorted_generation[0])

        #add configured % of tournament winners directly
        for h in range(int(population * code_generation.best_programs_percentage / 100)):
            while (True):
                code_candinate = self.select_with_tournament()
                if ((code_candinate in next_generation.generation) == False):
                    next_generation.add_code(code_candinate)
                    break

        #merge configured % programs together
        for h in range(int(population * code_generation.crossover_percentage / 100)):
            next_generation.add_code(code_merger.merge(
                self.select_with_tournament(), self.select_with_tournament()))

        #then add rest with random branches
        left = population - len(next_generation.generation)
        for h in range(left):
            next_generation.add_code(code_merger.merge_with_random(self.select_with_tournament()))

        return next_generation


class dummy_class:
    @staticmethod
    def operation1(text):
        print "dummy_class: operation1 " + text
        return 1

    @staticmethod
    def operation2(number):
        print "dummy_calss: operation2 " + str(number)
        return 2

class project:

    def start(self):
        print "Starting..." 

        global_variable.register("fact1", bool, [True], True)
        global_variable.register("fact2", bool, [True], True)
        global_variable.register("lie", bool, [False], True)
        global_variable.register("dummy", dummy_class, None, True)
        literal.register("Kaljaa!!")
        literal.register("Kebabbia??")
        literal.register("Vodaa...?")
        literal.register("Jaloviinaa?")
        literal.register(1001)        
        literal.register(-50)
        equation.register("<", int)
        equation.register(">", int)
        equation.register("==", int)
        if_statement.register(int);
        command.register("operation1", int, dummy_class, [str])
        command.register("operation2", int, dummy_class, [int])
        command.register("print", None, None, [str])
        command.register("print", None, None, [int])

        print "Generating code for generation one:"
        generator = code_generator().generate()
        code = generator.to_s()
        print "Code:"
        print "-" * 40
        print code 
        print "-" * 40

        print "Executing code:"
        print "-" * 40
        exec code
        print "-" * 40

        merged = code_merger.merge(generator, generator)
        print "Merged Code:"
        print merged.to_s()


if __name__ == '__main__':
    print "This is the greatest project ever!"
    print "=" * 40
    proj = project()
    proj.start()

    
