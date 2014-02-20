/*********************************************
 * OPL 12.6.0.0 Model
 * Author: thiago
 * Creation Date: 02/02/2014 at 08:20:34
 *********************************************/

tuple aresta {
  key string i;
  key string j;
  int l;
  int u;
};

{aresta} A = ...;
string s = ...;
string d = ...;

{string} V = {a.i | a in A} union {a.j | a in A};
int n = card(V); 
int M = n - 1;
int delta[v in V] = v == s ? 1 : (v == d ? -1 : 0);

int L = ...;
int U = ...;
  
dvar float+ x[V];
dvar boolean y[A];
dvar float+ z[A] in 0..1;
dvar boolean w[L..U];
dvar float+ t[V] in 0..M;

minimize
  sum(a in A) a.u * z[a] - 1;
subject to{
  forall(v in V)
    sum (a in A : a.i == v) y[a] - sum (a in A : a.j == v) y[a] == delta[v];
                
  forall(<i,j,l,u> in A)
    x[j] <= x[i] + l + (u - l) * y[<i,j,l,u>];
  
  x[s] == 0;  
    
  forall(i,j in V : <i,j> in A)
    if (<j,i> in A)
      t[i] - t[j] + M * y[<i,j>] + (M - 2) * y[<j,i>] <= M - 1;
    else 
      t[i] - t[j] + M * y[<i,j>]                      <= M - 1;
  
  t[s] == 0;
    
  forall (a in A) 
    z[a] <= y[a];
    
  forall (a in A) 
    z[a] >= sum(l in L..U) ((1.0 / l) * w[l]) - (1 - y[a]);
    
  sum(l in L..U) w[l] == 1;
    
  sum(l in L..U) l * w[l] == x[d];
    
  sum(a in A) a.u * z[a] - 1 >= (sum(a in A) a.u * y[a] - x[d]) / U;
  
  sum(a in A) a.u * z[a] - 1 <= (sum(a in A) a.u * y[a] - x[d]) / L;
};