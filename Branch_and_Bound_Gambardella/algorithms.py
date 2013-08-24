from models import Digraph

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
            if j:
                self.complementoS.remove(j)
                self.s.append(j)
                adjacentesj = self.graph.adjacentes(j)
                for i in adjacentesj:
                    if i in self.complementoS:
                        shortest_path_in_node = min(self.shortest_path_in_node[i],self.shortest_path_in_node[j]+self.graph.get_cost_edge(j,i))
                        self.shortest_path_in_node[i] = shortest_path_in_node
                        if shortest_path_in_node == self.shortest_path_in_node[j]+self.graph.get_cost_edge(j,i):
                            self.antecessor[i] = j
            else:
                return

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

class BranchBoundRSP(object):
    def __init__(self, source, dest, digraph_interval):
        self.source = source
        self.dest = dest
        self.digraph_interval = digraph_interval
        self.edges_in = {self.source:[]}
        self.edges_out = {self.source:[]}
        self.lower_bound = {self.source:0}
        self.S = [self.source]

    def execute(self):
        ub_path, cost = self.get_shortest_path_cenario_ub_from_node(self.source)
        robust_cost = self.get_robust_cost_to_path_p(ub_path, cost)
        d_count = 1
        while self.S:
            shortest_lower_bound = 100000
            for node in self.S:
                if self.lower_bound[node] < shortest_lower_bound:
                    shortest_lower_bound = self.lower_bound[node]
                    d = node
            self.S.remove(d)
            path_d, cost_path_d = self.get_shortest_path_cenario_ub_from_node(d)
            if self.edges_in[d] != path_d:
                a = self.get_first_edge_in_p_d_and_not_in_in_d(path_d, d)
                d_one = d_count
                d_two = d_count + 1
                d_count += 2
                self.edges_in[d_one] = self.edges_in[d] 
                self.edges_out[d_one] = self.edges_out[d] + [a]
                path_d_one, cost_path_d_one = self.get_shortest_path_cenario_ub_from_node(d_one)
                if path_d_one:
                    robust_cost_d_one = self.get_robust_cost_to_path_p(path_d_one, cost_path_d_one)
                    if robust_cost_d_one < robust_cost:
                        robust_cost = robust_cost_d_one
                        ub_path = path_d_one[:]
                        for node in self.S:
                            if self.lower_bound[node] >= robust_cost:
                                self.S.remove(node)
                    lb_done = self.calculate_lower_bound(d_one)
                    if lb_done < robust_cost:
                        self.lower_bound[d_one] = lb_done
                        self.S.append(d_one)
                self.edges_in[d_two] = self.edges_in[d] + [a]
                self.edges_out[d_two] = self.edges_out[d]
        return robust_cost, ub_path

    def get_shortest_path_cenario_ub_from_node(self, node):
        edges_in = self.edges_in.get(node, [])
        edges_out = self.edges_out.get(node, [])
        graph = self._create_graph_cost_ub_from_node(node)
        if edges_in:
            source = edges_in[-1][1]
        else:
            source = self.source
        dijkstra = Dijkstra(graph, source)
        dijkstra.execute()
        try:
            path = edges_in + dijkstra.get_shortest_path(self.dest)
            cost = 0
            for edge in edges_in:
                cost += self.digraph_interval.get_upper_bound_edge(edge[0], edge[1])
            cost += dijkstra.get_cust_shortest_path_to(self.dest)
        except:
            path = []
            cost = 10000000000
        return path, cost


    def _create_graph_cost_ub_from_node(self, node):
        edges_in = self.edges_in.get(node, [])
        edges_out = self.edges_out.get(node, [])
        graph = Digraph()
        nodes = self.digraph_interval.edges_starts_node_i.keys()
        for source in nodes:
            edges_from_node = self.digraph_interval.edges_starts_node_i[source]
            for dest in edges_from_node.keys():
                if (source,dest) not in edges_in and (source,dest) not in edges_out:
                    graph.insert_edge(source, dest, self.digraph_interval.get_upper_bound_edge(source, dest))
        return graph

    def get_robust_cost_to_path_p(self, path, cost):
        graph_induse = self._create_graph_induse_path(path)
        dijkstra = Dijkstra(graph_induse, self.source)
        dijkstra.execute()
        cost_shortst_path = dijkstra.get_cust_shortest_path_to(self.dest)
        return (cost - cost_shortst_path) / float(cost_shortst_path)

    def _create_graph_induse_path(self, path):
        graph = Digraph()
        nodes = self.digraph_interval.edges_starts_node_i.keys()
        for source in nodes:
            edges_from_node = self.digraph_interval.edges_starts_node_i[source]
            for dest in edges_from_node.keys():
                if (source,dest) in path:
                    graph.insert_edge(source, dest, self.digraph_interval.get_upper_bound_edge(source, dest))
                else:
                    graph.insert_edge(source, dest, self.digraph_interval.get_lower_bound_edge(source, dest))
        return graph

    def get_first_edge_in_p_d_and_not_in_in_d(self, path, d):
        edges_in_d = self.edges_in[d]
        for edge in path:
            if edge not in edges_in_d:
                return edge
        return None

    def calculate_lower_bound(self, d):
        shortest_path, cost_shortest_path = self.get_shortest_path_cenario_ub_from_node(d)
        graph = self._create_graph_edges_out_d_in_lower_bound(d)
        dijkstra = Dijkstra(graph, self.source)
        dijkstra.execute()
        cost_shortest_path_out_d = dijkstra.get_cust_shortest_path_to(self.dest)
        return (cost_shortest_path - cost_shortest_path_out_d) / float(cost_shortest_path_out_d)

    def _create_graph_edges_out_d_in_lower_bound(self, d):
        graph = Digraph()
        nodes = self.digraph_interval.edges_starts_node_i.keys()
        for source in nodes:
            edges_from_node = self.digraph_interval.edges_starts_node_i[source]
            for dest in edges_from_node.keys():
                if (source,dest) in self.edges_out[d]:
                    graph.insert_edge(source, dest, self.digraph_interval.get_lower_bound_edge(source, dest))
                else:
                    graph.insert_edge(source, dest, self.digraph_interval.get_upper_bound_edge(source, dest))
        return graph