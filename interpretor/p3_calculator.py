#!/usr/bin/env python
# -*- coding: utf-8 -*-

'calculat + or - for int'

__author__ = 'lydiacx_develop@outlook.com'


INTEGER, PLUS, MINUS, MULTI, DIVID, EOF = 'INTEGER', 'PLUS', 'MINUS', 'MULTI', 'DIVID', 'EOF'

class Token(object):
    def __init__(self, type, value):
        self.__type = type
        self.__value = value

    def __str__(self):
        # string representation of the class instance
        # Example:
        #   Token (INTEGER, 2)
        #   Token (PLUS, '+')
        #   Tokem (EOF, None)
        
        return 'Token ({type}, {value})'.format(
            type = self.__type,
            value = repr(self.__value))
    
    __repr__ = __str__

    @property
    def type(self):
        return self.__type
    @property
    def value(self):
        return self.__value

class Operator(Token):
    def run(left, right):
        return 0

class PlusOperator(Operator):
    def run(self, left, right):
        return left + right

class MinusOperator(Operator):
    def run(self, left, right):
        return left - right

class MultiOperator(Operator):
    def run(self, left, right):
        return left * right

class DividOperator(Operator):
    def run(self, left, right):
        if (right == 0):
            raise ZeroDivisionError
        return left / right

class OperatorFactory(object):
    def build(self, txt):
        if (txt == '+'):
            token = PlusOperator(PLUS, txt)
        elif (txt == '-'):
            token = MinusOperator(MINUS, txt)
        elif (txt == '*'):
            token = MultiOperator(MULTI, txt)
        elif (txt == '/'):
            token = DividOperator(DIVID, txt)
        else:
            raise Exception('Token error')
        return token




class Interpretor(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current = self.text[self.pos]
        self.token = None
        self.operatorFactory = OperatorFactory()

    def __str__(self):
        return 'text={0}, pos={1}, current={2}, token={3}'.format(
                self.text,
                self.pos,
                repr(self.current),
                repr(self.token)
                )

    __repr__ = __str__

    def error(self):
        raise Exception('parsing error')

    def _advance(self):
        self.pos += 1
        if self.pos >= len(self.text):
            self.current = None
        else:
            self.current = self.text[self.pos]

    def _skip_whitespace(self):
        while(self.current is not None
                and self.current.isspace()):
            self._advance()


    # get next pos of string and format as a token
    def _get_next_token(self):
        if (self.current is not None):
            self._skip_whitespace()
            txt = self.current
            # end with whitespace
            if (txt.isdigit()):
                token = self._int(txt)
            # operator like - + * /
            else:
                token = self.operatorFactory.build(txt)
                self._advance()
            self.token = token
        else:
            self.token = None
    
    
    def _eat(self, token_type):
        if (self.token is not None 
                and 
                (self.token.type == token_type
                or 
                isinstance(self.token, token_type))):
                self._get_next_token()
        else:
            self.error()

    # get a continuous int string
    def _int(self, t):
        self._advance()
        while (self.current is not None and self.current.isdigit()):
            t += self.current
            self._advance()
        return Token(INTEGER, t)
    

    # analyze the text
    def expr(self):
        self._get_next_token()
        left = int(self.token.value)
        
        while (True):
            self._eat(INTEGER)
            opt = self.token
            if (opt is None): 
                break

            self._eat(Operator)
            if (self.token is None):
                self.error()
            right = int(self.token.value)
            left = opt.run(left, right)
        return left
        
    

def test():
    while True:
        try:
            txt = input('calculator>')
        except Exception as e:
            break
        if not txt:
            continue

        itp = Interpretor(txt)
        print('done! {t} = {r}'.format(t=txt, r=itp.expr()))

if __name__ == '__main__':
    test()
