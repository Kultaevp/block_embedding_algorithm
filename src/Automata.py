class Node:
    def __init__(self, val):
        self.val = val
        self.links = []

    def add_link(self, link):
        self.links.append(link)

    def __str__(self):
        node = "(%s):\n" % self.val
        for link in self.links:
            node += "\t" + link + "\n"
        return node

    def __add__(self, other):
        return str(self) + other

    def __radd__(self, other):
        return other + str(self)

    def equals(self, node):
        ok = (self.val == node.val)
        if len(self.links) == len(node.links):
            for i in range(len(self.links)):
                ok = ok and (self.links[i] == node.links[i])
            return ok
        else:
            return False

    def logger(self, block):
        pass


def embedding(block):
    pass


class Link:
    def __init__(self, from_node, etiquette, to_node):
        self.from_node = from_node
        self.etiquette = etiquette
        self.to_node = to_node

    def __str__(self):
        return "(%s --%s--> %s)" % (self.from_node.val, self.etiquette, self.to_node.val)

    def __add__(self, other):
        return str(self) + other

    def __radd__(self, other):
        return other + str(self)

    def equals(self, link):
        return (self.from_node == link.from_node) and (self.etiquette == link.etiquette) and (self.to_node == link.to_node)


class Automata:
    def __init__(self, initial_node, nodes, terminal_node):
        self.initial_node = initial_node
        self.nodes = nodes
        self.terminal_node = terminal_node

    @staticmethod
    def get_next_node(self, current_node, etiquette):
        for link in current_node.links:
            if link.etiquette == etiquette:
                return link.to_node
        return None

    def accepts(self, string):
        node = self.initial_node
        for character in string:
            node = self.get_next_node(node, character)
        return self.terminal_node.equals(node)

    def __str__(self):
        automata = "Initial node: %s\nTerminal node: %s\n" % (self.initial_node.val, self.terminal_node.val)
        for node in self.nodes:
            automata += node
        return automata

    def __add__(self, other):
        return str(self) + other

    def __radd__(self, other):
        return other + str(self)
