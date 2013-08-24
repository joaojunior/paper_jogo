class DigraphInterval(object):
	LB = 0
	UB = 1
	def __init__(self, source, dest):
		self.source = source
		self.dest = dest
		self.edges_starts_node_i = {}

	def insert_edge(self, source, dest, lb, ub):
		edges_starts_node_i = self.edges_starts_node_i.get(source,{})
		edges_starts_node_i.update({dest:[lb,ub]})
		self.edges_starts_node_i[source] = edges_starts_node_i

	def get_lower_bound_edge(self, source, dest):
		return self.__get_cost_edge_in_cenario(source, dest, self.LB)

	def get_upper_bound_edge(self, source, dest):
		return self.__get_cost_edge_in_cenario(source, dest, self.UB)

	def __get_cost_edge_in_cenario(self, source, dest, cenario):
		edges_starts_node_source = self.edges_starts_node_i.get(source,{})
		edges_source_to_dest = edges_starts_node_source.get(dest, [])
		cost_cenario = edges_source_to_dest[cenario]
		return cost_cenario

class Digraph(object):
    def __init__(self):
        self.nodes = []
        self.edges_starts_node_i = {}

    def insert_edge(self, source, dest, cost=0):
        self.insert_node(source)
        self.insert_node(dest)
        edges_starts_node_i = self.edges_starts_node_i.get(source,{})
        edges_starts_node_i.update({dest:cost})
        self.edges_starts_node_i[source] = edges_starts_node_i
        
    def insert_node(self, node):
        if node not in self.nodes:
            self.nodes.append(node)
                    
    def adjacentes(self, node):
        adjacentes = []
        edges_starts_node_i = self.edges_starts_node_i.get(node,{})
        for dest in edges_starts_node_i.keys():
            adjacentes.append(dest)
        return adjacentes
        
    def get_cost_edge(self, source, dest):
        edges_starts_node_source = self.edges_starts_node_i.get(source,{})
        cost = edges_starts_node_source.get(dest, 0)
        return cost
        
    def get_edge(self,source, dest):
        edges_starts_node_i = self.edges_starts_node_i.get(source,{})
        aresta = Aresta(source,dest, self.get_cost_edge(source, dest))
        return aresta
