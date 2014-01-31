execute PARAMS {
  cplex.tilim = 7200;
}
int numero_nos = ...;
int cenario = ...;
int numero_cenarios = 2; 

tuple aresta{
    string cidade_origem;
    string cidade_destino;
    float distancia[1..numero_cenarios];
};
{aresta} arestas = ...;
string origem = ...;
string destino = ...;
{string} cidades = {i.cidade_origem|i in arestas} union {i.cidade_destino|i in arestas};
//float minimos[1..numero_cenarios] = ...;
dvar boolean x[arestas];
//dvar float comprimento_caminho_robusto;
minimize
    //comprimento_caminho_robusto;
    sum(i in arestas)
		i.distancia[cenario] * x[i];
subject to{
    sum (j in arestas:j.cidade_origem==origem) x[j] == 1 + sum (k in arestas:k.cidade_destino==origem) x[k];
    sum (j in arestas:j.cidade_origem==destino) x[j] == -1 + sum (k in arestas:k.cidade_destino==destino) x[k];
    forall(cidade in cidades)
        if(cidade!=origem && cidade!=destino)
            sum (j in arestas:j.cidade_origem==cidade) x[j] == sum (k in arestas:k.cidade_destino==cidade) x[k];
    //  comprimento:
    //    forall(cenario in 1..numero_cenarios)
    //        comprimento_caminho_robusto >= (sum(i in arestas) i.distancia[cenario] * x[i]) - minimos[cenario]; 
};
execute {
    //writeln( comprimento.name," ",comprimento.UB," ",comprimento.LB," ",comprimento.dual," ",comprimento.slack);
    writeln("Nós = " + cplex.getNnodes());
    //writeln("Cenario" + cenario); 
    var i;
    var caminho = new Array()
    writeln("Caminho:");
    for(i in arestas)
        if(x[i] == 1)
            caminho[i.cidade_origem] = i.cidade_destino;
    i = origem;
    while(i != destino){
        writeln(i,"->",caminho[i]);
        i = caminho[i];
    }
}
