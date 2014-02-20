import unittest

class TestConverte2OPL(unittest.TestCase):
    def test_converte2opl(self):
        linhas_arquivo_entrada = [['4','3'],['0','1','2','4'],['0','2','4','8'],['1','3','6','12'],['0','3']]
        linhas_arquivo_saida_esperada = ['s = "0";','d = "3";',
            'A = {<"0","1",[2,4]>,\n<"0","2",[4,8]>,\n<"1","3",[6,12]>};']
        converte2opl = Converte2OPL('arquivo.txt','arquivo_saida.txt')
        mocker = Mocker()
        obj = mocker.patch(converte2opl)
        obj.le_arquivo_entrada()
        mocker.result(linhas_arquivo_entrada)
        mocker.replay()
        obj.converte()
        self.assertListEqual(linhas_arquivo_saida_esperada,obj.linhas_arquivo_saida)

class Converte2OPL(object):
    def __init__(self,nome_arquivo_entrada,nome_arquivo_saida):
        self.nome_arquivo_entrada = nome_arquivo_entrada
        self.nome_arquivo_saida = nome_arquivo_saida
        self.linhas_arquivo_entrada = []
        self.linhas_arquivo_saida = []

    def converte(self):
        self.linhas_arquivo_entrada = self.le_arquivo_entrada()
        self.le_configuracoes()
        self.le_arestas()
        self.linhas_arquivo_saida.append('s = "%s";' % self.origem)
        self.linhas_arquivo_saida.append('d = "%s";' % self.destino)
        arestas = 'A = {'
        for aresta in self.arestas[:-1]:
            arestas += '<"%s","%s",[%s,%s]>,\n' %(aresta[0],aresta[1],aresta[2],aresta[3])
        aresta = self.arestas[-1]
        arestas += '<"%s","%s",[%s,%s]>};' %(aresta[0],aresta[1],aresta[2],aresta[3])
        self.linhas_arquivo_saida.append(arestas)
        self.escreve_arquivo_saida()        
        
    def le_arquivo_entrada(self):
        linhas_arquivo_entrada = []
        with open(self.nome_arquivo_entrada) as f:
            for line in f:
                line = line.strip()
                line = line.split()
                linhas_arquivo_entrada.append(line)
        return linhas_arquivo_entrada
        
    def le_configuracoes(self):
        self.numero_arestas = self.linhas_arquivo_entrada[0][1]
        self.origem = self.linhas_arquivo_entrada[-1][0]
        self.destino = self.linhas_arquivo_entrada[-1][1]

    def le_arestas(self):
        self.arestas = self.linhas_arquivo_entrada[1:-1]
             
        
    def escreve_arquivo_saida(self):
        arquivo_saida = open(self.nome_arquivo_saida,'w')
        arquivo_saida.write("\n".join(self.linhas_arquivo_saida))
        arquivo_saida.close()

def converte_grafos_para_opl(arquivos_data):
    arquivos_data_opl = []
    for arquivo in arquivos_data:
        nome_novo_arquivo = arquivo[:-4] + '_opl.dat'
        arquivos_data_opl.append(nome_novo_arquivo)
        converte2opl = Converte2OPL(arquivo,nome_novo_arquivo)
        converte2opl.converte()
    return arquivos_data_opl
    
if __name__ == '__main__':
    from mocker import Mocker
    unittest.main()