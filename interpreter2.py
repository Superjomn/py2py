import sys
'''
A lisp interpreter

(+ 1 2)

(if (> 2 1) ... ...)
'''


class Block(object):
    def __init__(self, codes):
        '''
        the instructions should be pushed to code_stack, the
        data stack should be shared.
        '''
        self.codes = codes


class VirtualMachine(object):
    '''
    run codes, and if get a function call, create a frame and push to
    frame stack.
    '''

    def __init__(self):
        self.frame_stack = []
        self.functions = {}

    def make_frame(self, func):
        frame = Frame(self.functions[func].codes)


class Function:
    def __init__(self, codes, vm):
        self.codes = codes
        self.frame = frame

    def run(self):
        pass


class Tokenizer(object):
    def __init__(self):
        self.binary_ops = [
            '+',
            '-',
            '*',
            '/',
            '=',
        ]

        self.cmp_ops = [
            '>',
            '<',
            '>=',
            '<=',
            '==',
        ]

        self.ops = {
            '+': 'ADD_TWO',
            '-': 'SUB_TWO',
            '*': 'MUL_TWO',
            '/': 'DIV_TWO',
            '=': 'STORE_TO',
            '>': 'GT',
            '<': 'LT',
            '>=': 'GE',
            '<=': 'LE',
            '==': 'EQ',
        }

    def parse(self, lines):
        codes = []
        for line in lines:
            words = line.strip().split()

            if len(words) == 5:
                '''
                c = a + b
                '''
                target, op0, arg0, op1, arg2 = words
                codes += [('LOAD_FAST', arg1), ('LOAD_FAST', arg2),
                          (self.ops[op1], )('LOAD_CONST',
                                            target), (self.ops[op0], )]
            elif len(words) == 2:
                codes += [
                    ('LOAD_CONST', words[1]),
                    ('LOAD_FAST', ),
                    ('PRINT_VAL', ),
                ]
        return codes

    def is_str(self, w):
        return "'" in w or '"' in w

    def is_True(self, w):
        return w == 'true'

    def is_false(self, w):
        return w == 'false'

    def is_digit(self, w):
        return not self.is_str(w) and w != 'None' and w.isdigit()

    def is_op(self, w):
        return w in self.ops

    def is_var(self, w):
        return not self.is_str(w)


class Frame(object):
    def __init__(self, args, globals):
        '''
        :param globals: dict
        LOAD_FAST will load the variable from globals to data stack

        args: list of arguments
        globals: a dict
        '''
        self.args = args
        self.globals = globals
        self.locals = {}

        self.data_stack = []

    def LOAD_FAST(self):
        arg = self.data_stack.pop()
        if type(arg) is int:
            self.data_stack.append(self.args[arg])
        else:
            self.data_stack.append(self.globals[arg])

    def LOAD_CONST(self):
        pass

    def ADD_TWO(self):
        arg0 = self.data_stack.pop()
        arg1 = self.data_stack.pop()
        self.data_stack.append(arg0 + arg1)

    def SUB_TWO(self):
        arg0 = self.data_stack.pop()
        arg1 = self.data_stack.pop()
        self.data_stack.append(arg0 - arg1)

    def MUL_TWO(self):
        arg0 = self.data_stack.pop()
        arg1 = self.data_stack.pop()
        self.data_stack.append(arg0 * arg1)

    def DIV_TWO(self):
        arg0 = self.data_stack.pop()
        arg1 = self.data_stack.pop()
        self.data_stack.append(arg0 / arg1)

    def STORE_TO(self):
        arg0 = self.data_stack.pop()
        arg1 = self.data_stack.pop()
        self.locals[arg1] = arg0

    def GT(self):
        arg0 = self.data_stack.pop()
        arg1 = self.data_stack.pop()
        self.data_stack.append(arg0 > arg1)

    def GE(self):
        arg0 = self.data_stack.pop()
        arg1 = self.data_stack.pop()
        self.data_stack.append(arg0 >= arg1)

    def LT(self):
        arg0 = self.data_stack.pop()
        arg1 = self.data_stack.pop()
        self.data_stack.append(arg0 < arg1)

    def LE(self):
        arg0 = self.data_stack.pop()
        arg1 = self.data_stack.pop()
        self.data_stack.append(arg0 <= arg1)

    def EQ(self):
        arg0 = self.data_stack.pop()
        arg1 = self.data_stack.pop()
        self.data_stack.append(arg0 == arg1)

    def PRINT_VAL(self):
        arg = self.data_stack.pop()
        print "res: ", arg

    def run_code(self, codes):
        '''
        run blocks in the block_stack, and

        code:

        c = a + b

        LOAD_CONSTANT 'a'
        LOAD_FAST      -> push a to data stack
        LOAD_CONSTANT 'b'
        LOAD_FAST      -> push b to data stack
        ADD_TWO        -> no need a stack, just execute it
        STORE_FAST c   -> set the last item of data stack to variable c

        the order that programmer writes is the order to execute the codes, only
        when to call a function.
        '''
        for c in codes:
            code = c[0]
            if len(c) > 0:
                args = c[1:]
            for arg in args:
                self.data_stack.append(arg)
            method = getattr(self, code)
            method()


if __name__ == '__main__':
    frame = Frame(args=[5, 10], globals={})
    frame.run_code([('LOAD_CONST', 0), ('LOAD_FAST', ), ('LOAD_CONST', 1),
                    ('LOAD_FAST', ), ('ADD_TWO', ), ('PRINT_VAL', )])
    assert len(frame.data_stack) == 0
