from typing import Iterable, Set, Union


def match(pattern: str, text: str) -> bool:
    return text == pattern


class NFAState:
    def __init__(self, name: str = '') -> None:
        self.name = name
        self.transition = dict()
        self.neg_transition = dict()

    def addTransition(self, state: 'NFAState', c: str = '') -> None:
        if c not in self.transition:
            self.transition[c] = {state}
        else:
            self.transition[c].add(state)

    def addNegTransition(self, state: 'NFAState', c: str = '') -> None:
        if state not in self.neg_transition:
            self.neg_transition[state] = {c}
        else:
            self.neg_transition[state].add(c)

    def getTransitions(self, c: str = '') -> Set['NFAState']:
        # print(c, self.neg_transition)

        trans = [s for t, s in self.transition.items() if match(t, c)]
        if not c:
            return set().union(*trans)

        neg_trans = [s for s, t in self.neg_transition.items()
                     if all(map(lambda x: not match(x, c), t))]

        # for state, cs in self.neg_transition.items():
        #     print(list(map(lambda x: not match(x, c), cs)))

        return set().union(*trans, neg_trans)

    def __repr__(self) -> str:
        return '<NFAState %s %d>' % (self.name, id(self))


def updateEpsilonClosure(state: NFAState, states: Set[NFAState]):
    for next_state in state.getTransitions():
        if next_state not in states:
            states.add(next_state)
            updateEpsilonClosure(next_state, states)


class NFA:
    def __init__(self, pattern: str = None, neg: bool = False) -> None:
        self.states = set()
        self.start = NFAState('ε')
        self.states.add(self.start)
        self.end = self.start
        if pattern:
            if not neg:
                last = self.start
                for c in pattern:
                    new_state = NFAState(c)
                    self.states.add(new_state)
                    last.addTransition(new_state, c)
                    last = new_state
                self.end = last
            else:
                self.end = NFAState('not-{}'.format(pattern))
                self.states.add(self.end)
                for c in pattern:
                    self.start.addNegTransition(self.end, c)
        else:
            if neg:
                self.end = NFAState('not-{}'.format(pattern))
                self.states.add(self.end)
                self.start.addNegTransition(self.end)

    def simulate(self, text: str, start: int = 0) -> int:
        length = len(text)
        i = start
        accept_len = -1
        states = {self.start}
        updateEpsilonClosure(self.start, states)
        # print(states)

        while states and i < length:
            c = text[i]

            # NFAState transition
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
        new_nfa.end = NFAState('end-or')
        self.end.addTransition(new_nfa.end)
        other.end.addTransition(new_nfa.end)
        new_nfa.states.update(self.states)
        new_nfa.states.update(other.states)
        new_nfa.states.add(new_nfa.end)
        return new_nfa

    def __radd__(self, other: 'NFA') -> 'NFA':
        return self + other

    @classmethod
    def alt(cls, *args: Union[Iterable['NFA'], 'NFA']) -> 'NFA':
        new_nfa = cls()
        new_nfa.end = NFAState('end-or')
        new_nfa.states.add(new_nfa.end)

        nfas = list()
        for arg in args:
            try:
                nfas.extend(arg)
            except TypeError:
                nfas.append(arg)

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
    def concat(cls, *args: Union[Iterable['NFA'], 'NFA']) -> 'NFA':
        nfas = list()
        for arg in args:
            try:
                nfas.extend(arg)
            except TypeError:
                nfas.append(arg)
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

    # COMMENT = r('//') * n('\n').star() * r('\n')
    COMMENT = n().star() * r('y')

    text = '// uiygi\n'
    i = COMMENT.simulate(text)
    print(i, text[0:i])
