import copy
from if_statement import if_statement

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

