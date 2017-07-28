#!/usr/bin/env python
# -*- coding: utf-8 -*-

'calculat + or - for int'

__author__ = 'lydiacx_develop@outlook.com'


INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS', 'MINUS', 'EOF'

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


class Interpretor(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current = None

    def __str__(self):
        return 'text={0}, pos={1}, current={2}'.format(
                self.text,
                self.pos,
                repr(self.current)
                )

    __repr__ = __str__

    def error(self):
        raise Exception('parsing error')

    # get next pos of string and format as a token
    def _get_next_token(self):
        if (self.pos <= len(self.text) - 1):
            txt = self.text[self.pos]
            if (txt.isdigit()):
                token = Token(INTEGER, txt)
            elif (txt == '+'):
                token = Token(PLUS, txt)
            elif (txt == '-'):
                token = Token(MINUS, txt)
            else:
                self.error()
        else:
            token = Token(EOF, None)
        self.pos += 1
        return token

    def _eat(self, token_type):
        if (self.current.type == token_type):
            self.current = self._get_next_token()
        else:
            self.error()

    # get a continuous int string
    def _int(self):
        t = ''
        while self.current.type == INTEGER:
            try:
                t += self.current.value
                self._eat(INTEGER)
            except Exception as e:
                break

        return t
    

    # analyze the text
    def expr(self):
        self.current = self._get_next_token()
        left = int(self._int()) 

        opt = self.current.type
        if (opt == PLUS):
            self._eat(PLUS)
        else:
            self._eat(MINUS)


        right = int(self._int())
        if (opt == PLUS):
            res = left + right
        else:
            res = left - right
        return res
        
    

def test():
    while True:
        try:
            txt = input('oneDigitAdd>')
        except Exception as e:
            break;
        if not txt:
            continue

        itp = Interpretor(txt)
        print('done! {t} = {r}'.format(t=txt, r=itp.expr()))

if __name__ == '__main__':
    test()
