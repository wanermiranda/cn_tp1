import random
import uuid

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
        self._id = str(uuid.uuid1())
        self._tree = Tree(self, self._non_terminals, self._terminals, self._min_depth, self._max_depth,
                          self._terminals_chance, self._non_terminals_chance)

    def get_id(self):
        return self._id

    def equals(self, target):
        return self._id == target.get_id()

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

    def cross_over(self, target_node, new_node):
        self._tree.cross_over(target_node, new_node)

    def select_node(self):
        result = self._tree.select_node()
        if result is None:
            result = self.select_node()
        return result


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
        self._id = str(uuid.uuid1())
        self._mutate_chance = 0
        self._mutation_nodes_reviewed = 0
        self._root = self.gen_node(self)

        while self._depth < min_depth:
            print 'Deeper', self._depth
            self._root = self.gen_node(self)
            print 'Try deepening ', self._depth

    def get_id(self):
        return self._id

    def equals(self, target):
        return self._id == target.get_id()

    def gen_node_(self, parent, children, mutating):
        chance = random.random()
        is_terminal = chance <= self._terminals_chance
        parent_depth = 0 if isinstance(parent, Tree) else parent.get_depth()
        module = globals()

        if ((not is_terminal) or isinstance(parent, Tree)) and (parent_depth <= self._max_depth - 1):
            non_terminal = int(random.choice(range(self._non_terminals.__len__())))
            non_terminal_class = module[self._non_terminals[non_terminal]]
            node = non_terminal_class(parent, children, mutating)
        else:
            terminal = int(random.choice(range(self._terminals.__len__())))
            terminal_class = module[self._terminals[terminal]]
            node = terminal_class(parent)

        self._mutation_nodes_reviewed = self._nodes
        return node

    def gen_node(self, parent):
        node = self.gen_node_(parent, [], False)
        self._nodes += 1
        return node

    def add_child(self, child):
        child.set_tree(self)
        self._children.append(child)

    @staticmethod
    def get_depth():
        return 0

    def get_real_depth(self):
        return self._depth

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
        if self._mutation_nodes_reviewed > self._nodes:
            self._mutate_chance = 1
        else:
            self._mutate_chance = float(self._mutation_nodes_reviewed)/float(self._nodes)
        self._mutation_nodes_reviewed += 1
        return self._mutate_chance

    def mutate(self):
        self._mutation_nodes_reviewed = 0
        chance = self.get_mutate_chance()
        mutating = random.random() <= chance
        representation = str(self)
        if mutating:
            print 'Choose ',  self._root
            self._root = self.gen_node_(self, self._root.get_children(), True)
            print 'Changed', self._root
        else:
            self._root.mutate()
        if representation == str(self):
            print 'Not changing'
            print representation
            print self
            self.mutate()

        while self._depth < self._min_depth:
            print 'Deeper Mutation', self._depth
            self.mutate()

    def cross_over(self, target_node, new_node):
        if self._root.equals(target_node):
            self._root = new_node
        else:
            self._root.cross_over(target_node, new_node)

    def select_node(self):
        self._mutation_nodes_reviewed = 0
        chance = self.get_mutate_chance()
        mutating = random.random() <= chance
        if mutating:
            print 'Choose ',  self._root
            return self._root
        else:
            return self._root.select_node()


class Node:
    def __init__(self, parent, children=[]):
        self._parent = parent
        self._tree = parent.get_tree()
        self._children = children
        self._depth = 0
        self._id = str(uuid.uuid1())

    def get_id(self):
        return self._id

    def equals(self, target):
        return self._id == target.get_id()

    def mutate(self):
        mutated = False
        for pos in range(self._children.__len__()):
            chance = self._tree.get_mutate_chance()
            mutating = random.random() <= chance
            if mutating:
                changing_node = self._children[pos]
                node = self._tree.gen_node_(self, changing_node.get_children(), True)
                print 'Choose ',  changing_node
                print 'Changed', node
                self._children[pos] = node
                mutated = True
                return mutated

        if not mutated:
            for pos in range(self._children.__len__()):
                mutated = self._children[pos].mutate()
                if mutated:
                    break
        return mutated

    def cross_over(self, target_node, new_node):
        for pos in range(self._children.__len__()):
            if self._children[pos].equals(target_node):
                self._children[pos] = new_node
                return True

        for pos in range(self._children.__len__()):
            if self._children[pos].cross_over(target_node, new_node):
                return True

        return False

    def select_node(self):
        for pos in range(self._children.__len__()):
            chance = self._tree.get_mutate_chance()
            selected = random.random() <= chance
            if selected:
                return self._children[pos]

        for pos in range(self._children.__len__()):
            node = self._children[pos].select_node()
            if node is not None:
                return node

        return None

    def set_tree(self, tree):
        self._tree = tree

    def add_child(self, child):
        self._children.append(child)

    def get_tree(self):
        return self._tree

    def get_depth(self):
        return self._depth

    def get_children(self):
        return self._children


class NonTerminal(Node):
    def __init__(self, parent, children=[], mutating=False):
        Node.__init__(self, parent)
        self._symbol = ''
        self._value = 0.0
        self._children = []
        if not mutating:
            self._depth = self._tree.add_depth()
            self._children.append(self._tree.gen_node(self))
            self._children.append(self._tree.gen_node(self))
        else:
            if len(children) == 0:
                self._children.append(self._tree.gen_node(self))
                self._children.append(self._tree.gen_node(self))
            else:
                self._children = children

            self._depth = parent.get_depth() + 1

            if self._depth > self.get_tree().get_real_depth():
                self.get_tree().get_depth()

    def __str__(self):
        representation = '(' + self._symbol + ' '
        for child in self._children:
            # try:
                representation += child.__str__() + ' '
            # except RuntimeError as re:
            #     print re.args, re.message
        return representation + ')'

    def get_depth(self):
        return self._depth


class Terminal(Node):
    def __init__(self, parent):
        Node.__init__(self, parent)
        self._value = 0.0
        self._depth = parent.get_depth() + 1

    def eval(self):
        return self._value

    def add_child(self, child):
        raise Exception('Terminals could not have children')

    def get_children(self):
        return []


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
    def __init__(self, parent, children=[], mutating=False):
        NonTerminal.__init__(self, parent, children, mutating)
        self._symbol = '+'
        self._value = 0.0

    def eval(self):
        self._value = 0.0
        for child in self._children:
            self._value += child.eval()
        return self._value


class Multiply (NonTerminal):
    def __init__(self, parent, children=[], mutating=False):
        NonTerminal.__init__(self, parent, children, mutating)
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
    def __init__(self, parent, children=[], mutating=False):
        NonTerminal.__init__(self, parent, children, mutating)
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
    def __init__(self, parent, children=[], mutating=False):
        NonTerminal.__init__(self, parent, children, mutating)
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