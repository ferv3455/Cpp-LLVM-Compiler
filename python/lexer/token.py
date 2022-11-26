from typing import Any

from .nfa import NFA


class Token:
    def __init__(self, name: str, value: Any, length: int, ignore: bool = False) -> None:
        self.name = name
        self.value = value
        self.length = length
        self.ignore = ignore


class TokenRule:
    def __init__(self, name: str, nfa: NFA, ignore: bool = False) -> None:
        self.name = name
        self.nfa = nfa
        self.ignore = ignore

    def apply(self, text: str, start: int = 0) -> int:
        length = self.nfa.simulate(text, start)
        if length > 0:
            return Token(self.name, text[start:start+length], length, self.ignore)
        return None
