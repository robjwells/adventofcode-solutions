int: numIngredients;
set of int: Ingredients = 1..numIngredients;

array [Ingredients] of int: capacities;
array [Ingredients] of int: durabilities;
array [Ingredients] of int: flavors;
array [Ingredients] of int: textures;

array [Ingredients] of var int: amounts;
var int: total_cap = max(0, sum(i in Ingredients)(amounts[i] * capacities[i]));
var int: total_dur = max(0, sum(i in Ingredients)(amounts[i] * durabilities[i]));
var int: total_fla = max(0, sum(i in Ingredients)(amounts[i] * flavors[i]));
var int: total_tex = max(0, sum(i in Ingredients)(amounts[i] * textures[i]));

var int: score = total_cap * total_dur * total_fla * total_tex;

constraint forall(i in Ingredients)(amounts[i] >= 0);
constraint forall(i in Ingredients)(amounts[i] <= 100);
constraint sum(i in Ingredients)(amounts[i]) == 100;


numIngredients = 4;
capacities = [3, -3, -1, 0];
durabilities = [0, 3, 0, 0];
flavors = [0, 0, 4, -2];
textures = [-3, 0, 0, 2];


solve maximize score;


output [ "value: " ++ show(score) ++
         "\namounts: " ++ show(amounts) ++ 
         "\ntotals: " ++ show([total_cap, total_dur, total_fla, total_tex])];
         
