import random

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

