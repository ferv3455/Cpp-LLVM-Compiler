from copy import deepcopy
from typing import Dict, Generator
from collections import deque

from .dfa import ViablePrefixDFA
from .symbol import Symbol
from .grammar import Grammar
from ..utils import IteratorWrapper


class Parser:
    def __init__(self, grammar: Dict = None) -> None:
        self.grammar = Grammar(grammar)
        # print(self.grammar)
        self.dfa = ViablePrefixDFA(self.grammar)

    def parse(self, tokens: IteratorWrapper) -> Symbol:
        stack = deque([(Symbol(True, name="#dummy"), 0)])
        while True:
            token = tokens.peek()    # could be None
            # print(token)
            action = self.dfa.action(stack[-1][1], token)
            # print(action)
            if action.type == 1:
                # Shift to state j
                stack.append((Symbol(True, token=tokens.pop()), action.value))
            elif action.type == 2:
                # Reduce using derivation j
                derivation = self.grammar[action.value]
                symbol = deepcopy(derivation.lhs)
                symbol.symbols = [stack.pop()[0]
                                  for _ in range(len(derivation.rhs))]
                symbol.symbols.reverse()
                symbol.derivation = derivation
                stack.append((symbol, self.dfa.goto(stack[-1][1], symbol)))
            elif action.type == 0:
                # Accept
                break
            else:
                # Error
                raise SyntaxError("Failed to parse {}".format(token))
            # print(stack)

        return stack[-1][0]

    def __call__(self, tokens: IteratorWrapper) -> Symbol:
        return self.parse(tokens)


def generateAST(token_gen: Generator, grammar: Dict = None):
    if grammar is None:
        parser = Parser()
    else:
        parser = Parser(grammar)

    tokens = IteratorWrapper(token_gen)
    return parser(tokens)
