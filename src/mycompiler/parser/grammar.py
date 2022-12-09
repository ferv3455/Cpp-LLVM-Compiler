from typing import Dict, Iterator, List, Set

from .symbol import Symbol


def first(grammar: 'Grammar') -> Dict[Symbol, Set]:
    # TODO: do not consider epsilon here
    # Initialize first sets for terminals
    first_sets = dict()
    for symbol in grammar.symbols.values():
        if symbol.terminal:
            first_sets[symbol] = set((symbol, ))
        else:
            first_sets[symbol] = set()

    # Update other first sets until no changes have been made
    while True:
        updated = False
        for d in grammar.derivations:
            if first_sets[d.rhs[0]] - first_sets[d.lhs]:
                updated = True
                first_sets[d.lhs].update(first_sets[d.rhs[0]])
        if not updated:
            break

    return first_sets


def follow(grammar: 'Grammar') -> Dict[Symbol, Set]:
    # TODO: do not consider epsilon here
    # Initialize first sets for terminals
    follow_sets = dict()
    for name, symbol in grammar.symbols.items():
        if name == '#S':
            follow_sets[symbol] = set((grammar.symbols['#$'], ))
        else:
            follow_sets[symbol] = set()

    # Update follow sets with first sets
    first_sets = first(grammar)
    for d in grammar.derivations:
        length = len(d.rhs)
        for i in range(length - 1):
            follow_sets[d.rhs[i]].update(first_sets[d.rhs[i + 1]])

    # Update first sets until no changes have been made
    while True:
        updated = False
        for d in grammar.derivations:
            if follow_sets[d.lhs] - follow_sets[d.rhs[-1]]:
                updated = True
                follow_sets[d.rhs[-1]].update(follow_sets[d.lhs])
        if not updated:
            break

    return follow_sets


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
        self.symbols['#$'] = Symbol(True, name='#$')
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

        self.firstSets = first(self)
        self.followSets = follow(self)

    def __getitem__(self, index: int) -> Derivation:
        return self.derivations[index]

    def __iter__(self) -> Iterator:
        return iter(self.derivations)

    def __repr__(self) -> str:
        derivations = ('{}'.format(d) for d in self.derivations)
        return '<Grammar [{}]>'.format(', '.join(derivations))
