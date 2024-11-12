int: n; 
int: m;
array[1..m] of float: v;
array[1..m] of int: p;

array[1..m, 1..m] of float: c;
array[1..m] of float: ce;

array[1..m] of 0..1: esta_vacio = [if p[j] == 0 then 1 else 0 endif | j in 1..m];

array[1..m, 1..m] of var 0..n: X;
array[1..m] of var 0..n: p_modificado;

array[1..m] of var 0..1: es_mediana = [if (i = 1 \/ sum(j in 1..i-1)(p_modificado[j]) < n/2.0) /\ sum(j in 1..i)(p_modificado[j]) >= n/2.0 then 1 else 0 endif | i in 1..m];

var float: valor_mediana = sum(i in 1..m)(v[i] * es_mediana[i]);
var float: costo_total = sum(i in 1..m, j in 1..m)(
    (c[i,j] * (1 + p[i]/n) + ce[j] * esta_vacio[j]) * X[i,j]
);
var float: polarizacion = sum(i in 1..m)(
    p_modificado[i] * abs(v[i] - valor_mediana)
);

constraint forall(i in 1..m)(
    p_modificado[i] = p[i] + sum(k in 1..m)(X[k,i]) - sum(k in 1..m)(X[i,k])
);

constraint forall(i in 1..m)(
    sum(j in 1..m)(X[i,j]) <= p[i]
);

int: maxMovs;
constraint sum(i in 1..m, j in 1..m)(
    abs(j - i) * X[i,j]
) <= maxMovs;

float: ct; 
constraint costo_total <= ct;

constraint sum(i in 1..m)(es_mediana[i]) = 1;

array[1..m, 1..m] of var float: costo_parcial = array2d(1..m, 1..m,
  [ (c[i,j] * (1 + p[i]/n) + ce[j] * esta_vacio[j]) * X[i,j]
    | i in 1..m, j in 1..m ]);

solve minimize polarizacion;

output [

  "Distribucion inicial = \(p)\n",
  "Distribucion final = \(p_modificado)\n\n",
  "Polarizacion = \(polarizacion)\n"
]