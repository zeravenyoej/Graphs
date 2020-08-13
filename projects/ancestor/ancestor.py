class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        if vertex_id not in self.vertices:
            self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        self.vertices[v1].add(v2)
    
    def get_neighbors(self, vertex):
        return self.vertices[vertex]


def build_graph(ancestors):
    g = Graph()
    for parent, child in ancestors:
        g.add_vertex(parent)
        g.add_vertex(child)
        g.add_edge(child, parent)
    return g


def earliest_ancestor(ancestors, starting_node):
    graph = build_graph(ancestors)

    s = Stack()
    visited = set()
    s.push([starting_node])

    longest_path = [starting_node]
    aged_one = -1
    
    while s.size() > 0:
        path = s.pop()
        current_node = path[-1]

        if (len(path) > len(longest_path)) or (len(path) == len(longest_path) and current_node < aged_one):
            longest_path = path
            aged_one = longest_path[-1]

        if current_node not in visited:
            visited.add(current_node)
            parents = graph.get_neighbors(current_node)

            for parent in parents: 
                new_path = list(path)
                new_path.append(parent)
                s.push(new_path)

    return aged_one