from typing import Iterable, List

from .token import Token, TokenRule


class Lexer:
    def __init__(self, rules: List[TokenRule] = None) -> None:
        self.rules = rules

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
        return token


def generateTokens(text: str, rules: List[tuple]):
    lexer = Lexer([TokenRule(*rule) for rule in rules])
    index = 0
    length = len(text)

    while index < length:
        token = lexer.lex(text, index)

        if token is None:
            # TODO: should be error here
            index += 1
            continue

        if not token.ignore:
            yield token

        index += token.length
