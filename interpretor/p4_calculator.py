#!/usr/bin/env python
# -*- coding: utf-8 -*-

'整数的计算器，得到的结果是浮点值，四则运算（不带括号）'

__author__ = 'lydiacx_develop@outlook.com'

'''
    BNF（巴科斯）范式定义语法如下：
     term: integer ===> self._term
     multi-divid-exp: ((multi|divid)term)* ===> self._multi_divid_handler
     multi-divid-full-exp: term(multi-divid-exp) ===> self.expr中的_multi_divid_handler调用
     plus-minus-exp: ((plus|minus)(multi-divid-full-exp)+)* ===> self._plus_minus_handler
     exp: term(plus-minus-exp | multi-divid-exp) ===> self.expr 
'''

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
        self.current = None
        self.nextpos = 0
        self.next = self.text[self.nextpos]

    def __str__(self):
        return 'text={0}, pos={1}, token={2}, next={3}'.format(
                self.text,
                self.nextpos,
                repr(self.current),
                repr(self.next)
                )

    __repr__ = __str__

    def error(self):
        raise Exception('parsing error')

    # the next pointer moves a step
    def _advance(self):
        self.nextpos += 1
        if self.nextpos >= len(self.text):
            self.next = None
        else:
            self.next = self.text[self.nextpos]

    def _skip_whitespace(self):
        while(self.next is not None and self.next.isspace()):
            self._advance()


    # get next pos of string and format as a token
    def _get_next_token(self):
        self._skip_whitespace()
        
        if (self.next is not None):
            txt = self.next

            if (txt.isdigit()):
                self.current = self._int(txt)
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
        self.current = token
    

    # get a continuous int string
    def _int(self, t):
        while (True):
            self._advance()
            if (self.next is None or (not self.next.isdigit())):
                break
            t += self.next
      
        return Token(INTEGER, t, PRO_TERM)
        
    def _operator_check(self, priority):
        t = self.current
        ty = t.type
        if (priority == PRO_OPERATOR):
            return ty == PLUS or ty == MINUS or ty == MULTI or ty == DIVID
        else:
            return t.priority == priority

    ## check current token and get the next token, current token from previous char
    def _eat(self, token_type_priority):
        if (
                self.current is not None
                and
                (self.current.type == token_type_priority
                or
                self._operator_check(token_type_priority))
            ):
                self._get_next_token()
        else:
            self.error()


    def _term(self):
        t = self.current
        self._eat(INTEGER)
        return int(t.value)

    def _multi_divid_token_calc(self, token_type, left, right):
        if (token_type == MULTI):
            return left * right
        else:
            return left / right

    def _plus_minus_token_calc(self, token, left, right):
        if token.type == PLUS:
            left += right
        else:
            left -= right
        return left

    def _plus_minus_handler(self, left):
        while(True):
            opt = self.current
            self._eat(PRO_PLUS_MINUS)
            right = self._term()

            if (self.current is not None):
                if (self._operator_check(PRO_MULTI_DIVID)):
                    right = self._multi_divid_handler(right)
            left = self._plus_minus_token_calc(opt, left, right)
            if (self.current is None):
                break
        
        return left

    def _multi_divid_handler(self, left):
        while(True):
            opt = self.current
            self._eat(PRO_MULTI_DIVID)
            right = self._term()
            left = self._multi_divid_token_calc(opt.type, left, right)
            if ((self.current is None) or (not self._operator_check(PRO_MULTI_DIVID))):
                break
        return left

            

    # analyze the text
    def expr(self):
        self._get_next_token()
        left = self._term()

        while (self.current is not None):
            # begin with * or /
            if (self._operator_check(PRO_MULTI_DIVID)):
                left = self._multi_divid_handler(left)
            # begin with + or -
            else:
                left = self._plus_minus_handler(left)
    
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
        res = itp.expr()
        print('done! {0} = {1}'.format(txt, res))

if __name__ == '__main__':
    test()
