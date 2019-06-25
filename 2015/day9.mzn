include "globals.mzn";

int: n; % number of cities
array[1..n, 1..n] of int: distances;

array[1..n] of var 1..n: tour;
constraint all_different(tour);

var int: tourCost = sum(i in 2..n)(distances[tour[i], tour[i - 1]]);
constraint tourCost > 0;
solve maximize tourCost;

output [ "tourCost=\(tourCost) \t tour=\(tour)" ];
