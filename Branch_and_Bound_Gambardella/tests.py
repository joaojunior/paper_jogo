import unittest

from models import DigraphInterval, Digraph
from algorithms import Dijkstra, BranchBoundRSP

class TestDigraphInterval(unittest.TestCase):
	def setUp(self):
		self.g = DigraphInterval()
		self.g.insert_edge(source=0, dest=1, lb=87, ub=10087)
		self.g.insert_edge(source=0, dest=2, lb=84, ub=10084)
		self.g.insert_edge(source=1, dest=0, lb=16, ub=10016)
		self.g.insert_edge(source=1, dest=3, lb=78, ub=10078)
		self.g.insert_edge(source=2, dest=0, lb=94, ub=10094)
		self.g.insert_edge(source=2, dest=3, lb=36, ub=10036)
		self.g.insert_edge(source=3, dest=1, lb=87, ub=10087)
		self.g.insert_edge(source=3, dest=2, lb=93, ub=10093)

	def test_verify_costs_edges_lower_bound(self):
		self.assertEqual(87, self.g.get_lower_bound_edge(source=0, dest=1))
		self.assertEqual(84, self.g.get_lower_bound_edge(source=0, dest=2))
		self.assertEqual(16, self.g.get_lower_bound_edge(source=1, dest=0))
		self.assertEqual(78, self.g.get_lower_bound_edge(source=1, dest=3))
		self.assertEqual(94, self.g.get_lower_bound_edge(source=2, dest=0))
		self.assertEqual(36, self.g.get_lower_bound_edge(source=2, dest=3))
		self.assertEqual(87, self.g.get_lower_bound_edge(source=3, dest=1))
		self.assertEqual(93, self.g.get_lower_bound_edge(source=3, dest=2))

	def test_verify_costs_edges_upper_bound(self):
		self.assertEqual(10087, self.g.get_upper_bound_edge(source=0, dest=1))
		self.assertEqual(10084, self.g.get_upper_bound_edge(source=0, dest=2))
		self.assertEqual(10016, self.g.get_upper_bound_edge(source=1, dest=0))
		self.assertEqual(10078, self.g.get_upper_bound_edge(source=1, dest=3))
		self.assertEqual(10094, self.g.get_upper_bound_edge(source=2, dest=0))
		self.assertEqual(10036, self.g.get_upper_bound_edge(source=2, dest=3))
		self.assertEqual(10087, self.g.get_upper_bound_edge(source=3, dest=1))
		self.assertEqual(10093, self.g.get_upper_bound_edge(source=3, dest=2))

class TestDijkstra(unittest.TestCase):
    def setUp(self):
        self.graph = Digraph()
        self.no0 = 0
        self.no1 = 1
        self.no2 = 2
        self.no3 = 3
        self.graph.insert_edge(self.no0,self.no1,7)
        self.graph.insert_edge(self.no0,self.no2,5)
        self.graph.insert_edge(self.no1,self.no3,2)
        self.graph.insert_edge(self.no1,self.no2,1)
        self.graph.insert_edge(self.no2,self.no1,1)
        self.graph.insert_edge(self.no2,self.no3,10)
        self.dijkstra = Dijkstra(self.graph,self.no0)

    def testgetNoComMenorDistancia(self):
        self.assertEqual(self.no2,self.dijkstra.get_node_with_shortest_distance())

    def testCustoMenorCaminhoAte3E5(self):
        self.dijkstra.execute()
        self.assertEqual(8,self.dijkstra.get_cust_shortest_path_to(self.no3))
        
    def testCustoMenorCaminhoAte2E5(self):
        self.dijkstra.execute()
        self.assertEqual(5,self.dijkstra.get_cust_shortest_path_to(self.no2))
        
    def testCustoMenorCaminhoAte1E3(self):
        self.dijkstra.execute()
        self.assertEqual(6,self.dijkstra.get_cust_shortest_path_to(self.no1))
        
    def testCustoMenorCaminhoAte0E0(self):
        self.dijkstra.execute()
        self.assertEqual(0,self.dijkstra.get_cust_shortest_path_to(self.no0))
        
    def testgetMenorCaminhoDe0Ate2(self):
        caminhoEsperado = [(self.no0,self.no2)] 
        cost = self.graph.get_cost_edge(self.no0,self.no2)
        path_result = self.dijkstra.get_shortest_path(self.no2)
        self.assertEqual(caminhoEsperado,self.dijkstra.get_shortest_path(self.no2))
        
    def testgetMenorCaminhoDe0Ate1(self):
        caminhoEsperado = [(self.no0,self.no1)]
        self.assertEqual(caminhoEsperado,self.dijkstra.get_shortest_path(self.no1))
        
    def testgetMenorCaminhoDe0Ate3(self):
        self.dijkstra.execute()
        caminhoEsperado = [(self.no0,self.no2),
                          (self.no2,self.no1),
                          (self.no1,self.no3)]
        cost_expect = self.graph.get_cost_edge(self.no0,self.no2) + self.graph.get_cost_edge(self.no2,self.no1) + self.graph.get_cost_edge(self.no1,self.no3)
        path, cost = self.dijkstra.get_shortest_path_and_cost_shortest_path(self.no3)
        self.assertEqual(caminhoEsperado,path)
        self.assertEqual(cost_expect,cost)

