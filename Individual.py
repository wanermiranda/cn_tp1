import random
import uuid
import math

__author__ = 'Waner Miranda'
GROWTH = 0
FULL = 0


class Individual:
    def __init__(self, non_terminals=[], terminals=[], min_depth=2, max_depth=6,  terminals_chance=0.7,
                 non_terminals_chance=0.3, variables=[], method=GROWTH, unity=False):
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
        self.using_vars = 0
        self._id = None
        self.renew_id()
        if not unity:
            self._tree = Tree(self, self._non_terminals, self._terminals, self._min_depth, self._max_depth,
                              self._terminals_chance, self._non_terminals_chance)
        else:
            self._tree = Tree.create_unity(self ,self._non_terminals, self._terminals, self._min_depth, self._max_depth,
                                          self._terminals_chance, self._non_terminals_chance)
        self._representation = None
        self._representation = self.gen_representation()
        while not self.check_all_vars():
            self._tree = Tree(self, self._non_terminals, self._terminals, self._min_depth, self._max_depth,
                              self._terminals_chance, self._non_terminals_chance)
            self._representation = None
            self._representation = self.gen_representation()

    def renew_id(self):
        self._id = str(uuid.uuid1())

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
        if self._representation is None:
            self._representation = self.gen_representation()
        return self._representation

    def gen_representation(self):
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
        representation = str(self)
        while not self.check_all_vars() or str(self) == representation:
            self._fitness = 0.0
            self.renew_id()
            self._representation = None
            self._tree.mutate()
            self._tree.update_depth()

    def cross_over(self, target_node, new_node):
        self._fitness = 0.0
        self.renew_id()
        self._representation = None
        self._tree.cross_over(target_node, new_node)
        self._tree.update_depth()
        return self.check_all_vars()

    def select_node(self):
        result = self._tree.select_node()
        if result is None:
            result = self.select_node()
        return result

    def get_tree_depth(self):
        return self._tree.get_tree_depth()

    def print_stats(self):
        print 'Ind:', self
        print 'Fitness =', self.get_fitness()

    def check_all_vars(self):
        result = True
        representation = str(self)
        for var in self._variables:
            result = result and (var in representation)
        return result


class Tree:
    def __init__(self, individual,  non_terminals=[], terminals=[], min_depth=2, max_depth=6,  terminals_chance=0.7,
                 non_terminals_chance=0.3, method=GROWTH, children=[], unity=False):
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
        if not unity:
            self._root = self.gen_node(self)

            while self._depth < min_depth:
                # print 'Deeper', self._depth
                self._root = self.gen_node(self)
                # print 'Try deepening ', self._depth

    def get_id(self):
        self._id = str(uuid.uuid1())

    def equals(self, target):
        return self._id == target.get_id()

    def gen_node_(self, parent, children, mutating):
        chance = random.random()
        is_terminal = chance <= self._terminals_chance
        parent_depth = 0 if isinstance(parent, Tree) else parent.get_depth()
        module = globals()

        if ((not is_terminal) or isinstance(parent, Tree)) and (parent_depth < self._max_depth - 1):
            non_terminal = random.choice(range(self._non_terminals.__len__()))
            non_terminal_class = module[self._non_terminals[non_terminal]]
            node = non_terminal_class(parent, children, mutating)
        else:
            terminal = random.choice(range(self._terminals.__len__()))
            terminal_class = module[self._terminals[terminal]]
            node = terminal_class(parent)

        self._mutation_nodes_reviewed = self._nodes
        return node

    def update_depth(self):
        self._depth = 0
        self._nodes = 0
        self._root.update_depth()

    def gen_node(self, parent):
        node = self.gen_node_(parent, [], False)
        self.add_node()
        return node

    def add_node(self):
        self._nodes += 1

    def add_child(self, child):
        child.set_tree(self)
        self._children.append(child)

    @staticmethod
    def get_depth():
        return 0

    def get_tree_depth(self):
        return self._depth

    def check_tree_depth(self, depth):
        self._depth = depth if depth > self._depth else self._depth

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
        # if self._mutation_nodes_reviewed > self._nodes:
        #     self._mutate_chance = 1
        # else:
            # float(self._mutation_nodes_reviewed)
        self._mutate_chance = 0.10
        # self._mutation_nodes_reviewed += 1
        return self._mutate_chance

    def mutate(self):
        self._mutation_nodes_reviewed = 0
        chance = self.get_mutate_chance()
        mutating = random.random() <= chance
        representation = str(self)
        if mutating:
            # print 'Choose ',  self._root
            self._root = self.gen_node_(self, self._root.get_children(), True)

            self._root.mutate()

        if representation == str(self):
            self.mutate()

    def cross_over(self, target_node, new_node):
        if self._root.equals(target_node):
            self._root = new_node
            self._root.update_parent(self)
        else:
            self._root.cross_over(target_node, new_node)

    def select_node(self):
        self._mutation_nodes_reviewed = 0
        chance = self.get_mutate_chance()
        mutating = random.random() <= chance
        if mutating:
            # print 'Choose ',  self._root
            return self._root
        else:
            return self._root.select_node()

    @staticmethod
    def create_unity(parent, _non_terminals, _terminals, _min_depth, _max_depth, _terminals_chance, _non_terminals_chance):
        tree = Tree(individual=parent, terminals=_terminals, non_terminals=_non_terminals, min_depth=_min_depth, max_depth=_max_depth,
                    terminals_chance=_terminals_chance, non_terminals_chance=_non_terminals_chance, unity=True)
        tree._root = Add(parent=tree, children=[], mutating=True, gen=True)
        tree._root._depth = tree.get_depth() + 1
        tree._root._children.append(Multiply(parent=tree._root, children=[], mutating=True, gen=True))
        tree._root._depth = tree.get_depth() + 1
        tree._root._children[0]._children.append(ArrayVariableFloat(tree._root._children[0], 1.0, 0))
        tree._root._children[0]._children.append(ArrayVariableFloat(tree._root._children[0], 1.0, 0))
        tree._root._depth = tree.get_depth() + 1
        tree._root._children.append(Multiply(parent=tree._root, children=[], mutating=True, gen=True))
        tree._root._depth = tree.get_depth() + 1
        tree._root._children[1]._children.append(ArrayVariableFloat(tree._root._children[1], 1.0, 1))
        tree._root._children[1]._children.append(ArrayVariableFloat(tree._root._children[1], 1.0, 1))
        tree._root._depth = tree.get_depth() + 1
        return tree


