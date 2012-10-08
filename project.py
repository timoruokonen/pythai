class line:
    def __init__(self, msg):
        self.line = 'print "' + msg + '"' 
    
    def to_s(self):
        return self.line


class block:
    def __init__(self):
        line1 = line("Kaljaa!!")
        line2 = line("Kebabbia!!")
        self.lines = list()
        self.lines.append(line1)
        self.lines.append(line2) 
    
    def to_s(self):
        ret = "if (True):"
        for line in self.lines:
            ret += "\n\t" + line.to_s()
        return ret


class code_generator:
    def __init__(self):
        self.blocks = block()

    def generate(self):
        return self.blocks.to_s() 

class project:

    def start(self):
        print "Starting..." 
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

    
