import pymzn

pymzn.config["minizinc"] = "/Applications/MiniZincIDE.app/Contents/Resources/minizinc"

n = 8

distances = [
    [0, 40, 54, 70, 99, 97, 67, 91],
    [40, 0, 135, 53, 129, 122, 24, 116],
    [54, 135, 0, 82, 75, 142, 129, 15],
    [70, 53, 82, 0, 15, 49, 71, 18],
    [99, 129, 75, 15, 0, 103, 60, 12],
    [97, 122, 142, 49, 103, 0, 58, 118],
    [67, 24, 129, 71, 60, 58, 0, 13],
    [91, 116, 15, 18, 12, 118, 13, 0],
]

template = """\
include "globals.mzn";

int: n; % number of cities
array[1..n, 1..n] of int: distances;

array[1..n] of var 1..n: tour;
constraint all_different(tour);

var int: tourCost = sum(i in 2..n)(distances[tour[i], tour[i - 1]]);
constraint tourCost > 0;
solve {{ mode }} tourCost;

output [ "tourCost=\(tourCost) \t tour=\(tour)" ];
"""

for part, mode in [("one", "minimize"), ("two", "maximize")]:
    solution = pymzn.minizinc(
        mzn=template,
        output_vars=["tourCost"],
        args=dict(mode=mode),
        data=dict(n=n, distances=distances),
    )[0]
    print(f'Part {part}: {solution["tourCost"]}')
