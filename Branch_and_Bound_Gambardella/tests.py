import unittest

from models import DigraphInterval

class TestDigraphInterval(unittest.TestCase):
	def setUp(self):
		self.g = DigraphInterval(source=0, dest=3)
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

if __name__ == '__main__':
	unittest.main()