class TestBranchBoundRSP(unittest.TestCase):
    def setUp(self):
        self.g = DigraphInterval()
        self.g.insert_edge(source=0, dest=1, lb=87, ub=10087)
        self.g.insert_edge(source=0, dest=2, lb=84, ub=10084)
        self.g.insert_edge(source=1, dest=0, lb=16, ub=10016)
        self.g.insert_edge(source=1, dest=3, lb=78, ub=10078)
        self.g.insert_edge(source=2, dest=0, lb=94, ub=10094)
        self.g.insert_edge(source=2, dest=3, lb=36, ub=10036)
        self.g.insert_edge(source=3, dest=1, lb=87, ub=10087)
        self.g.insert_edge(source=3, dest=2, lb=93, ub=10093)
        self.branch_bound_rsp = BranchBoundRSP(0, 3, self.g)

    def test_get_shortest_path_cenario_ub_from_node_0(self):
        expect = [(0,2), (2,3)]
        path, cost = self.branch_bound_rsp.get_shortest_path_cenario_ub_from_node(0)
        self.assertListEqual(expect, path)
        self.assertEqual(10084 + 10036, cost)

    def test_get_shortest_path_cenario_ub_from_node_1(self):
        expect = [(0,1), (1,3)]
        self.branch_bound_rsp.edges_in.update({1:[(0, 1)]})
        path, cost = self.branch_bound_rsp.get_shortest_path_cenario_ub_from_node(1)
        self.assertListEqual(expect, path)
        self.assertEqual(10087 + 10078, cost)

    def test_get_shortest_path_cenario_ub_from_node_0_with_not_edge_0_2(self):
        expect = [(0,1), (1,3)]
        self.branch_bound_rsp.edges_out.update({0:[(0, 2)]})
        path, cost = self.branch_bound_rsp.get_shortest_path_cenario_ub_from_node(0)
        self.assertListEqual(expect, path)
        self.assertEqual(10087 + 10078, cost)

    def test_get_robust_cost_to_path_p(self):
        path = [(0,2), (2,3)]
        cost = 10084 + 10036
        expect = (cost - (87 + 78)) / float(87 + 78)
        self.assertEqual(expect, self.branch_bound_rsp.get_robust_cost_to_path_p(path, cost))

    def test_get_first_edge_in_p_d_and_not_in_in_d(self):
        expect = (1, 3)
        self.branch_bound_rsp.edges_in.update({0:[(0,1)]})
        self.assertEqual(expect, self.branch_bound_rsp.get_first_edge_in_p_d_and_not_in_in_d([(0,1), (1,3)], 0))

    def test_calculate_lower_bound(self):
        expect = 0
        self.assertEqual(expect, self.branch_bound_rsp.calculate_lower_bound(0))

    def test_apply_rule1(self):
        d = 0
        self.branch_bound_rsp.edges_in.update({d:[(0,1)]})
        out_d_expect = [(0,2)]
        self.branch_bound_rsp.apply_rule1(d)
        self.assertEqual(out_d_expect, self.branch_bound_rsp.edges_out[d])

    def test_apply_rule2(self):
        d = 0
        self.branch_bound_rsp.edges_in.update({d:[(0,2)]})
        out_d_expect = [(3,2)]
        self.branch_bound_rsp.apply_rule2(d)
        self.assertEqual(out_d_expect, self.branch_bound_rsp.edges_out[d])
    
    def test_execute(self):
        expect_solution = [(0, 2), (2, 3)]
        expect_cost = 120.93939393939394
        cost, solution = self.branch_bound_rsp.execute()
        self.assertEqual(expect_solution, solution)
        self.assertEqual(expect_cost, cost)

if __name__ == '__main__':
	unittest.main()