class Node:
    def __init__(self, parent, children=[]):
        self._parent = parent
        self._tree = parent.get_tree()
        self._children = children
        self._depth = 0
        self._id = str(uuid.uuid1())

    def update_parent(self, parent):
        self._parent = parent
        self._tree = parent.get_tree()
        self._depth = parent.get_depth() + 1

        for child in self._children:
            child.update_parent(self)

    def get_id(self):
        return self._id

    def equals(self, target):
        return self._id == target.get_id()

    def mutate(self):
        for pos in range(len(self._children)):
            chance = self._tree.get_mutate_chance()
            mutating = random.random() <= chance
            if mutating:
                changing_node = self._children[pos]
                node = self._tree.gen_node_(self, changing_node.get_children(), True)
                # print 'Choose ',  changing_node
                # print 'Changed', node
                self._children[pos] = node
        for pos in range(len(self._children)):
            self._children[pos].mutate()

    def cross_over(self, target_node, new_node):
        for pos in range(self._children.__len__()):
            if self._children[pos].equals(target_node):
                self._children[pos] = new_node
                self._children[pos].update_parent(self)
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
    def __init__(self, parent):
        Node.__init__(self, parent)
        self._symbol = ''
        self._value = 0.0
        self._children = []

    def update_depth(self):
        self._depth = self._parent.get_depth() + 1
        self.get_tree().add_node()
        self.get_tree().check_tree_depth(self._depth)
        for child in self._children:
            child.update_depth()

    def __str__(self):
        representation = '(' + ' '
        for child in self._children:
                representation += child.__str__() + ' ' + self._symbol + ' '
        representation = representation.rstrip(self._symbol + ' ')
        return representation + ' )'

    def get_depth(self):
        return self._depth


class NonTerminalPair(NonTerminal):
    def __init__(self, parent, children=[], mutating=False, gen=False):
        NonTerminal.__init__(self, parent=parent)
        self._depth = parent.get_depth() + 1
        if not gen:
            if len(children) == 0:
                self._children.append(self._tree.gen_node(self))
                self._children.append(self._tree.gen_node(self))
            else:
                if len(children) < 2:
                    self._children = children[0:1]
                    self._children.append(self._tree.gen_node(self))
                else:
                    self._children = children[:2]

        self.get_tree().check_tree_depth(self._depth)

    def __str__(self):
        representation = '(' + ' '
        for child in self._children:
                representation += child.__str__() + ' ' + self._symbol + ' '
        representation = representation.rstrip(self._symbol + ' ')
        return representation + ' )'


class NonTerminalSingle(NonTerminal):
    def __init__(self, parent, children=[], mutating=False, gen=False):
        NonTerminal.__init__(self, parent=parent)
        Node.__init__(self, parent)
        self._symbol = ''
        self._value = 0.0
        self._children = []
        self._depth = parent.get_depth() + 1
        if not mutating and not gen:
            self._children.append(self._tree.gen_node(self))
        elif not gen:
            self._depth = parent.get_depth() + 1
            if len(children) > 0:
                self._children = children[:1]
            else:
                self._children.append(self._tree.gen_node(self))

        self.get_tree().check_tree_depth(self._depth)

    def __str__(self):
        representation = '(' + ' '
        representation += self._children[0].__str__() + self._symbol + ' '
        return representation + ' )'


