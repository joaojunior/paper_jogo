execute PARAMS {
  cplex.tilim = 7200;
}
int cenario = ...;
int numero_cenarios = 2; 

tuple aresta{
    string cidade_origem;
    string cidade_destino;
    float distancia[1..numero_cenarios];
};
{aresta} A = ...;
string s = ...;
string d = ...;
{string} cidades = {i.cidade_origem|i in A} union {i.cidade_destino|i in A};
dvar boolean x[A];
minimize
    sum(i in A)
		i.distancia[cenario] * x[i];
subject to{
    sum (j in A:j.cidade_origem==s) x[j] == 1 + sum (k in A:k.cidade_destino==s) x[k];
    sum (j in A:j.cidade_origem==d) x[j] == -1 + sum (k in A:k.cidade_destino==d) x[k];
    forall(cidade in cidades)
        if(cidade!=s && cidade!=d)
            sum (j in A:j.cidade_origem==cidade) x[j] == sum (k in A:k.cidade_destino==cidade) x[k];
};
execute {
    writeln("Nós = " + cplex.getNnodes());
    var i;
    var caminho = new Array()
    writeln("Caminho:");
    for(i in A)
        if(x[i] == 1)
            caminho[i.cidade_origem] = i.cidade_destino;
    i = s;
    while(i != d){
        writeln(i,"->",caminho[i]);
        i = caminho[i];
    }
}
