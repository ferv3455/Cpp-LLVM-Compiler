from typing import Generator, List

from .myast import AST
from ..utils import IteratorWrapper


class Parser:
    def __init__(self) -> None:
        # TODO
        pass

    def parse(self, tokens: IteratorWrapper) -> AST:
        # TODO
        res = list()
        while not tokens.empty():
            res.append(tokens.pop())
        return res

    def __call__(self, tokens: IteratorWrapper) -> AST:
        return self.parse(tokens)


def generateAST(token_gen: Generator, grammar: List[tuple] = None):
    if grammar is None:
        parser = Parser()
    else:
        parser = Parser()  # TODO
        pass

    tokens = IteratorWrapper(token_gen)
    return parser(tokens)