class Pow2(NonTerminalSingle):
    def __init__(self, parent, children=[], mutating=False, gen=False):
        NonTerminalSingle.__init__(self, parent=parent, children=children, mutating=mutating, gen=gen)
        self._symbol = '^2'

    def eval(self):
        self._value = self._children[0].eval()
        self._value *= self._value
        return self._value


class Terminal(Node):
    def __init__(self, parent):
        Node.__init__(self, parent)
        self._value = 0.0
        self.update_depth()
    @staticmethod
    def gen_float():
        return math.trunc((1.0 / random.randint(1, 10))*10.00) / 10.0

    def eval(self):
        return self._value

    def add_child(self, child):
        raise Exception('Terminals could not have children')

    def get_children(self):
        return []

    def update_depth(self):
        self._depth = self._parent.get_depth() + 1
        self.get_tree().check_tree_depth(self._depth)


class FloatTerminal(Terminal):
    def __init__(self, parent):
        Terminal.__init__(self, parent)
        self._value = random.random()

    def __str__(self):
        return str(self._value)

    def eval(self):
        return self._value


class IntTerminal(Terminal):
    def __init__(self, parent):
        Terminal.__init__(self, parent)
        self._value = float(random.randint(1, 10))

    def __str__(self):
        return str(self._value)

    def eval(self):
        return self._value


class ArrayVariableFloat(Terminal):
    def __init__(self, parent, hard_value=None, index=None):
        Terminal.__init__(self, parent)
        self._individual = None
        self._variables = ''
        self.update_parent(parent)
        if hard_value is None:
            self._multiplier = random.randint(1, 10)
            self._index = int(random.choice(range(self._variables.__len__())))
        else:
            self._multiplier = hard_value
            self._index = index

    def update_parent(self, parent):
        Node.update_parent(self, parent)
        self._individual = self.get_tree().get_individual()
        self._variables = self._individual.get_variables()

    def __str__(self):
        return str(self._multiplier) + self._variables[self._index]

    def eval(self):
        data_row = self._individual.get_data_row()
        self._value = self._multiplier * data_row[self._index]

        return self._value


class ArrayVariableSkewed(Terminal):
    def __init__(self, parent, hard_value=None, index=None):
        Terminal.__init__(self, parent)
        self._individual = None
        self._variables = ''
        self._skew = float(random.randint(-10, 10))
        self.update_parent(parent)

        if hard_value is None:
            self._multiplier = random.randint(1, 10)
            self._index = int(random.choice(range(self._variables.__len__())))
        else:
            self._multiplier = hard_value
            self._index = index

    def update_parent(self, parent):
        Node.update_parent(self, parent)
        self._individual = self.get_tree().get_individual()
        self._variables = self._individual.get_variables()

    def __str__(self):
        return '(' + str(self._multiplier) + self._variables[self._index] + ' + ' + str(self._skew) + ')'

    def eval(self):
        data_row = self._individual.get_data_row()
        self._value = self._multiplier * data_row[self._index] + self._skew

        return self._value


class ArrayVariableTerminal(Terminal):
    def __init__(self, parent):
        Terminal.__init__(self, parent)
        self._individual = None
        self._variables = ''
        self.update_parent(parent)
        self._multiplier = random.randint(1, 10)
        self._index = int(random.choice(range(self._variables.__len__())))

    def update_parent(self, parent):
        Node.update_parent(self, parent)
        self._individual = self.get_tree().get_individual()
        self._variables = self._individual.get_variables()

    def __str__(self):
        return str(self._multiplier) + self._variables[self._index]

    def eval(self):
        data_row = self._individual.get_data_row()
        self._value = self._multiplier * data_row[self._index]

        return self._value


class Add (NonTerminalPair):
    def __init__(self, parent, children=[], mutating=False, gen=False):
        NonTerminalPair.__init__(self, parent, children, mutating, gen)
        self._symbol = '+'
        self._value = 0.0

    def eval(self):
        self._value = 0.0
        for child in self._children:
            self._value += child.eval()
        return self._value


class Multiply (NonTerminalPair):
    def __init__(self, parent, children=[], mutating=False, gen=False):
        NonTerminalPair.__init__(self, parent, children, mutating, gen)
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


class Subtract (NonTerminalPair):
    def __init__(self, parent, children=[], mutating=False, gen=False):
        NonTerminalPair.__init__(self, parent, children, mutating, gen)
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


class ProtectedDiv (NonTerminalPair):
    def __init__(self, parent, children=[], mutating=False, gen=False):
        NonTerminalPair.__init__(self, parent, children, mutating, gen)
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
