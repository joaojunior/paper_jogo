import os
import sys

PATH_CPLEX = "cplex.exe"

def execute_lps(name_files):
    for name_file in name_files:
        create_file_run(name_file)
        os.system('cat run.run | "%s"' %PATH_CPLEX)
        
def create_file_run(name_file):
    lines = 'set timelimit 7200\nset logfile %s\nread %s\noptimize\nwrite %s\ny\nquit\n' %('log'+name_file,name_file, name_file+'.sol')
    f = open('run.run','w')
    f.write(lines)
    f.close()
    
if __name__ == '__main__':
    if len(sys.argv) == 2:
        file_path = sys.argv[1]
        f = open(file_path,'r')
        name_files = []
        for line in f.readlines():
            line = line.replace('\n','')
            name_files.append(line)
        f.close()
        execute_lps(name_files)