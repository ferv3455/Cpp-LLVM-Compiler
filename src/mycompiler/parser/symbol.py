from typing import Any, List

from ..lexer import Token


class Symbol:
    def __init__(self, isTerminal: bool, **kwargs: Any) -> None:
        if isTerminal:
            self.terminal = True
            if 'token' in kwargs:
                self.token = kwargs['token']
                self.name = self.token.name
                self.value = self.token.value
            elif 'name' in kwargs:
                self.token = None
                name_list = kwargs['name'].split('::')
                self.name = name_list[0]
                if len(name_list) == 1:
                    self.value = None
                else:
                    self.value = name_list[1]
            else:
                raise SyntaxError('No name is given to the symbol')
        else:
            self.terminal = False
            self.symbols = None         # only to save the AST
            self.derivation = None      # only to save the AST
            if 'name' in kwargs:
                self.name = kwargs['name']
            else:
                raise SyntaxError('No name is given to the symbol')

    def printAST(self, end: List[bool] = None, **kwargs: Any) -> None:
        if end is None:
            print(self, **kwargs)
            for symbol in self.symbols[:-1]:
                symbol.printAST([False], **kwargs)
            self.symbols[-1].printAST([True], **kwargs)
            return

        prefix_list = [('   ' if b else '│  ') for b in end[:-1]] + \
            ['└─ ' if end[-1] else '├─ ']

        # Skip nodes with only one child
        if not self.terminal and len(self.symbols) == 1:
            self.symbols[0].printAST(end, **kwargs)
            return

        print('{}{}'.format(''.join(prefix_list), self), **kwargs)
        if not self.terminal:
            for symbol in self.symbols[:-1]:
                symbol.printAST(end + [False], **kwargs)
            self.symbols[-1].printAST(end + [True], **kwargs)

    def matchToken(self, token: Token) -> bool:
        if not self.terminal:
            return False

        if self.value is None:
            return self.name == token.name
        else:
            return self.name == token.name and self.value == token.value

    def __repr__(self) -> str:
        if self.terminal and self.value is not None:
            return self.name + '::' + self.value
        else:
            return self.name

    def __hash__(self) -> int:
        if self.terminal:
            return hash(self.name + str(self.value))
        else:
            return hash(self.name)

    def __eq__(self, __o: object) -> bool:
        if self.terminal and self.value is not None:
            return self.name == __o.name and self.value == __o.value
        else:
            return self.name == __o.name
