import sys

from algorithms import BranchBoundRSP
from models import DigraphInterval

def main(name_file):
    f = open(name_file, 'r')
    lines = f.readlines()
    lines = lines[1:]
    digraph_interval = DigraphInterval()
    for line in lines:
        line = line.replace('\n', '')
        line = line.split(' ')
        if len(line) == 4:
            source = int(line[0])
            dest = int(line[1])
            lb = int(line[2])
            ub = int(line[3])
            digraph_interval.insert_edge(source, dest, lb, ub)
        else:
            source = int(line[0])
            dest =  int(line[1])
    branch_bound_RSP = BranchBoundRSP(source, dest, digraph_interval)
    cost, path, time_run = branch_bound_RSP.execute()
    print file_name, cost, time_run, path

if __name__ == '__main__':
    file_name = sys.argv[1]
    main(file_name)