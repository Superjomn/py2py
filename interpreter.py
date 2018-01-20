class Interpreter:
    def __init__(self):
        self.stack = []
        self.env = {}

    def STORE_NAME(self, name):
        val = self.stack.pop()
        self.env[name] = val

    def LOAD_VALUE(self, val):
        self.stack.append(val)

    def LOAD_NAME(self, name):
        val = self.env[name]
        self.stack.append(val)

    def ADD_TWO(self):
        val0 = self.stack.pop()
        val1 = self.stack.pop()
        self.stack.append(val0 + val1)

    def PRINT_VALUE(self):
        val = self.stack.pop()
        print val

    def parse_argument(self, instruction, argument, what_to_execute):
        '''
        What is argument?
        '''
        numbers = set(["LOAD_VALUE"])
        names = set(["LOAD_NAME", "STORE_NAME"])

        # argument: index or key
        if instruction in numbers:
            argument = what_to_execute["numbers"][argument]
        elif instruction in names:
            argument = what_to_execute["names"][argument]
        return argument

    def execute(self, what_to_execute):
        instructions = what_to_execute["instructions"]
        for step in instructions:
            instruction, argument = step
            argument = self.parse_argument(instruction, argument, what_to_execute)
            bytecode_method = getattr(self, instruction)
            if argument is None:
                bytecode_method()
            else:
                bytecode_method(argument)

if __name__ == '__main__':
    '''
    a = 1
    b = 2
    c = a + b
    print c
    '''

    instructions = {
        "instructions": [
            ("LOAD_VALUE", 0),
            ("LOAD_VALUE", 1),
            ("ADD_TWO", None),
            ("PRINT_VALUE", None),],
        "numbers": [7, 5],
    }

    ins = Interpreter()
    ins.execute(instructions)
