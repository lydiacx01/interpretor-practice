#!/usr/bin/env python
# -*- coding: utf-8 -*-

'calculat + or - for int'

__author__ = 'lydiacx_develop@outlook.com'


INTEGER, PLUS, MINUS, MULTI, DIVID, EOF = 'INTEGER', 'PLUS', 'MINUS', 'MULTI', 'DIVID', 'EOF'
PRO_TERM, PRO_PLUS_MINUS, PRO_MULTI_DIVID, PRO_OPERATOR =1, 10, 20, 99

class Token(object):
    def __init__(self, type, value, priority):
        self.__type = type
        self.__value = value
        self.__priority = priority

    def __str__(self):
        # string representation of the class instance
        # Example:
        #   Token (INTEGER, 2)
        #   Token (PLUS, '+')
        #   Tokem (EOF, None)
        
        return 'Token ({type}, {value}, {p})'.format(
            type = self.__type,
            value = repr(self.__value),
            p = self.__priority)
    
    __repr__ = __str__

    @property
    def type(self):
        return self.__type
    @property
    def value(self):
        return self.__value
    @property
    def priority(self):
        return self.__priority


class Interpretor(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current = self.text[self.pos]
        self.token = None

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
            if (txt is None):
                return 
            elif (txt.isdigit()):
                self.token = self._int(txt)
                return
            # operator like - + * /
            elif (txt == '+'):
                token = Token(PLUS, txt, PRO_PLUS_MINUS)
            elif (txt == '-'):
                token = Token(MINUS, txt, PRO_PLUS_MINUS)
            elif (txt == '*'):
                token = Token(MULTI, txt, PRO_MULTI_DIVID)
            elif (txt == '/'):
                token = Token(DIVID, txt, PRO_MULTI_DIVID)
            else:
                self.error()
            
            self._advance()
        else:
            token = None
        self.token = token
    
    
    def _operator_check (self, priority):
        t = self.token
        ty = t.type
        if (priority == PRO_OPERATOR):
            return ty == PLUS or ty == MINUS or ty == MULTI or ty == DIVID
        else:
            return t.priority == priority
    
    ## check current token and get the next token, current token from previous char
    def _eat(self, token_type_priority):
        if (
                self.token is not None 
                and 
                (self.token.type == token_type_priority
                or 
                self._operator_check(token_type_priority))
            ):
                self._get_next_token()
        else:
            self.error()

    # get a continuous int string
    def _int(self, t):
        self._advance()
        while (self.current is not None and self.current.isdigit()):
            t += self.current
            self._advance()
        return Token(INTEGER, t, PRO_TERM)
    
    
    def _term(self):
        t = self.token
        if (t is None):
            self.error()

        self._eat(INTEGER)
        return int(t.value)


    ## known an operator is * or /, then go this cycle to run * or / calculate
    def _multi_divid(self, term, opt):
        while (True):
            right = self._term()
            if (opt.type == MULTI):
                term *= right
            else:
                term /= right
            
            opt = self.token
            if ((opt is None) or (not self._operator_check(PRO_MULTI_DIVID))):
                if (opt is not None):
                    self._eat(PRO_PLUS_MINUS)
                break
            else:
                self._eat(PRO_MULTI_DIVID)
        

        return (term, opt)

    ## known an operator is + or -, check next operator whether it's * or /
    def _plus_minus(self, term, opt):
        while (True):
            right = self._term()
            nextOpt = self.token
            # if there is a next operator existed, do next-check; else just calculate left and right
            if (self.token is not None):
                nextOpt = self.token
                self._eat(PRO_OPERATOR)
                if (nextOpt.priority == PRO_MULTI_DIVID):
                    right, nextOpt = self._multi_divid(right, nextOpt)

            term = self._plus_minus_token_calc(opt, term, right)
            opt = nextOpt
            if (opt is None):
                break
        return (term, opt)
        

    def _plus_minus_token_calc(self, token, left, right):
        if token.type == PLUS:
            left += right
        else:
            left -= right
        return left


    # analyze the text
    def expr(self):
        self._get_next_token()
        left = self._term()
        opt = self.token
        if (opt is None):
            return left

        self._eat(PRO_OPERATOR)
        while (opt is not None):
            if (opt.priority == PRO_MULTI_DIVID):
                left, opt = self._multi_divid(left, opt)
            else:
                left, opt = self._plus_minus(left, opt)


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

if __name__ == '__main__':
    test()
