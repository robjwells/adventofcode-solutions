let ingredients = [
    [3, 0, 0, -3, 2],
    [-3, 3, 0, 0, 9],
    [-1, 0, 4, 0, 1],
    [0, 0, -2, 2, 8],
]

func combo(length: Int, total: Int) -> AnyIterator<[Int]> {
    if length == 1 {
        return AnyIterator([[total]].makeIterator())
    }
    let combined = (0...total).flatMap { num in
        combo(length: length - 1, total: total - num).lazy.map { (list: [Int]) in
            [num] + list
        }
    }
    return AnyIterator(combined.makeIterator())
}

func combo_four(total: Int) -> AnyIterator<[Int]> {
    return combo(length: 4, total: total)
}

func scoreCookie(quantities: [Int], ingredients: [[Int]]) -> (score: Int, calories: Int) {
    let summed = zip(quantities, ingredients).map { teaspoons, ingredient in
        ingredient.map { teaspoons * $0 }
    }.reduce([0, 0, 0, 0, 0]) { accumulator, list in
        zip(accumulator, list).map(+)
    }.map { item in
        item <= 0 ? 0 : item
    }
    let calories = summed.last!
    let score = summed.prefix(4).reduce(1, *)
    return (score, calories)
}

let allScores: [(score: Int, calories: Int)] = combo_four(total: 100).map { quantities in
    scoreCookie(quantities: quantities, ingredients: ingredients)
}
let partOne = allScores.map { $0.score }.max()!
let partTwo = allScores.filter { $0.calories == 500 }.map { $0.score }.max()!

print("Part one: \(partOne)")
print("Part two: \(partTwo)")
