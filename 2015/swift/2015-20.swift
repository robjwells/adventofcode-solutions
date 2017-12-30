func totalPresents(for houseNumber: Int,
                   presentsPerElf: Int,
                   housesPerElf: Int? = nil) -> Int {
    let rangeLimit = Int(Double(houseNumber).squareRoot())
    let divisorRange = 1...rangeLimit
    let divisors = divisorRange.filter { candidate in
        houseNumber % candidate == 0
    }.map { smallDivisor in
        [smallDivisor, houseNumber / smallDivisor]
    }.flatMap {
        $0
    }

    var uniqueDivisors = Set(divisors)
    if let elfLimit = housesPerElf {
        uniqueDivisors = uniqueDivisors.filter { $0 * elfLimit >= houseNumber }
    }

    let presents = uniqueDivisors.map { $0 * presentsPerElf }.reduce(0, +)
    return presents
}


func firstHouse(withMorePresentsThan targetPresents: Int,
                headStart factor: Int = 50,
                presentsPerElf: Int = 10,
                housesPerElf: Int? = nil) -> Int {
    var presents = 0
    var houseNumber = targetPresents / factor

    while presents < targetPresents {
        houseNumber += 1
        presents = totalPresents(for: houseNumber,
                                 presentsPerElf: presentsPerElf,
                                 housesPerElf: housesPerElf)
    }
    return houseNumber
}

let puzzleInput = 36_000_000
let partOneResult = firstHouse(withMorePresentsThan: puzzleInput)
print("Part one:", partOneResult)

let partTwoResult = firstHouse(withMorePresentsThan: puzzleInput,
                               presentsPerElf: 11,
                               housesPerElf: 50)
print("Part two:", partTwoResult)
