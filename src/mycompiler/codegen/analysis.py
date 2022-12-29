from typing import Callable
from ..parser import Symbol


processors = dict()

def processor(name: str):
    global processors
    def wrapper(func: Callable) -> Callable:
        if name in processors:
            raise SyntaxError("Multiple processors assigned to " + name)
        processors[name] = func
        return func
    return wrapper

def simplifyAST(symbol: Symbol):
    if symbol.name in processors:
        processors[symbol.name](symbol)
    else:
        if not symbol.terminal:
            for s in symbol.symbols:
                simplifyAST(s)

@processor('EXPR-ST')
@processor('EXPR')
@processor('EXPR-L17')
@processor('EXPR-L16')
@processor('EXPR-L15')
@processor('EXPR-L14')
@processor('EXPR-L13')
@processor('EXPR-L12')
@processor('EXPR-L11')
@processor('EXPR-L10')
@processor('EXPR-L7')
@processor('EXPR-L6')
@processor('EXPR-L5')
@processor('EXPR-L3')
@processor('EXPR-L2')
@processor('EXPR-L1')
def expr(symbol: Symbol):
    new_symbols = list()
    for s in symbol.symbols:
        simplifyAST(s)
        if s.name.startswith('EXPR') and not s.terminal and len(s.symbols) == 1:
            new_symbols.append(s.symbols[0])
        else:
            new_symbols.append(s)
    symbol.symbols = new_symbols

@processor('TYPES')
@processor('ARGS')
def args(symbol: Symbol):
    simplifyAST(symbol.symbols[0])
    if symbol.symbols[0].name == symbol.name:
        simplifyAST(symbol.symbols[-1])
        symbol.symbols = [*symbol.symbols[0].symbols, symbol.symbols[-1]]

@processor('DECLARATORS')
@processor('PARAMS')
def args_reverse(symbol: Symbol):
    simplifyAST(symbol.symbols[0])
    if symbol.symbols[-1].name == symbol.name:
        simplifyAST(symbol.symbols[-1])
        symbol.symbols = [symbol.symbols[0], *symbol.symbols[-1].symbols]

@processor('TYPE-SPECS')
@processor('STATEMENTS')
def stats_reverse(symbol: Symbol):
    simplifyAST(symbol.symbols[0])
    if symbol.symbols[-1].name == symbol.name:
        simplifyAST(symbol.symbols[-1])
        symbol.symbols = [*symbol.symbols[0].symbols, *symbol.symbols[-1].symbols]
    else:
        symbol.symbols = symbol.symbols[-1].symbols
