import random

__author__ = 'Waner Miranda'
GROWTH = 0
FULL = 0


class Individual:
    def __init__(self, non_terminals=[], terminals=[], min_depth=2, max_depth=6,  terminals_chance=0.7, non_terminals_chance=0.3, method=GROWTH):
        self._tree = Tree(self)
        self._method = method
        self._min_depth = min_depth
        self._max_depth = max_depth
        self._terminals_chance = terminals_chance
        self._non_terminals_chance = non_terminals_chance
        self._non_terminals = non_terminals
        self._terminals = terminals

    def get_tree(self):
        return self._tree

    def gen_node(self, parent):
        module = globals()
        operator = int(random.choice(range(self._non_terminals.__len__())))
        operator_class = getattr(module, self._non_terminals[operator])
        return operator_class(parent)


class Tree:
    def __init__(self, individual,  min_depth=2, max_depth=6,  terminals_chance=0.7, non_terminals_chance=0.3,
                 method=GROWTH, children=[]):
        self._root = None
        self._individual = individual
        self._children = children
        self._method = method
        self._min_depth = min_depth
        self._max_depth = max_depth
        self._terminals_chance = terminals_chance
        self._non_terminals_chance = non_terminals_chance
        self._height = 0

    def add_child(self, child):
        child.set_tree(self)
        self._children.append(child)

    def add_height(self):
        self._height += 1


class Node:
    def __init__(self, parent, children=[]):
        self._parent = parent
        self._tree = parent.get_tree()
        parent.add_child(self)
        self._children = children

    def set_tree(self, tree):
        self._tree = tree

    def add_child(self, child):
        self._children.append(child)


class NonTerminal(Node):
    def __init__(self, parent, children=[]):
        Node.__init__(self, parent)
        self._children = children
        self._symbol = ''
        self.value = 0.0
        self._tree.add_height()

    def __str__(self):
        representation = '(' + self._symbol + ' '
        for child in self._children:
            representation += child.__str__() + ' '
        return representation + ')'


class Terminal(Node):
    def __init__(self, parent):
        Node.__init__(self, parent)
        self._value = 0.0

    def evaluate(self):
        return self._value

    def add_child(self, child):
        raise Exception('Terminals could not have children')


class FloatTerminal(Terminal):
    def __init__(self, parent):
        Terminal.__init__(self, parent)
        self._value = random.random()

    def __str__(self):
        return str(self._value)


class Add (NonTerminal):
    def __init__(self, parent):
        NonTerminal.__init__(self, parent, [])
        self._symbol = '+'
        self._value = 0.0

    def evaluate(self):
        self._value = 0.0
        for child in self._children:
            self._value += child.evaluate()


class Multiply (NonTerminal):
    def __init__(self, parent):
        NonTerminal.__init__(self, parent, [])
        self._symbol = '*'
        self._value = 0.0

    def evaluate(self):
        self._value = 0.0
        for child in self._children:
            self._value *= child.evaluate()


class Subtract (NonTerminal):
    def __init__(self, parent):
        NonTerminal.__init__(self, parent, [])
        self._symbol = '-'
        self._value = 0.0

    def evaluate(self):
        self._value = 0.0
        for child in self._children:
            self._value -= child.evaluate()


class ProtectedDiv (NonTerminal):
    def __init__(self, parent):
        NonTerminal.__init__(self, parent, [])
        self._symbol = '%'
        self._value = 0.0

    def evaluate(self):
        self._value = 0.0
        for child in self._children:
            child_value = child.evaluate()
            if child_value == 0:
                self._value = 1
                break
            self._value /= child_value