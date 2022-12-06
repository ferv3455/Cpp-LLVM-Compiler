from typing import List
import pickle

from .token import Token, TokenRule


class Lexer:
    def __init__(self, rules: List[TokenRule] = None) -> None:
        if rules is not None:
            self.rules = rules
            with open("./tmp/lexrules.pkl", "wb") as fp:
                pickle.dump(self.rules, fp)
        else:
            with open("./tmp/lexrules.pkl", "rb") as fp:
                self.rules = pickle.load(fp)

    def lex(self, text: str, start: int = 0) -> Token:
        if not self.rules:
            print("No rules given")
            return None

        token = None
        longest_length = 0
        for rule in self.rules:
            result = rule.apply(text, start)
            if result is not None and result.length > longest_length:
                token = result
                longest_length = result.length
        return token

    def __call__(self, text: str, start: int = 0) -> Token:
        return self.lex(text, start)


def generateTokens(text: str, rules: List[tuple] = None):
    if rules is None:
        lexer = Lexer()
    else:
        lexer = Lexer([TokenRule(*rule) for rule in rules])

    index = 0
    length = len(text)

    while index < length:
        token = lexer(text, index)

        if token is None:
            raise Exception("No rules can be applied in lexical analysis")
            # index += 1
            # continue

        if not token.ignore:
            yield token

        index += token.length
