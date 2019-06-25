include "globals.mzn";

int: n;
array[1..n, 1..n] of int: happiness;
array[1..n] of var 1..n: seating;

var int: totalHappiness = sum(i in 1..n)
  (happiness[seating[i], seating[ (i - 2 + n) mod n + 1 ]] +
   happiness[seating[i], seating[ i mod n + 1 ]]);

constraint circuit(seating);

solve maximize totalHappiness;

output [ "totalHappiness=\(totalHappiness) \t seating=\(seating)" ]