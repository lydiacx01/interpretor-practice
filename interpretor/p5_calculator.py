#!/usr/bin/env python
# -*- coding: utf-8 -*-

'整数的计算器，得到的结果是浮点值，四则运算（不带括号）'

__author__ = 'lydiacx_develop@outlook.com'

'''
    BNF（巴科斯）范式定义语法如下：
     factor: integer
     term: factor((multi|divid)factor)*
     exp: term((plus|minus)term)*
'''

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

        return '(Token ({type}, {value}))'.format(
            type = self.__type,
            value = repr(self.__value))

    __repr__ = __str__

    @property
    def type(self):
        return self.__type
    @property
    def value(self):
        return self.__value

# grammar analyzer
class Lexer(object):
    def __init__(self, text):
        self.__text = text
        self.__pos = 0
        self.__current = self.__text[self.__pos]
    
    def __str__(self):
        return '(text={0}, pos={1}, current={2})'.format(
                self.__text,
                self.__pos,
                self.__current
                )

    __repr__ = __str__

    def _error(self):
        raise Exception('parsing error')

    # the pointer move advance a step, check whether it reached the end of text
    def _advance(self):
        self.__pos += 1
      
        if (self.__pos >= len(self.__text)):
            self.__current = None
        else:
            self.__current = self.__text[self.__pos]

    # skip all the contiuous spaces to a char that is not space
    def _skip_whitespace(self):
        while(self.__current is not None and self.__current.isspace()):
            self._advance()

    # get contiuous digit as a integer number
    def _integer(self):
        t = ''
        while(self.__current is not None and self.__current.isdigit()):
            t += self.__current
            self._advance()
        
        return int(t)

    # get current char as token, and move pointer to next char 
    def get_current_token(self):
        while (self.__current is not None):
            t = self.__current
            # when t is a space, skip all spaces and continue to get the first none-space token
            if (t.isspace()):
                self._skip_whitespace()
                continue
            elif (t.isdigit()):
                t = self._integer()
                self._advance()
                return Token(INTEGER, t)
            elif (t == '+'):
                self._advance()
                return Token(PLUS, t)
            elif (t == '-'):
                self._advance()
                return Token(MINUS, t)
            elif (t == '*'):
                self._advance()
                return Token(MULTI, t)
            elif (t == '/'):
                self._advance()
                return Token(DIVID, t)
            else:
                self._error()
                
        return Token(EOF, None)


class Interpretor(object):
    def __init__(self, lexer):
        self.__lexer = lexer
        self.__currentToken = self.__lexer.get_current_token()

    def __str__(self):
        return '(currentToken={0}, lexer={1})'.format(
                repr(self.__currentToken),
                repr(self.__lexer)
                )

    __repr__ = __str__


    def _error(self):
        raise Exception('interprete error')
        
    def _eat(self, tokenType):
        if (self.__currentToken.type == tokenType):
            self.__currentToken = self.__lexer.get_current_token()
        else:
            self._error()
    
    def _factor(self):
        t = self.__currentToken
        self._eat(INTEGER)
        return t.value

    def _term(self):
        t = self._factor()
        while (self.__currentToken.type in (MULTI, DIVID)):
            if (self.__currentToken.type == MULTI):
                self._eat(MULTI)
                t *= self._factor()
            else:
                self._eat(DIVID)
                t /= self._factor()
        return t
        
    def expr(self):
        t = self._term()

        while(self.__currentToken.type is not EOF):
            if (self.__currentToken.type == PLUS):
                self._eat(PLUS)
                t += self._term()
            else:
                self._eat(MINUS)
                t -= self._term()
        return t


def test():
    while True:
        try:
            txt = input('calculator>')
        except Exception as e:
            break
        if not txt:
            continue

        lexer = Lexer(txt)
        itp = Interpretor(lexer)
        res = itp.expr()
        print('done! {0} = {1}'.format(txt, res))

if __name__ == '__main__':
    test()
