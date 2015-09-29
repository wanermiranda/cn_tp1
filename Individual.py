import random
__author__ = 'Waner Miranda'
GROWTH = 0
FULL = 0


class Individual:
    def __init__(self, non_terminals=[], terminals=[], min_depth=2, max_depth=6,  terminals_chance=0.7,
                 non_terminals_chance=0.3, variables=[], method=GROWTH):
        self._method = method
        self._min_depth = min_depth
        self._max_depth = max_depth
        self._terminals_chance = terminals_chance
        self._non_terminals_chance = non_terminals_chance
        self._non_terminals = non_terminals
        self._terminals = terminals
        self._variables = variables
        self._value = 0.0
        self._fitness = 0.0
        self._data_row = []
        self._tree = Tree(self, self._non_terminals, self._terminals, self._min_depth, self._max_depth,
                          self._terminals_chance, self._non_terminals_chance)

    def set_fitness(self, value):
        self._fitness = value

    def get_fitness(self):
        return self._fitness

    def get_tree(self):
        return self._tree

    def __str__(self):
        return self._tree.__str__()

    def eval(self, data_row=[]):
        self._data_row = data_row
        self._value = self._tree.eval()
        return self._value

    def get_data_row(self):
        return self._data_row

    def get_variables(self):
        return self._variables

    def mutate(self):
        self._tree.mutate()


class Tree:
    def __init__(self, individual,  non_terminals=[], terminals=[], min_depth=2, max_depth=6,  terminals_chance=0.7,
                 non_terminals_chance=0.3, method=GROWTH, children=[]):
        self._individual = individual
        self._children = children
        self._method = method
        self._min_depth = min_depth
        self._max_depth = max_depth
        self._terminals_chance = terminals_chance
        self._non_terminals_chance = non_terminals_chance
        self._non_terminals = non_terminals
        self._terminals = terminals
        self._depth = 0
        self._nodes = 0
        self._value = 0.0
        self._mutate_chance = 0
        self._nodes_to_mutate = 0
        self._root = self.gen_node(self)

    def gen_node_(self, parent, mutating=False):
        chance = random.random()
        is_terminal = chance <= self._terminals_chance
        module = globals()
        if ((not is_terminal) or isinstance(parent, Tree)) and (self._depth <= self._max_depth - 1):
            non_terminal = int(random.choice(range(self._non_terminals.__len__())))
            non_terminal_class = module[self._non_terminals[non_terminal]]
            node = non_terminal_class(parent, mutating=False)
        else:
            terminal = int(random.choice(range(self._terminals.__len__())))
            terminal_class = module[self._terminals[terminal]]
            node = terminal_class(parent)
        return node

    def gen_node(self, parent):
        node = self.gen_node_(parent)

        self._nodes += 1
        return node

    def add_child(self, child):
        child.set_tree(self)
        self._children.append(child)

    def add_depth(self):
        self._depth += 1
        return self._depth

    def get_tree(self):
        return self

    def get_individual(self):
        return self._individual

    def __str__(self):
        return self._root.__str__()

    def eval(self):
        self._value = self._root.eval()
        return self._value

    def get_mutate_chance(self):
        self._nodes_to_mutate -= 1
        self._mutate_chance = 1 - (self._nodes_to_mutate/self._nodes)
        return self._mutate_chance

    def mutate(self):
        self._nodes_to_mutate = self._nodes
        chance = self.get_mutate_chance()
        mutating = random.random() >= chance
        if mutating:
            self._root = self.gen_node_(self, True)


class Node:
    def __init__(self, parent, children=[]):
        self._parent = parent
        self._tree = parent.get_tree()
        self._children = children

    def set_tree(self, tree):
        self._tree = tree

    def add_child(self, child):
        self._children.append(child)

    def get_tree(self):
        return self._tree

    def mutate(self):
        print 'mutate'


class NonTerminal(Node):
    def __init__(self, parent, mutating=False, children=[]):
        Node.__init__(self, parent)
        self._children = children
        self._symbol = ''
        self._value = 0.0
        self._depth = self._tree.add_depth()
        children.append(self._tree.gen_node(self))
        children.append(self._tree.gen_node(self))

    def __str__(self):
        representation = '(' + self._symbol + ' '
        for child in self._children:
            representation += child.__str__() + ' '
        return representation + ')'

    def get_depth(self):
        return self._depth


class Terminal(Node):
    def __init__(self, parent):
        Node.__init__(self, parent)
        self._value = 0.0
        self._depth = parent.get_depth()

    def eval(self):
        return self._value

    def add_child(self, child):
        raise Exception('Terminals could not have children')


class FloatTerminal(Terminal):
    def __init__(self, parent):
        Terminal.__init__(self, parent)
        self._value = random.random()

    def __str__(self):
        return str(self._value)

    def eval(self):
        return self._value


class ArrayVariableTerminal(Terminal):
    def __init__(self, parent):
        Terminal.__init__(self, parent)
        self._individual = self.get_tree().get_individual()
        self._variables = self._individual.get_variables()
        self._index = int(random.choice(range(self._variables.__len__())))

    def __str__(self):
        return self._variables[self._index]

    def eval(self):
        data_row = self._individual.get_data_row()
        self._value = data_row[self._index]
        return self._value


class Add (NonTerminal):
    def __init__(self, parent):
        NonTerminal.__init__(self, parent, [])
        self._symbol = '+'
        self._value = 0.0

    def eval(self):
        self._value = 0.0
        for child in self._children:
            self._value += child.eval()
        return self._value


class Multiply (NonTerminal):
    def __init__(self, parent):
        NonTerminal.__init__(self, parent, [])
        self._symbol = '*'
        self._value = 0.0

    def eval(self):
        self._value = 0.0
        first = True
        for child in self._children:
            if first:
                self._value = child.eval()
                first = False
            else:
                self._value *= child.eval()
        return self._value


class Subtract (NonTerminal):
    def __init__(self, parent):
        NonTerminal.__init__(self, parent, [])
        self._symbol = '-'
        self._value = 0.0

    def eval(self):
        self._value = 0.0
        first = True
        for child in self._children:
            if first:
                self._value = child.eval()
            else:
                self._value -= child.eval()
        return self._value


class ProtectedDiv (NonTerminal):
    def __init__(self, parent):
        NonTerminal.__init__(self, parent, [])
        self._symbol = '%'
        self._value = 0.0

    def eval(self):
        self._value = 0.0
        first = True

        for child in self._children:
            child_value = child.eval()
            if first:
                self._value = child_value
                first = False
            else:
                if child_value == 0:
                    self._value = 1
                    break
                self._value /= child_value
        return self._value