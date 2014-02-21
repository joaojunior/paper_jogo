import unittest
import re
import tempfile

class ReadSolution(object):
    def read_file(self, name_file):
        f = open(name_file, 'r')
        self.content = f.read()
        f.close()

    def get_instance(self):
        regex = re.compile(re.compile("Problem ['-/_ .\w]*\n")) 
        name_instance = regex.findall(self.content)[0]
        name_instance = name_instance.replace("Problem '", '')
        name_instance = name_instance.replace("' read.\n", '')
        return name_instance
        
    def get_objective_value(self):
        encontra_valor_objetivo = re.compile(re.compile("Objective = [-+ .\w]*\n")) 
        valor_objetivo = encontra_valor_objetivo.findall(self.content)
        if valor_objetivo:
            objective_value = valor_objetivo[0].split('=')[1]
            objective_value = objective_value.replace(' ', '')
            objective_value = objective_value.replace('\n', '')
        else:
            objective_value = 'No solution exists'
        return objective_value
    
    def get_solution_time(self):
        regex = re.compile(re.compile("Solution time = [- .\w]*sec")) 
        solution_time = regex.findall(self.content)
        solution_time = solution_time[0].split('=')[1]
        solution_time = solution_time.replace(' ', '')
        solution_time = solution_time.replace('sec', '')
        return solution_time
    
    def get_nodes(self):
        regex = re.compile(re.compile("Nodes = [0-9]*[ \n]")) 
        nodes = regex.findall(self.content)
        nodes = nodes[0].split('=')[1]
        nodes = nodes.replace(' ', '')
        nodes = nodes.replace('\n', '')
        return nodes
    
    def get_gap(self):
        regex = re.compile(re.compile("(gap = [- ,.\w]*%)")) 
        gap = regex.findall(self.content)
        if gap:
            gap = gap[0].split(',')[1]
            gap = gap.replace(' ', '')
        else:
            gap = '0'
        return gap
    
    def get_lb(self):
        regex = re.compile(re.compile("Current MIP best bound =  [- .\w]* ")) 
        lb = regex.findall(self.content)
        if lb:
            lb = lb[0].split('=')[1]
            lb = lb.replace(' ', '')
        else:
            lb = '0'
        return lb
    
    def get_results(self):
        return self.get_instance(), self.get_lb(), self.get_objective_value(), self.get_gap(), self.get_solution_time(), self.get_nodes()

class TestReadSolution(unittest.TestCase):
    def setUp(self):
        file_content_not_complete = """Problem 'instancias/formato_lp/grid/g_3x30_a_oplminimos.dat.lp' read.
MIP - Integer optimal solution:  Objective =  4.9776007964e-03
Solution time =    0.32 sec.  Iterations = 466  Nodes = 0
Deterministic time = 228.86 ticks  (718.48 ticks/sec)


Incumbent solution written to file 'instancias/formato_lp/grid/g_3x30_a_oplminimos.dat.sol'.
"""
        file_content_complete = """Problem 'instancias/formato_lp/grid/g_10x100_b_oplminimos.dat.lp' read.
MIP - Time limit exceeded, integer feasible:  Objective =  5.5115936695e-01
Current MIP best bound =  2.9302992071e-01 (gap = 0.258129, 46.83%)
Solution time =  600.42 sec.  Iterations = 19349  Nodes = 0 (1)
Deterministic time = 629690.37 ticks  (1048.75 ticks/sec)


Incumbent solution written to file 'instancias/formato_lp/grid/g_10x100_b_oplminimos.dat.sol'.

        """
        file_not_complete = tempfile.NamedTemporaryFile(delete=False)
        file_not_complete.writelines(file_content_not_complete)
        file_not_complete.close()
        self.file_complete = tempfile.NamedTemporaryFile(delete=False)
        self.file_complete.writelines(file_content_complete)
        self.file_complete.close()
        self.read_solution = ReadSolution()
        self.read_solution.read_file(file_not_complete.name)
    
    def test_get_instance(self):
        expect = 'instancias/formato_lp/grid/g_3x30_a_oplminimos.dat.lp'
        self.assertEqual(expect, self.read_solution.get_instance())
        
    def test_get_objective_value(self):
        expect = '4.9776007964e-03'
        self.assertEqual(expect, self.read_solution.get_objective_value())
    
    def test_get_solution_time(self):
        expect = '0.32'
        self.assertEqual(expect, self.read_solution.get_solution_time())
        
    def test_get_nodes(self):
        expect = '0'
        self.assertEqual(expect, self.read_solution.get_nodes())
        
    def test_get_gap(self):
        expect = '0'
        self.assertEqual(expect, self.read_solution.get_gap())
        
    def test_get_lb(self):
        expect = '0'
        self.assertEqual(expect, self.read_solution.get_lb())
        
    def test_get_gap_file_complete(self):
        self.read_solution = ReadSolution()
        self.read_solution.read_file(self.file_complete.name)
        expect = '46.83%'
        self.assertEqual(expect, self.read_solution.get_gap())
        
    def test_get_lb_file_complete(self):
        self.read_solution = ReadSolution()
        self.read_solution.read_file(self.file_complete.name)
        expect = '2.9302992071e-01'
        self.assertEqual(expect, self.read_solution.get_lb())
        
    def test_get_results_file_not_complete(self):
        expect = ('instancias/formato_lp/grid/g_3x30_a_oplminimos.dat.lp', '0', '4.9776007964e-03', '0', '0.32','0')
        self.assertEqual(expect, self.read_solution.get_results())
        
    def test_get_results_file_complete(self):
        self.read_solution = ReadSolution()
        self.read_solution.read_file(self.file_complete.name)
        expect = ('instancias/formato_lp/grid/g_10x100_b_oplminimos.dat.lp', '2.9302992071e-01', '5.5115936695e-01', '46.83%', '600.42','0')
        self.assertEqual(expect, self.read_solution.get_results())
        
if __name__ == '__main__':
    unittest.main()
