from fabric.api import local
import os
import re
import tempfile
import shutil

import converte_entrada

PATH_OPL_RUN = "/opt/ibm/ILOG/CPLEX_Studio126/opl/bin/x86-64_linux/oplrun"
PATH_CPLEX = "/opt/ibm/ILOG/CPLEX_Studio126/cplex/bin/x86-64_linux/cplex"
PATH_MODELO_MATEMATICO_CMC = "modelo_matematico/intervalar_CMC.mod"
PATH_MODELO_MATEMATICO_RSP_RELATIVE_REGRET = "modelo_matematico/RSP_Relative_Regret.mod"
PATH_FILE_OPS = "modelo_matematico/notime.ops"

def clean_files():
    local('find . -name "*.rpt" -print0 | xargs -0 rm -f')
    local('find . -name "*.*~" -print0 | xargs -0 rm -f')
    local('find . -name "*.pyc" -print0 | xargs -0 rm -f')

def criar_arquivos_lp(name_file):
    with open(name_file, 'r') as f:
        arquivos_opl = f.read().splitlines()
    path_modelo_matematico, modelo_matematico = os.path.split(PATH_MODELO_MATEMATICO_RSP_RELATIVE_REGRET)
    modelo_matematico = os.path.splitext(modelo_matematico)[0]
    for arquivo_opl in arquivos_opl:
        path, file_name = os.path.split(arquivo_opl)
        os.system('%s -tune a.ops -tuneFixed %s %s %s' %(PATH_OPL_RUN,PATH_FILE_OPS, PATH_MODELO_MATEMATICO_RSP_RELATIVE_REGRET,arquivo_opl))
        shutil.copy2(os.path.join(path_modelo_matematico, modelo_matematico + '.lp'), os.path.join(path, file_name + '.lp'))
        os.remove(os.path.join(path_modelo_matematico, modelo_matematico + '.lp'))

def execute_lps(name_file):
    with open(name_file, 'r') as f:
        arquivos_lp = f.read().splitlines()
    lines = '''set timelimit 600
    set logfile %s
    read %s
    opt
    write %s
    quit'''
    #arquivos = ['instancias/formato_lp/grid/g_3x30_a_oplminimos.dat.lp', 'instancias/formato_lp/grid/g_3x30_b_oplminimos.dat.lp']
    for arquivo in arquivos_lp:
        arquivo_sem_extensao = arquivo[:-2]
        f = open('execute.cmd','w')
        f.write(lines %(arquivo_sem_extensao + 'log', arquivo, arquivo_sem_extensao + 'sol'))
        f.close()
        os.system('cat execute.cmd | %s' %(PATH_CPLEX))
    
def transforma_entradas_para_minmax_relativo(name_file):
    with open(name_file, 'r') as f:
        arquivosTestes = f.read().splitlines()
    arquivos_opl = converte_entrada.converte_grafos_para_opl(arquivosTestes)
    for arquivo in arquivos_opl:
        _transforma_entrada_para_minmax_relativo(arquivo)
        os.remove(arquivo)

def _transforma_entrada_para_minmax_relativo(arquivo_data,NUMERO_CENARIOS=2):
    encontra_valor_objetivos = re.compile(re.compile("OBJECTIVE: [\w]*\n"))
    objetivos = []
    for cenario in xrange(NUMERO_CENARIOS):
        arquivo_com_cenario = _cria_arquivo_com_cenario(arquivo_data,cenario+1)
        arquivo_resposta = tempfile.NamedTemporaryFile()
        os.system('%s %s %s > %s' %(PATH_OPL_RUN, PATH_MODELO_MATEMATICO_CMC, arquivo_com_cenario.name, arquivo_resposta.name))
        resposta = open(arquivo_resposta.name)
        valor_objetivo = encontra_valor_objetivos.findall(resposta.read())
        valor_objetivo = float(valor_objetivo[0].split(":")[1])
        objetivos.append(valor_objetivo)
        resposta.close()
    _cria_arquivo_com_minimos(arquivo_data,objetivos)

def _cria_arquivo_com_cenario(nome_arquivo_original,cenario):
    arquivo = open(nome_arquivo_original)
    arquivo_novo = tempfile.NamedTemporaryFile(delete=False)
    for linha in arquivo:
        arquivo_novo.write(linha)
    arquivo_novo.write('\ncenario = %i;' % cenario)
    arquivo.close()
    arquivo_novo.close()
    return arquivo_novo

def _cria_arquivo_com_minimos(nome_arquivo_original,minimos):
    arquivo = open(nome_arquivo_original)
    arquivo_novo = open(nome_arquivo_original[:-4] + 'minimos.dat','w')
    for linha in arquivo:
        linha = linha.replace('[','')
        linha = linha.replace(']','')
        arquivo_novo.write(linha)
    arquivo_novo.write('\nL = %s;' % int(minimos[0]))
    arquivo_novo.write('\nU = %s;' % int(minimos[1]))
    arquivo.close()
    arquivo_novo.close()