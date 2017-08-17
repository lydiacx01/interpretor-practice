#empty statement#!/usr/bin/env python
# -*- coding: utf-8 -*-

'定义一个完整的pascal语法分析器，处理：program头部、var定义、begin-end.的复杂语句 + 区分var定义的变量和计算的变量存储区域(SymbolTable和GLOBAL_MEMORY) + procedure块 + nested scope'

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

INTEGER_CONST, REAL_CONST, INTEGER, REAL, VARIABLE = (
    'INTEGER_CONST', 'REAL_CONST', 'INTEGER', 'REAL', 'VARIABLE'
    )
PLUS, MINUS, MULTI, FLOAT_DIVID, INT_DIVID, LPAREN, RPAREN = (
    'PLUS', 'MINUS', 'MULTI', 'FLOAT_DIVID', 'INT_DIVID', 'LPAREN', 'RPAREN'
    )
BEGIN, END, PROGRAM, VAR, PROCEDURE = (
    'BEGIN', 'END', 'PROGRAM', 'VAR', 'PROCEDURE'
    )
EOF, DOT, ASSIGN, SEMI, COMMA, COLON = (
     'EOF',  'DOT', 'ASSIGN', 'SEMI', 'COMMA', 'COLON'
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


class Program(AST):
    def __init__(self, name, block):
        self.name = name
        self.block = block
    def __str__(self):
       return '(Program(name={n}, block={b}))'.format(
            n = self.name,
            b = repr(self.block)
           )    
    __repr__ = __str__

class Block(AST):
    def __init__(self, declarations, compound):
        self.declarations = declarations
        self.compound = compound
    def __str__(self):
       return '(Block(declarations={v}, compound={c}))'.format(
            v = repr(self.declarations),
            c = repr(self.compound)
           )    
    __repr__ = __str__

class VarDecl(AST):
    def __init__(self, variable, varType):
        self.variable = variable
        self.type = varType
    def __str__(self):
       return '(VarDecl(variable={v}, type={t}))'.format(
            v = repr(self.variable),
            t = repr(self.type)
           )    
    __repr__ = __str__


# variables
class Variable(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __str__(self):
        return '(Variable (token={t}, value={v}))'.format(
            t=repr(self.token),
            v=self.value
        )

    __repr__ = __str__

#variable Type
class VarType(AST):
    def __init__(self, typeToken):
        self.token = typeToken
        self.value = typeToken.value
    def __str__(self):
       return '(VarType(token={t}, value={v}))'.format(
            t = repr(self.token),
            v = self.value
           )    
    __repr__ = __str__

class Param(AST):
    def __init__(self, name, type):
        self.variable = name
        self.type = type
    def __str__(self):
        return '(Param: variable={n}, type={t})'.format(
            n = self.variable,
            t = self.type
        )
    __repr__ = __str__
class ProcedureDecl(AST):
    def __init__(self, name, block, params):
        self.name = name
        self.block = block
        self.params = params
    def __str__(self):
        return '(ProcedureDecl[name={name}, params={p}, block={block}])'.format(
            name = self.name,
            p = repr(self.params),
            block = repr(self.block)
        )
    __repr__ = __str__

# grammar analyzer
class Lexer(object):
    RESERVED_KEYWORDS = {
          'BEGIN': Token(BEGIN, 'BEGIN'),
          'END': Token(END, 'END'),
          'PROGRAM': Token(PROGRAM, 'PROGRAM'),
          'VAR': Token(VAR, 'VAR'),
          'INTEGER': Token(INTEGER, 'INTEGER'),
          'REAL': Token(REAL, 'REAL'),
          'DIV': Token(INT_DIVID, 'DIV'),
          'PROCEDURE': Token(PROCEDURE, 'PROCEDURE')
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
    def _number(self):
        t = ''
        while(self.__current is not None and self.__current.isdigit()):
            t += self.__current
            self._advance()
        if (self.__current == '.'):
            t += '.'
            self._advance()
            while (self.__current is not None and self.__current.isdigit()):
                t += self.__current
                self._advance()
            return Token(REAL_CONST, float(t))
        else:
            return Token(INTEGER_CONST, int(t))
    
    # return the next pos char
    def _peek(self, nx=1):
        nextpos = self.__pos + nx
        if (nextpos >= len(self.__text)):
            return None
        else:
            return self.__text[nextpos]

    # 处理字母
    def _id(self):
        t = self.__current
        self._advance()
        # 允许为字母或数字
        while (self.__current is not None and self.__current.isalnum()):
            t += self.__current
            self._advance()
        #小写格式，进行精确匹配
        up = t.upper()
        return self.RESERVED_KEYWORDS.get(up, Token(VARIABLE, t))

    def _explanation(self):
        while (self.__current != '}'):
            self._advance()
        self._advance()

    # get current char as token, and move pointer to next char 
    def get_current_token(self):
        while (self.__current is not None):
            t = self.__current
            # when t is a space, skip all spaces and continue to get the first none-space token
            if (t.isspace()):
                self._skip_whitespace()
                continue
            elif (t == '\\' and self._peek() == 'n'):
                self._advance()
                self._advance()
                continue
            elif (t == '{'):
                self._advance()
                self._explanation()
                continue
            elif (t.isdigit()):
                return self._number()
            elif (t.isalpha() or t == '_'):
                return self._id()
            elif (t == '.'):
                self._advance()
                return Token(DOT, t)
            elif (t == ':' and self._peek() == '='):
                self._advance()
                self._advance()
                return Token(ASSIGN, ':=')
            elif (t == ':'):
                self._advance()
                return Token(COLON, ':')
            elif (t == ','):
                self._advance()
                return Token(COMMA, ',')
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
                return Token(FLOAT_DIVID, t)
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
            self._error()
        return res

    def _program(self):
        name = None
        if (self.__currentToken.type == PROGRAM):
            self._eat(PROGRAM)
            name = self.__currentToken.value
            self._eat(VARIABLE)
            self._eat(SEMI)

        block = self._block()
        self._eat(DOT)
        return Program(name, block)
    
    def _block(self):
        declarations = self._declaration()
        ast = self._compound()
        return Block(declarations, ast)

    def _declaration(self):
        res = []
        if self.__currentToken.type == VAR:
            self._eat(VAR)
            while (self.__currentToken.type == VARIABLE):
                self._variableList(res)

        if (self.__currentToken.type == PROCEDURE):
            self._eat(PROCEDURE)
            name = self.__currentToken.value
            self._eat(VARIABLE)
            params = []
            if (self.__currentToken.type == LPAREN):
                self._eat(LPAREN)
                params = self._procedureParamList()
                self._eat(RPAREN)
            self._eat(SEMI)
            bl = self._block()
            res.append(ProcedureDecl(name, bl, params))
            self._eat(SEMI)
        return res

    def _procedureParamList(self):
        res = self._procedureParams()
        while (self.__currentToken.type == SEMI):
            self._eat(SEMI)
            res.extend(self._procedureParamList())
        return res

    def _procedureParams(self):
        res = []
        varIds = self._variableIdList()
        self._eat(COLON)
        varType = self._varType()
        for n in varIds:
            res.append(Param(n, varType))
        return res

    def _variableList(self, res):
        varVars = self._variableIdList()
        self._eat(COLON)
        varType = self._varType()
        self._eat(SEMI)
        for n in varVars:
            res.append(VarDecl(n, varType))

    def _variableIdList(self):
        ids = [Variable(self.__currentToken)]
        self._eat(VARIABLE)
        while self.__currentToken.type == COMMA:
            self._eat(COMMA)
            ids.append(Variable(self.__currentToken))
            self._eat(VARIABLE)
        return ids

    def _varType(self):
        t = self.__currentToken
        if (t.type == INTEGER):
            self._eat(INTEGER)
        elif (t.type == REAL):
            self._eat(REAL)
        else:
            self._error()
        return VarType(t)

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
        elif (self.__currentToken.type in (SEMI, END)):
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
        if (t.type in (INTEGER_CONST, REAL_CONST)):  
            self._eat(t.type)
            return Num(t)
        elif (t.type == LPAREN):
            self._eat(LPAREN)
            res = self._expr()
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
        while (self.__currentToken.type in (MULTI, INT_DIVID, FLOAT_DIVID)):
            op = self.__currentToken
            self._eat(op.type)
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
class NodeVisitor(object):
    GLOBAL_MEMORY = {}
    
    def _error(self):
        raise Exception('invalid node')

    def _visitBinOp(self, node):
        if (node.left is not None):
            left = self.visit(node.left)
        if (node.right is not None):
            right = self.visit(node.right)
        if (node.token.type == PLUS):
            return left + right
        elif (node.token.type == MINUS):
            return left - right
        elif (node.token.type == MULTI):
            return left * right
        elif (node.token.type == FLOAT_DIVID):
            return left / right
        elif (node.token.type == INT_DIVID):
            return left // right
        else:
            self._error()

    def _visitNum(self, node):
        return node.value

    def _visitUnary(self, node):
        r = self.visit(node.value)
        if (node.token.type == PLUS):
            return r
        else:
            return -1 * r

    def _visitAssign(self, node):
        key =  node.left.value
        val = self.visit(node.right)
        self.GLOBAL_MEMORY[key] = val

    def _visitVariable(self, node):
        name = node.value
        val = self.GLOBAL_MEMORY.get(name)
        if (val is None):
            raise NameError(repr(name))
        else:
            return val


    def _visitCompound(self, node):
        for n in node.children:
            self.visit(n)

    def _visitEmpty(self, node):
        pass

    def _visitProcedureDecl(self, node):
        print ('visit the procedure', node, '\n')

    def visit(self, node):
        if (isinstance(node, Program)):
            return self._visitProgram(node)
        elif (isinstance(node, Block)):
            return self._visitBlock(node)
        elif (isinstance(node, ProcedureDecl)):
            return self._visitProcedureDecl(node)
        elif (isinstance(node, VarDecl)):
            return  self._visitVarDecl(node)
        elif (isinstance(node, Compound)):
            return self._visitCompound(node)
        elif (isinstance(node, Empty)):
            return self._visitEmpty(node)
        elif (isinstance(node, AssignStatement)):
            return self._visitAssign(node)
        elif (isinstance(node, Variable)):
            return self._visitVariable(node)
        elif (isinstance(node, BinOp)):
            return self._visitBinOp(node)
        elif (isinstance(node, Unary)):
            return self._visitUnary(node)
        elif (isinstance(node, Num)):
            return self._visitNum(node)
        else:
            self._error()

    def _visitProgram(self, node):
        self.visit(node.block)

    def _visitBlock(self, node):
        for n in node.declarations:
            self.visit(n)
        self.visit(node.compound)

    def _visitVarDecl(self, node):
        pass


class Symbol(object):
    def __init__(self, name, type = None):
        self.name = name
        self.type = type
        self.category = self.__class__.__name__
class BuiltinSymbol(Symbol):
    def __init__(self, name):
        super(BuiltinSymbol, self).__init__(name)
    def __str__(self):
        return '<Builtin {n}>'.format(n = repr(self.name))
    __repr__ = __str__
class VarSymbol(Symbol):
    def __init__(self, name, type):
        super(VarSymbol, self).__init__(name, type)
    def __str__(self):
        return '<{n} : {t}>'.format(
            n = repr(self.name),
            t = self.type.name
        )
    __repr__ = __str__
class ProcedureSymbol(Symbol):
    def __init__(self, name, params = None):
        super(ProcedureSymbol, self).__init__(name)
        self.params = params if params is not None else []
    def __str__(self):
        return '(ProcedureSymbol: name={n}, params={p})'.format(
            n = self.name,
            p = self.params
        )
    __repr__ = __str__
class ScopedSymbolTable(object):
    def __init__(self, scopeName, scopeLevel, enclosingScope):
        self.__table = dict()
        self.__name = scopeName
        self.__level = scopeLevel
        self.__enclosingScope = enclosingScope
        self._builtins()
    def _builtins(self):
        self.define(BuiltinSymbol(INTEGER))
        self.define(BuiltinSymbol(REAL))
    @property
    def level(self):
        return self.__level
    @property
    def enclosingScope(self):
        return self.__enclosingScope
    def define(self, symbol):
        if symbol is None:
            raise Exception('must define a symbol')
        else:
            #print('define symbol:', symbol, '\n')
            name = symbol.name
            self.__table[name] = symbol
    def lookup(self, name, onlyCurrent = False):
        if (type(name) != str):
            raise NameError(name)

        node = self.__table.get(name)
        if (node is not None):
            return node
        if (onlyCurrent):
            return None

        return self.__enclosingScope.lookup(name)
    def __str__(self):
        t = '<ScopedSymbolTable-Start>\n'
        t += 'scopeLevel: %d \n' % self.__level
        t += 'scopeName: %s \n' % repr(self.__name)
        t += 'scopedContent: \n'
        for n in self.__table.items():
            t += repr(n) + '\n'
        t += '<ScopedSymbolTable-end>\n'
        return t
    __repr__ = __str__

class SemanticAnalyzer(NodeVisitor):
    def __init__(self):
        self.__currentScope = None
    def _visitProgram(self, node):
        scopeSymbolTable = ScopedSymbolTable(
            scopeName='global', scopeLevel=1, enclosingScope=self.__currentScope)
        self.__currentScope = scopeSymbolTable
        #print ('# enter the scope: global \n')
        self.visit(node.block)
        #print('# leave the scope: global \n', self.__currentScope)
        self.__currentScope = self.__currentScope.enclosingScope

    def _visitProcedureDecl(self, node):
        procedureName = node.name
        procedureSymbol = ProcedureSymbol(procedureName)
        scopedSymbolTable = ScopedSymbolTable(
            scopeName=procedureName,
            scopeLevel=self.__currentScope.level + 1,
            enclosingScope=self.__currentScope)

        for n in node.params:
            typeSymbol = self.__currentScope.lookup(n.type.value)
            varSymbol = VarSymbol(n.variable.value, typeSymbol)
            procedureSymbol.params.append(varSymbol)
            scopedSymbolTable.define(varSymbol)

        self.__currentScope.define(procedureSymbol)  # add procedure to current scope
        self.__currentScope = scopedSymbolTable # change current scope as procedure
        #print('#enter the scope: %s \n' % procedureName)
        self.visit(node.block)
        #print('#leave the scope: %s \n' % procedureName, self.__currentScope)
        self.__currentScope = self.__currentScope.enclosingScope # leave current scope
    def _visitVarDecl(self, node):
        name = node.variable.value
        if (self.__currentScope.lookup(name, True) is not None):
            raise Exception('Semantic error: duplicated declaration of variale: %s' % name)
        nodeType = node.type.value
        symbolType = self.__currentScope.lookup(nodeType)
        self.__currentScope.define(VarSymbol(name, symbolType))

    def _visitAssign(self, node):
        varName = node.left.value
        varSymbol = self.__currentScope.lookup(varName)
        if (varSymbol is None):
            raise NameError(repr(varName))
        else:
           right = self.visit(node.right)
           self.GLOBAL_MEMORY[varName] = right
    def _visitVariable(self, node):
        name = node.value
        symbol = self.__currentScope.lookup(name)
        if (symbol is None):
            raise NameError(repr(name))
        else:
            return self.GLOBAL_MEMORY.get(name)
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
        itp = SemanticAnalyzer()
        itp.visit(ast)
        print('done! 此时的GLOBAL_MEMORY={t}'.format(
            t=itp.GLOBAL_MEMORY
        ))

if __name__ == '__main__':
    test()
