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

