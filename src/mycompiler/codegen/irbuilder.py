from io import TextIOWrapper
from typing import Any

import llvmlite.ir as ll

from .analysis import simplifyAST
from .handlers import handlers
from .context import Context
from .builder import Builder
from ..parser import Symbol


class CodeGenerator:
    def __init__(self):
        pass

    def process(self, symbol: Symbol, builder: ll.IRBuilder, context: Context) -> None:
        # print(context.module)
        # print()
        if symbol.name in handlers:
            return handlers[symbol.name](symbol, builder, context, self.process)
        else:
            # print(f"Uncaught symbol: {symbol}. Using default processor")
            if symbol.terminal:
                return symbol
            else:
                if len(symbol.symbols) == 1:
                    return self.process(symbol.symbols[0], builder, context)
                else:
                    return [self.process(s, builder, context) for s in symbol.symbols]

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.process(*args, **kwds)


def generateCode(ast: Symbol, fp: TextIOWrapper, name: str = ""):
    # Semantic analysis: simplify AST 
    simplifyAST(ast)
    ast.printAST()

    # Module of the whole program
    context = Context()
    context.module = ll.Module(name)
    context.module.triple = ""
    builder = Builder()

    # Process AST
    code_gen = CodeGenerator()
    code_gen(ast, builder, context)
    
    # Output to fp
    print(context.module, file=fp)
