"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        self.vertices[v1].add(v2)

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.vertices[vertex_id]

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        # make a queue
        q = Queue()
        # enqueue our starting node
        q.enqueue(starting_vertex)

        # make a set to track if we've been here before
        visited = set()

        # while our queue isn't empty
        while q.size() > 0:
            ## dequeue whatever's at the front of our line, this is our current_node
            current_node = q.dequeue()
            ## if we haven't visited this node yet,
            if current_node not in visited:
                print(current_node)
                ### mark as visited
                visited.add(current_node)


                ### get its neighbors

                # res = [k for k in list(self.vertices.keys()) if k == current_node]
                
                neighbors = self.get_neighbors(current_node)
                ### for each of the neighbors,
                for neighbor in neighbors:
                    #### add to queue
                    q.enqueue(neighbor)
  
    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        s = Stack()
        s.push(starting_vertex)
        visited = set()

        while s.size() > 0:
            current_node = s.pop()
            if current_node not in visited:
                print(current_node)
                visited.add(current_node)
                neighbors = self.get_neighbors(current_node)
                for neighbor in neighbors:
                    s.push(neighbor)

    def dft_recursive(self, starting_vertex, visited=None):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """

        if visited is None:
            visited = set()
        
        visited.add(starting_vertex)
        print(starting_vertex)

        neighbors = self.get_neighbors(starting_vertex)

        for neighbor in neighbors:
            if neighbor not in visited:
                self.dft_recursive(neighbor, visited)

        
    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        q = Queue()                                   # make a queue
        q.enqueue([starting_vertex])                  # add first path, which in this first case, is the starting_vertex in list form
        
        while q.size() > 0:                           # keep running as long as there's stuff in the queue
            path = q.dequeue()                        # pop off latest path
            cur = path[-1]                            # point CUR variable at most recent path in list

            if cur == destination_vertex:             # base case = check if this cur node is where we want to end
                return path                           #if that's the case, return the path
            
            neighbors = self.get_neighbors(cur)       # get all the neighbors for this current node
            for neighbor in neighbors:                # loop through the neighbors
                path_copy = path.copy()               # make a copy of path
                path_copy.append(neighbor)            # add each of these neighbors to the list of paths
                q.enqueue(path_copy)                  # add the entire list to the queue 

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        s = Stack()                                   # make a queue
        s.push([starting_vertex])                  # add first path, which in this first case, is the starting_vertex in list form
        
        while s.size() > 0:                           # keep running as long as there's stuff in the queue
            path = s.pop()                        # pop off latest path
            cur = path[-1]                            # point CUR variable at most recent path in list

            if cur == destination_vertex:             # base case = check if this cur node is where we want to end
                return path                           #if that's the case, return the path
            
            neighbors = self.get_neighbors(cur)       # get all the neighbors for this current node
            for neighbor in neighbors:                # loop through the neighbors
                path_copy = path.copy()               # make a copy of path
                path_copy.append(neighbor)            # add each of these neighbors to the list of paths
                s.push(path_copy)                  # add the entire list to the queue 

    def dfs_recursive(self, starting_vertex, destination_vertex, visited=None, path=None):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        if visited == None:
            visited = set()

        if path == None:
            path = list()

        visited.add(starting_vertex)

        path_copy = path.copy()
        path_copy.append(starting_vertex)

        if starting_vertex == destination_vertex:
            return path_copy
          
        neighbors = self.get_neighbors(starting_vertex)
        for neighbor in neighbors:
            if neighbor not in visited:
                new_path = self.dfs_recursive(neighbor, destination_vertex, visited, path_copy)

                if new_path:
                    return new_path

if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print("NUMBER 1: ", graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    graph.dft(1)
    graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print("NUMBER 2: ", graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print("NUMBER 3: ", graph.dfs(1, 6))
    print("NUMBER 4: ", graph.dfs_recursive(1, 6))