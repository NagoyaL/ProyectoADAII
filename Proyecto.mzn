% Parámetros y Variables
int: n;
int: m;
array[1..m] of int: p;
array[1..m] of float: v;
array[1..m,1..m] of float: c;
array[1..m] of float: ce;
float: ct;
int: maxMovs;
array[1..m, 1..m] of var 0..n: x;

% Aproximación de la mediana (promedio ponderado)
float: approx_median = sum(i in 1..m)(p[i] * v[i]) / sum(i in 1..m)(p[i]);

% 1. Restricción de Costo Máximo
constraint sum(i in 1..m, j in 1..m where i != j)(
    x[i,j] * (c[i,j] * (1 + p[i] / n) + (if p[j] = 0 then ce[j] else 0 endif))
) <= ct;

% 2. Límite de Movimientos
constraint sum(i in 1..m, j in 1..m where i != j)(
    abs(j - i) * x[i,j]
) <= maxMovs;

% 3. Conservación de Personas
% La cantidad total de personas que se mueven desde cada opinión debe ser igual a la cantidad inicial.
constraint forall(i in 1..m)(
    sum(j in 1..m)(x[i,j]) = p[i]
);

% Función objetivo usando la aproximación de la mediana
solve minimize sum(i in 1..m)(
    p[i] * abs(v[i] - approx_median)
);