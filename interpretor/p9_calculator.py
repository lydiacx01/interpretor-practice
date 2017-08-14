#empty statement#!/usr/bin/env python
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

INTEGER, PLUS, MINUS, MULTI, DIVID, LPAREN, RPAREN, EOF, BEGIN, END, DOT, ASSIGN, VARIABLE, SEMI = (
    'INTEGER', 'PLUS', 'MINUS', 'MULTI', 'DIVID', 'LPAREN', 'RPAREN', 'EOF', 'BEGIN', 'END', 'DOT', 'ASSIGN', 'VARIABLE', 'SEMI'
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
    __repr__ = __str__

#variables
class Variable(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value
    
    def __str__(self):
        return '(Variable (token={t}, value={v}))'.format(
            t=repr(self.token),
            v = self.value
            )
    __repr__ = __str__


#empty statement
class Empty(AST):
    pass

class AssignStatement(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return '(AssignStatement (left={l}, op={o}, right={r}))'.format(
            l=repr(self.left),
            o=repr(self.op),
            r=repr(self.right)
            )
    __repr__ = __str__


class Compound(AST):
    def __init__(self, children):
        self.children = children
    def __str__(self):
       return '(Compound(children={t}))'.format(
            t = self.children
           )
       
    __repr__ = __str__


# grammar analyzer
class Lexer(object):
    RESERVED_KEYWORDS = {
          'BEGIN': Token(BEGIN, 'BEGIN'),
          'END': Token(END, 'END')
        }
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
        
        return Token(INTEGER, int(t))

    # return the next pos char
    def _peek(self):
        nextpos = self.__pos + 1
        if (nextpos >= len(self.__text)):
            return None
        else:
            return self.__text[nextpos]

    # 处理字母
    def _id(self):
        t = ''
        # 允许为字母或数字
        while (self.__current is not None and self.__current.isalnum()):
            t += self.__current
            self._advance()
        #小写格式，进行精确匹配
        up = t.upper()
        return self.RESERVED_KEYWORDS.get(up, Token(VARIABLE, t))

    # get current char as token, and move pointer to next char 
    def get_current_token(self):
        while (self.__current is not None):
            t = self.__current
            # when t is a space, skip all spaces and continue to get the first none-space token
            if (t.isspace()):
                self._skip_whitespace()
                continue
            elif (t == '\n'):
                self._advance()
                continue
            elif (t.isdigit()):
                return self._integer()
            elif (t.isalpha()):
                return self._id()
            elif (t == '.'):
                self._advance()
                return Token(DOT, t)
            elif (t == ':' and self._peek() == '='):
                self._advance()
                self._advance()
                return Token(ASSIGN, ':=')
            elif (t == ';'):
                self._advance()
                return Token(SEMI, t)
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

    def parse(self):
        res = self._program()
        if (self.__currentToken.type != EOF):
            self.error()
        return res

    def _program(self):
        ast = self._compound()
        self._eat(DOT)
        return ast

    def _compound(self):
        self._eat(BEGIN)
        res = self._statementList()
        self._eat(END)
        r = Compound(res)
        return r

    def _statementList(self):
        s = []
        s.append(self._statement())
        while (self.__currentToken.type == SEMI):
            self._eat(SEMI)
            if (self.__currentToken.type == END):
                break
            else:
                s.append(self._statement())
        return s

    def _statement(self):
        if (self.__currentToken.type == BEGIN):
            return self._compound()
        elif (self.__currentToken.type == SEMI):
            return Empty()
        else:
            return self._assignStatement()

    def _assignStatement(self):
        left = self.__currentToken
        self._eat(VARIABLE)
        op = self.__currentToken
        self._eat(ASSIGN)
        right = self._expr()
        ass = AssignStatement(left, op, right)
        return ass
                

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
            self._eat(VARIABLE)
            return Variable(t)

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
        
    def _expr(self):
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
    buff = {}
    
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
        r = self.run(node.value)
        if (node.token.type == PLUS):
            return r
        else:
            return -1 * r

    def _calcAssign(self, node):
        key =  node.left.value
        val = self.run(node.right)
        self.buff[key] = val

    def _calcVariable(self, node):
        name = node.value
        val = self.buff.get(name)
        if (val is None):
            raise NameError(repr(name))
        else:
            return val


    def _calcCompound(self, node):
        for n in node.children:
            self.run(n)

    def _calcEmpty(self, node):
        pass

    def run(self, node):
        if (isinstance(node, Num)):
            return self._calcNum(node)
        if (isinstance(node, Unary)):
            return self._calcUnary(node)
        if (isinstance(node, Variable)):
            return self._calcVariable(node)
        if (isinstance(node,Empty)):
            return self._calcEmpty(node)
        if (isinstance(node, Compound)):
            return self._calcCompound(node)
        if (isinstance(node, AssignStatement)):
            return self._calcAssign(node)

        if (isinstance(node, BinOp)): 
            if (node.left is not None):
                left = self.run(node.left)
            if (node.right is not None):
                right = self.run(node.right)
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
        ast = Parser(lexer).parse()
        itp = Interpretor()
        itp.run(ast)
        print('done! 此时的Buff={t}'.format(t=itp.buff))

if __name__ == '__main__':
    test()
