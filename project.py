import random
import copy
import gp

class dummy_class:
    @staticmethod
    def do_stuff(text):
        print "dummy_class: do stuff " + text
        return 1

    @staticmethod
    def get_state(number):
        print "dummy_calss: get_state " + str(number)
        return 2

class project:

    def start(self):
        print "Starting..." 

        gp.global_variable.register("fact1", bool, [True], True)
        gp.global_variable.register("fact2", bool, [True], True)
        gp.global_variable.register("lie", bool, [False], True)
        gp.global_variable.register("dummy", dummy_class, None, True)
        gp.literal.register("Kaljaa!!")
        gp.literal.register("Kebabbia??")
        gp.literal.register("Vodaa...?")
        gp.literal.register("Jaloviinaa?")
        gp.literal.register(1001)        
        gp.literal.register(-50)
        gp.equation.register("<", int)
        gp.equation.register(">", int)
        gp.equation.register("==", int)
        gp.if_statement.register(int);
        gp.command.register("do_stuff", int, dummy_class, [str], False)
        gp.command.register("get_state", int, dummy_class, [int], True)
        gp.command.register("print", None, None, [str], False)
        gp.command.register("print", None, None, [int], False)

        print "Generating code for generation one:"
        generator = gp.code.generate()
        code = generator.to_s()
        print "Code:"
        print "-" * 40
        print code 
        print "-" * 40

        print "Executing code:"
        print "-" * 40
        exec code
        print "-" * 40

        generation = gp.generation()
        generation.add_code(generator)
        generation.get_next_generation()

if __name__ == '__main__':
    print "This is the greatest project ever!"
    print "=" * 40
    proj = project()
    proj.start()

    
