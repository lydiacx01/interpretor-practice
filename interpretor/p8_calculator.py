#!/usr/bin/env python
# -*- coding: utf-8 -*-

'构造AST树，用interpretor后序遍历法（左-》右-》中顺序）计算树结果。整数的计算器，得到的结果是浮点值，四则运算, 允许带括号计算，允许单元运算，即:1+-2=-1,1++2=3'

__author__ = 'lydiacx_develop@outlook.com'

'''
    BNF（巴科斯）范式定义语法如下：
     factor: integer | LPAREN exp RPAREN
     term: factor((multi|divid)factor)*
     exp: term((plus|minus)term)*

    AST(Abstract-Syntax Tree):
    假设：1 * (2 + 3 - 4) * 5，其树状结构：
                 *
                / \
              *     5
             / \
            1   -
               / \
              +   4
             / \
            2   3
    叶子是数字（即integer），节点都是运算符
'''

INTEGER, PLUS, MINUS, MULTI, DIVID, LPAREN, RPAREN, EOF = (
    'INTEGER', 'PLUS', 'MINUS', 'MULTI', 'DIVID', 'LPAREN', 'RPAREN', 'EOF'
    )

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
        raise Exception('invalid character')

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
            elif (t == '('):
                self._advance()
                return Token(LPAREN, t)
            elif (t == ')'):
                self._advance()
                return Token(RPAREN, t)
            else:
                self._error()
                
        return Token(EOF, None)


# abstract-syntax tree node
class AST(object):
    pass

class BinOp(AST):
    def __init__(self, left, token, right):
        self.left = left
        self.token = token
        self.right = right
    def __str__(self):
        return '(BinOp (left={l}, token={t}, right={r}))'.format(
                l = repr(self.left),
                t = repr(self.token),
                r = repr(self.right)
            )
    __repr__ = __str__

# the leaf of AST
class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value
    def __str__(self):
        return '(Num (token={t}, value={v}))'.format(
                t = repr(self.token),
                v = self.value
            )
    __repr__ = __str__

# unary operator like +2, -2,在运算中：1++2=3, 1+-2=-1; 优先级比*或/更高
class Unary(AST):
    def __init__(self, token, value):
        self.token = token
        self.value = value
    def __str__(self):
        return '(Unary(token={t}, value={v}))'.format(
            t=repr(self.token),
            v = self.value
            )


#parse the text and get the AST
class Parser(object):
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
        raise Exception('invalid syntax')
        
    def _eat(self, tokenType):
        if (self.__currentToken.type == tokenType):
            self.__currentToken = self.__lexer.get_current_token()
        else:
            self._error()
    
    def _factor(self):
        t = self.__currentToken
        if (t.type == INTEGER):  
            self._eat(INTEGER)
            return Num(t)
        elif (t.type == LPAREN):
            self._eat(LPAREN)
            res = self.expr()
            self._eat(RPAREN)
            return res
        elif (t.type == PLUS):
            self._eat(PLUS)
            return Unary(t, self._factor())
        elif (t.type == MINUS):
            self._eat(MINUS)
            return Unary(t, self._factor())
        else:
            self.error()

    def _term(self):
        t = self._factor()
        while (self.__currentToken.type in (MULTI, DIVID)):
            op = self.__currentToken
            if (op.type == MULTI):
                self._eat(MULTI)
            else:
                self._eat(DIVID)
            t = BinOp(t, op, self._factor())
        return t
        
    def expr(self):
        t = self._term()

        while(self.__currentToken.type in (PLUS, MINUS)):
            op = self.__currentToken
            if (op.type == PLUS):
                self._eat(PLUS)
            else:
                self._eat(MINUS)
            t = BinOp(t, op, self._term())
        return t

# translate the ast to the rest
class Interpretor(object):
    def _error(self):
        raise Exception('invalid node')

    def _calcBinOp(self, left, node, right):
        if (node.token.type == PLUS):
            return left + right
        elif (node.token.type == MINUS):
            return left - right
        elif (node.token.type == MULTI):
            return left * right
        elif (node.token.type == DIVID):
            return left / right
        else:
            self._error()

    def _calcNum(self, node):
        return node.value

    def _calcUnary(self, node):
        if (node.token.type == PLUS):
            return self.visit(node.value)
        else:
            return -1 * self.visit(node.value)
        
    
    def visit(self, node):
        if (isinstance(node, Num)):
            return self._calcNum(node)
        if (isinstance(node, Unary)):
            return self._calcUnary(node)
        
        if (node.left is not None):
            left = self.visit(node.left)
        if (node.right is not None):
            right = self.visit(node.right)
        return self._calcBinOp(left, node, right)

    
def test():
    while True:
        try:
            txt = input('calculator>')
        except Exception as e:
            break
        if not txt:
            continue

        lexer = Lexer(txt)
        ast = Parser(lexer).expr()
        itp = Interpretor()
        res = itp.visit(ast)
        print('done! {0} = {1}'.format(txt, res))

if __name__ == '__main__':
    test()
