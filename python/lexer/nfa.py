from typing import Iterable, List, Set


def match(pattern: str, text: str) -> bool:
    return text == pattern


class State:
    def __init__(self, name: str = '') -> None:
        self.name = name
        self.transition = dict()
        self.neg_transition = dict()

    def addTransition(self, state: 'State', c: str = '') -> None:
        if c not in self.transition:
            self.transition[c] = {state}
        else:
            self.transition[c].add(state)

    def addNegTransition(self, state: 'State', c: str = '') -> None:
        if c not in self.neg_transition:
            self.neg_transition[c] = [state]
        else:
            self.neg_transition[c].add(state)

    def getTransitions(self, c: str = '') -> Set['State']:
        result = set()
        for t in self.transition:
            if match(t, c):
                result.update(self.transition[t])

        # trans = self.transition.get(c, list())
        trans = [s for t, s in self.transition.items() if match(t, c)]
        neg_trans = [s for t, s in self.neg_transition.items()
                     if not match(t, c)]
        return set().union(*trans, *neg_trans)

    def __str__(self) -> str:
        return '<State %s %d>' % (self.name, id(self))

    def __repr__(self) -> str:
        return str(self)


def updateEpsilonClosure(state: State, states: Set[State]):
    for next_state in state.getTransitions():
        if next_state not in states:
            states.add(next_state)
            updateEpsilonClosure(next_state, states)


class NFA:
    def __init__(self, pattern: str = None, neg: bool = False) -> None:
        self.states = set()
        self.start = State('ε')
        self.states.add(self.start)
        self.end = self.start
        if pattern:
            if not neg:
                last = self.start
                for c in pattern:
                    new_state = State(c)
                    self.states.add(new_state)
                    last.addTransition(new_state, c)
                    last = new_state
                self.end = last
            else:
                self.end = State('not-{}'.format(pattern))
                self.states.add(self.end)
                for c in pattern:
                    self.start.addNegTransition(self.end, c)

    def simulate(self, text: str, start: int = 0) -> int:
        length = len(text)
        i = start
        accept_len = -1
        states = {self.start}
        updateEpsilonClosure(self.start, states)
        # print(states)

        while states and i < length:
            c = text[i]

            # State transition
            new_states = set()
            for state in states:
                new_states.update(state.getTransitions(c))
            states = new_states.copy()

            # print(states)

            # Update epsilon transitions
            for state in states:
                updateEpsilonClosure(state, new_states)
            states = new_states

            # print(states)

            # Check whether to accept the input
            if self.end in states:
                accept_len = i - start + 1

            i += 1

        return accept_len

    def __add__(self, other: 'NFA') -> 'NFA':
        if other is None:
            return self

        new_nfa = type(self)()
        new_nfa.start.addTransition(self.start)
        new_nfa.start.addTransition(other.start)
        new_nfa.end = State('end-or')
        self.end.addTransition(new_nfa.end)
        other.end.addTransition(new_nfa.end)
        new_nfa.states.update(self.states)
        new_nfa.states.update(other.states)
        new_nfa.states.add(new_nfa.end)
        return new_nfa

    def __radd__(self, other: 'NFA') -> 'NFA':
        return self + other

    @classmethod
    def multipleOr(cls, nfas: Iterable['NFA']) -> 'NFA':
        new_nfa = cls()
        new_nfa.end = State('end-or')
        new_nfa.states.add(new_nfa.end)
        for nfa in nfas:
            new_nfa.start.addTransition(nfa.start)
            nfa.end.addTransition(new_nfa.end)
            new_nfa.states.update(nfa.states)
        return new_nfa

    def __mul__(self, other: 'NFA') -> 'NFA':
        if other is None:
            return self

        self.end.addTransition(other.start)
        self.end = other.end
        self.states.update(other.states)
        return self

    def __rmul__(self, other: 'NFA') -> 'NFA':
        return self * other

    @classmethod
    def multipleConcat(cls, nfas: Iterable['NFA']) -> 'NFA':
        iterator = iter(nfas)

        try:
            first = next(iterator)
        except StopIteration:
            return None

        last = first
        for nfa in iterator:
            last.end.addTransition(nfa.start)
            first.states.update(nfa.states)
            last = nfa

        first.end = last.end
        return first

    def star(self) -> 'NFA':
        self.start.addTransition(self.end)
        self.end.addTransition(self.start)
        return self

    def plus(self) -> 'NFA':
        self.end.addTransition(self.start)
        return self

    def optional(self) -> 'NFA':
        self.start.addTransition(self.end)
        return self


if __name__ == '__main__':
    import string
    from copy import deepcopy as c
    from functools import partial
    r = NFA
    n = partial(NFA, neg=True)

    COMMENT = r('//') * n('\n').star() * r('\n')

    text = '// uiygi\n'
    i = COMMENT.simulate(text)
    print(i, text[0:i])
