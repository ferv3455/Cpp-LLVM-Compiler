from collections import deque
from typing import Any, List

from .grammar import Grammar, Derivation
from .symbol import Symbol

from ..lexer import Token


class Item:
    def __init__(self, derivation: Derivation, index: int) -> None:
        self.derivation = derivation
        self.index = index

    def nextSymbol(self) -> Symbol:
        try:
            return self.derivation.rhs[self.index]
        except IndexError:
            return None

    def __repr__(self) -> str:
        rhs = [repr(s) for s in self.derivation.rhs]
        rhs.insert(self.index, '.')
        rhs_str = ' '.join(s for s in rhs)
        return '({})<{} -> {}>'.format(
            self.derivation.id, self.derivation.lhs, rhs_str)


class Action:
    def __init__(self, actionType: int, value: Any) -> None:
        self.type = actionType
        self.value = value

    def __repr__(self) -> str:
        return "<Action {} {}>".format(self.type, self.value)


class DFAState:
    def __init__(self, items: List[Item] = None) -> None:
        if items is not None:
            self.items = set(items)
        else:
            self.items = set()

    def updateClosure(self, allItems: List[List[Item]]) -> None:
        if not self.items:
            raise SyntaxError('Calculating closure of an empty set')

        while True:
            new_items = set()
            for item in self.items:
                next_symbol = item.nextSymbol()
                if next_symbol and not next_symbol.terminal:
                    for item_group in allItems:
                        derivation = item_group[0].derivation
                        if derivation.lhs == next_symbol:
                            if item_group[0] not in self.items:
                                new_items.add(item_group[0])

            self.items.update(new_items)
            if not new_items:
                break

    def __repr__(self) -> str:
        return repr(self.items)

    def __hash__(self) -> int:
        return sum(hash(item) for item in self.items)

    def __eq__(self, __o: object) -> bool:
        return self.items == __o.items


class ViablePrefixDFA:
    def __init__(self, grammar: Grammar) -> None:
        self.grammar = grammar

        # Get all items
        self.items = list()
        for derivation in grammar:
            self.items.append([Item(derivation, i)
                               for i in range(len(derivation.rhs) + 1)])

        # Create canonical collections of items & GO table
        self.go = list()
        self.states = list()
        self.buildTables()

        # Show all states
        # print('States in Viable Prefix DFA:')
        # for i, (state, go) in enumerate(zip(self.states, self.go)):
        #     print(i, state, go, sep='\t')

    def buildTables(self) -> None:
        # Initialize tables and lists
        tmp_states = dict()
        unprocessed_states = deque()
        count = 0

        # Create the initial state
        initial_state = DFAState({self.items[0][0]})
        initial_state.updateClosure(self.items)
        self.states.append(initial_state)
        tmp_states[initial_state] = count
        unprocessed_states.append(initial_state)
        count += 1

        # Generate all states in the DFA
        while unprocessed_states:
            state = unprocessed_states.popleft()
            go_for_state = dict()
            j_sets = dict()
            for item in state.items:
                symbol = item.nextSymbol()
                if symbol is not None:
                    derivationId = item.derivation.id
                    new_item = self.items[derivationId][item.index + 1]
                    if symbol in j_sets:
                        j_sets[symbol].add(new_item)
                    else:
                        j_sets[symbol] = {new_item}

            for symbol, j in j_sets.items():
                new_state = DFAState(j)
                new_state.updateClosure(self.items)
                if new_state not in tmp_states:
                    self.states.append(new_state)
                    tmp_states[new_state] = count
                    unprocessed_states.append(new_state)
                    count += 1
                go_for_state[symbol] = tmp_states[new_state]

            self.go.append(go_for_state)

    def action(self, stateId: int, token: Token) -> Action:
        state = self.states[stateId]
        items = state.items

        # S' -> S: action[i, $] = accept
        for item in items:
            if item.derivation.id == 0 and token is None:
                return Action(0, 0)

        # X -> a. && t in follow(X) && X != S': action[i, t] = reduce
        for item in items:
            if item.nextSymbol() is None and item.derivation.id != 0:
                # TODO: check follow
                return Action(2, item.derivation.id)

        # X -> a.tb && go[i, t] = k: action[i, t] = shift k
        for item in items:
            nextSymbol = item.nextSymbol()
            if nextSymbol:
                if nextSymbol.terminal and nextSymbol.matchToken(token):
                    return Action(1, self.goto(stateId, nextSymbol))

        # error
        return Action(3, 0)

    def goto(self, stateId: int, symbol: Symbol) -> int:
        return self.go[stateId][symbol]
