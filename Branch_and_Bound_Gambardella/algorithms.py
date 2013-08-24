class Dijkstra(object):
    SHORTEST_DISTANCE = 10000000000000000000
    def __init__(self,graph, source):
        self.graph = graph
        self.source = source
        self.s = [source]
        self.complementoS = graph.nodes[:]
        self.complementoS.remove(source)
        self.shortest_path_in_node = {}
        self.antecessor = {}
        self.start_shortest_distance()

    def start_shortest_distance(self):
        self.shortest_path_in_node[self.source] = 0
        adjacentessource = self.graph.adjacentes(self.source)
        for no in self.complementoS:
            if no in adjacentessource:
                self.shortest_path_in_node[no] = self.graph.get_cost_edge(self.source,no)
                self.antecessor[no] = self.source
            else:
                self.shortest_path_in_node[no] = self.SHORTEST_DISTANCE

    def get_cust_shortest_path_to(self,no):
        return self.shortest_path_in_node[no]

    def execute(self):
        while(self.complementoS):
            j = self.get_node_with_shortest_distance()
            self.complementoS.remove(j)
            self.s.append(j)
            adjacentesj = self.graph.adjacentes(j)
            for i in adjacentesj:
                if i in self.complementoS:
                    shortest_path_in_node = min(self.shortest_path_in_node[i],self.shortest_path_in_node[j]+self.graph.get_cost_edge(j,i))
                    self.shortest_path_in_node[i] = shortest_path_in_node
                    if shortest_path_in_node == self.shortest_path_in_node[j]+self.graph.get_cost_edge(j,i):
                        self.antecessor[i] = j

    def get_node_with_shortest_distance(self):
        shortest_path_in_node = self.SHORTEST_DISTANCE
        noshortest_path_in_node = None
        for no in self.shortest_path_in_node:
            if self.shortest_path_in_node[no] < shortest_path_in_node and no in self.complementoS:
                noshortest_path_in_node = no
                shortest_path_in_node = self.shortest_path_in_node[no]
        return noshortest_path_in_node

    def get_shortest_path(self, dest):
        edges = []
        node = dest
        while self.antecessor[node] != self.source:
            origem = self.antecessor[node]
            edges.append((origem,node))
            node = origem
        edges.append((self.source,node))
        edges.reverse()
        return edges

    def get_shortest_path_and_cost_shortest_path(self, node):
        path = self.get_shortest_path(node)
        cost = self.get_cust_shortest_path_to(node)
        return path, cost