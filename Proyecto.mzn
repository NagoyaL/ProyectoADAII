% Parámetros
int: n; % Número de personas
int: m; % Número de opiniones posibles
array[1..m] of int: p; % Distribución inicial de personas por opinión
array[1..m] of float: v; % Valores de las opiniones
array[1..m,1..m] of float: c; % Costos de mover personas entre opiniones
array[1..m] of float: ce; % Costos extras si una opinión no es compartida inicialmente
float: ct; % Costo total máximo permitido
int: maxMovs; % Número máximo de movimientos

% Variables
array[1..m, 1..m] of var 0..n: x; % Número de personas que pasan de una opinión i a una j

% Restricciones
constraint sum(i in 1..m, j in 1..m where i != j)(x[i,j] * c[i,j]) <= ct; % Restricción de costo máximo


