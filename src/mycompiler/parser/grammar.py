from typing import Dict, Iterator, List

from .symbol import Symbol


class Derivation:
    def __init__(self, index: int, lhs: Symbol, rhs: List[Symbol]) -> None:
        self.id = index
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self) -> str:
        rhs_str = ' '.join(repr(s) for s in self.rhs)
        return '({})<{} -> {}>'.format(self.id, self.lhs, rhs_str)


class Grammar:
    def __init__(self, grammar: Dict) -> None:
        self.symbols = dict()
        self.symbols['#S'] = Symbol(False, name='#S')
        for t in grammar['terminals']:
            self.symbols[t] = Symbol(True, name=t)
        for n in grammar['non-terminals']:
            self.symbols[n] = Symbol(False, name=n)

        self.derivations = list()
        self.derivations.append(Derivation(
            0, self.symbols['#S'], [self.symbols[grammar['start']]]))
        for i, (lhs, rhs) in enumerate(grammar['derivations'], 1):
            self.derivations.append(Derivation(
                i, self.symbols[lhs], [self.symbols[s] for s in rhs.split()]))

    def __getitem__(self, index: int) -> Derivation:
        return self.derivations[index]

    def __iter__(self) -> Iterator:
        return iter(self.derivations)

    def __repr__(self) -> str:
        derivations = ('{}'.format(d) for d in self.derivations)
        return '<Grammar [{}]>'.format(', '.join(derivations))
