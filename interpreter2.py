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
    frame.run_code([
        ('LOAD_CONST', 0),
        ('LOAD_FAST',),
        ('LOAD_CONST', 1),
        ('LOAD_FAST',),
        ('ADD_TWO',),
        ('PRINT_VAL',)
    ])
    assert len(frame.data_stack) == 0
