from collections import deque
from pprint import pprint
from typing import Any, List, Set

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
    def __init__(self, items: List[tuple] = None) -> None:
        if items is not None:
            self.items = dict(items)
        else:
            self.items = dict()

    def updateClosure(self, allItems: List[List[Item]], grammar: Grammar) -> None:
        if not self.items:
            raise SyntaxError('Calculating closure of an empty set')

        while True:
            new_items = dict()
            # for each [A -> a.Bb, a]
            for item, lookahead in self.items.items():
                next_symbol = item.nextSymbol()
                if next_symbol and not next_symbol.terminal:
                    # Calculate first(ba)
                    index = item.index
                    if index == len(item.derivation.rhs) - 1:
                        # check first(a)
                        b_set = set()
                        for l in lookahead:
                            b_set = b_set.union(grammar.firstSets[l])
                    else:
                        # check first(b)
                        b_set = grammar.firstSets[item.derivation.rhs[index + 1]].copy()

                    # update each [B -> .r, c] where c in first(ba)
                    for item_group in allItems:
                        derivation = item_group[0].derivation
                        if derivation.lhs == next_symbol:
                            if item_group[0] in new_items:
                                new_items[item_group[0]].update(b_set)
                            else:
                                new_items[item_group[0]] = b_set

            # update items
            updated = False
            for item, lookahead in new_items.items():
                if item in self.items:
                    if lookahead - self.items[item]:
                        updated = True
                        self.items[item].update(lookahead)
                else:
                    updated = True
                    self.items[item] = lookahead

            if not updated:
                break

    def __repr__(self) -> str:
        return repr(self.items)

    def __hash__(self) -> int:
        return sum(hash(item) + sum(hash(l) for l in lookahead)
                   for item, lookahead in self.items.items())

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
        initial_state = DFAState(
            [(self.items[0][0], {self.grammar.symbols['#$']})])
        initial_state.updateClosure(self.items, self.grammar)
        self.states.append(initial_state)
        tmp_states[initial_state] = count
        unprocessed_states.append(initial_state)
        count += 1

        # Generate all states in the DFA
        while unprocessed_states:
            state = unprocessed_states.popleft()
            go_for_state = dict()
            j_sets = dict()

            for item, lookahead in state.items.items():
                symbol = item.nextSymbol()
                if symbol is not None:
                    derivationId = item.derivation.id
                    new_item = self.items[derivationId][item.index + 1]
                    if symbol in j_sets:
                        j_sets[symbol].append((new_item, lookahead))
                    else:
                        j_sets[symbol] = [(new_item, lookahead)]

            for symbol, j in j_sets.items():
                new_state = DFAState(j)
                new_state.updateClosure(self.items, self.grammar)
                if new_state not in tmp_states:
                    # print(count, new_state)
                    self.states.append(new_state)
                    tmp_states[new_state] = count
                    unprocessed_states.append(new_state)
                    count += 1
                go_for_state[symbol] = tmp_states[new_state]

            self.go.append(go_for_state)

    def action(self, stateId: int, token: Token) -> Action:
        state = self.states[stateId]
        items = state.items

        # [S' -> S., #$]: action[i, $] = accept
        for item in items:
            if item.derivation.id == 0 and item.index == 1:
                if self.grammar.symbols['#$'].matchToken(token):
                    return Action(0, 0)

        # [X -> a., t]: action[i, t] = reduce
        for item, lookahead in items.items():
            if item.nextSymbol() is None:
                for symbol in lookahead:
                    if symbol.matchToken(token):
                        return Action(2, item.derivation.id)

        # [X -> a.tb, ...] && go[i, t] = k: action[i, t] = shift
        for item in items:
            nextSymbol = item.nextSymbol()
            if nextSymbol:
                if nextSymbol.terminal and nextSymbol.matchToken(token):
                    return Action(1, self.goto(stateId, nextSymbol))

        # error
        return Action(3, 0)

    def goto(self, stateId: int, symbol: Symbol) -> int:
        return self.go[stateId][symbol]
