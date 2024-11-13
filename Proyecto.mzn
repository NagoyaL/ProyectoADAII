% Parámetros de entrada
int: n; % Cantidad total de personas o capacidad máxima
int: m; % Número de entidades o ubicaciones
array[1..m] of float: v; % Valores de cada entidad, representando características o valores
array[1..m] of int: p; % Población inicial de cada entidad

% Costos de movimiento y de vaciar entidades
array[1..m, 1..m] of float: c; % Matriz de costos para mover personas entre entidades
array[1..m] of float: ce; % Costo asociado si una entidad está vacía

% Variable auxiliar para indicar si una entidad está vacía (1 si p[j] == 0, 0 en caso contrario)
array[1..m] of 0..1: esta_vacio = [if p[j] == 0 then 1 else 0 endif | j in 1..m];

% Variables de decisión
array[1..m, 1..m] of var 0..n: X; % Matriz que indica cuántas personas se mueven de i a j
array[1..m] of var 0..n: p_modificado; % Población modificada en cada entidad después de los movimientos

% Variables para definir la mediana
array[1..m] of var 0..1: es_mediana = [
    if (i = 1 \/ sum(j in 1..i-1)(p_modificado[j]) < n/2.0) /\ 
       sum(j in 1..i)(p_modificado[j]) >= n/2.0 
    then 1 else 0 endif 
    | i in 1..m
]; % Arreglo booleano para indicar si una entidad es la mediana (1 si es mediana, 0 si no)

% Valor de la mediana basado en el valor de la entidad que se marca como mediana
var float: valor_mediana = sum(i in 1..m)(v[i] * es_mediana[i]);

% Costo total del plan de movimientos, considerando los costos de transporte y costos de entidades vacías
var float: costo_total = sum(i in 1..m, j in 1..m)(
    (c[i,j] * (1 + p[i]/n) + ce[j] * esta_vacio[j]) * X[i,j]
);

% Polarización medida como la suma de la desviación absoluta de cada entidad respecto a la mediana
var float: polarizacion = sum(i in 1..m)(
    p_modificado[i] * abs(v[i] - valor_mediana)
);

% Restricciones

% Restricción de conservación de la población en cada entidad:
% La población final es la población inicial más las personas que llegan menos las personas que salen
constraint forall(i in 1..m)(
    p_modificado[i] = p[i] + sum(k in 1..m)(X[k,i]) - sum(k in 1..m)(X[i,k])
);

% Restricción para asegurar que la cantidad de personas que salen de cada entidad no supere su población inicial
constraint forall(i in 1..m)(
    sum(j in 1..m)(X[i,j]) <= p[i]
);

% Restricción de movimientos máximos permitidos
int: maxMovs; % Máximo de movimientos en función de la distancia
constraint sum(i in 1..m, j in 1..m)(
    abs(j - i) * X[i,j]
) <= maxMovs;

% Restricción para limitar el costo total del plan de movimientos
float: ct; % Costo total máximo permitido
constraint costo_total <= ct;

% Restricción para asegurar que solo haya una entidad marcada como mediana
constraint sum(i in 1..m)(es_mediana[i]) = 1;

% Cálculo del costo parcial de cada movimiento para fines de referencia o análisis
array[1..m, 1..m] of var float: costo_parcial = array2d(1..m, 1..m,
  [ (c[i,j] * (1 + p[i]/n) + ce[j] * esta_vacio[j]) * X[i,j]
    | i in 1..m, j in 1..m ]);

% Objetivo de optimización: minimizar la polarización
solve minimize polarizacion;

% Salida del modelo
output [
  "Distribucion inicial = \(p)\n",
  "Distribucion final = \(p_modificado)\n",
  "Polarizacion = \(polarizacion)\n"
];
