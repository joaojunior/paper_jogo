execute PARAMS {
  cplex.tilim = 0;
  cplex.preind = 0;
  //cplex.prepass = 0;
  //cplex.mipinterval = 1;
  //cplex.heurfreq = -1;
  //cplex.mipsearch = 1;
  //cplex.submipnodelim = 10;
  //zerohalfcuts = -1;
  //cplex.cliques = -1;
  //cplex.relaxpreind = 0;
}

execute CPX_PARAM {
    //cplex.preind = 0;   // turns presolve off
    cplex.mipinterval = 1;
    //cplex.rootalg = 3;
}


int numero_cenarios = 2;
int numero_nos = ...; 

tuple aresta{
    key string cidade_origem;
    key string cidade_destino;
    float distancia[1..numero_cenarios];
};
{aresta} arestas = ...;
string origem = ...;
string destino = ...;
{string} cidades = {i.cidade_origem|i in arestas} union {i.cidade_destino|i in arestas};
int l = 1;
int u = 2;
int caminho_minimo_cenario_lb = ...;
int caminho_minimo_cenario_ub = ...;
range diferenca_SP_ub_lb = caminho_minimo_cenario_lb..caminho_minimo_cenario_ub;
dvar int+ sp[0..numero_nos-1];
dvar boolean x[arestas];
dvar boolean w[diferenca_SP_ub_lb];
dvar float+ z[arestas] in 0..1;
dvar int ordem_visita[intValue(origem)..intValue(destino)] in 0..numero_nos-1;
minimize
    sum(i in arestas) i.distancia[u] * z[i] - 1;
subject to{
    sum (j in arestas:j.cidade_origem==origem) x[j] == 1 + sum (k in arestas:k.cidade_destino==origem) x[k];
    sum (j in arestas:j.cidade_origem==destino) x[j] == -1 + sum (k in arestas:k.cidade_destino==destino) x[k];
    forall(cidade in cidades)
        if(cidade!=origem && cidade!=destino)
            sum (j in arestas:j.cidade_origem==cidade) x[j] == sum (k in arestas:k.cidade_destino==cidade) x[k];
    forall(aresta in arestas)
        sp[intValue(aresta.cidade_destino)] <= sp[intValue(aresta.cidade_origem)] + aresta.distancia[l] +(aresta.distancia[u] - aresta.distancia[l])*x[aresta];
    sp[intValue(origem)] == 0;
    forall (aresta in arestas:(aresta.cidade_origem!=origem)) ordem_visita[intValue(aresta.cidade_origem)] - ordem_visita[intValue(aresta.cidade_destino)] + (numero_nos-1)*x[aresta] + (numero_nos-3)*x[<aresta.cidade_destino,aresta.cidade_origem>] <= numero_nos - 2;
    forall(i in cidades)
        forall(j in cidades:j!=i)
            if(<i,j> in arestas)
                ordem_visita[intValue(i)] - ordem_visita[intValue(j)] + (numero_nos-1)*x[<i,j>] + (numero_nos-3)*x[<j,i>] <= numero_nos - 2;
    ordem_visita[intValue(origem)] == 0;
    forall (i in arestas) z[i] <= 1;
    forall (i in arestas) z[i] <= x[i];
    forall (i in arestas) (z[i] + (1 - x[i]))>= sum(t in diferenca_SP_ub_lb) ((1.0/t)*w[t]);
    sum(t in diferenca_SP_ub_lb) w[t] == 1;
    sum(t in diferenca_SP_ub_lb) t*w[t] == sp[intValue(destino)];
};


 
