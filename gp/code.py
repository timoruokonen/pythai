"""
@project: Pythai - Artificial Intellegence Project with Python
@package: Genetic Programming
@author: Timo Ruokonen (timoruokonen)
"""
import random
from settings import settings
from global_variable import global_variable
from if_statement import if_statement

class code:

    def __init__(self):
        self.if_statements = list()
        self.result = None
    
    @staticmethod
    def generate():
        retval = code()
        for i in range(1 + random.randrange(settings.maximumBlocks)):    
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

