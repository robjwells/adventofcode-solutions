//
//  AoC2015-01.swift
//  AdventOfCode2015
//
//  Created by Rob Wells on 2019-08-18.
//  Copyright © 2019 Rob Wells. All rights reserved.
//

import Foundation

struct AoC2015_01: AdventOfCodeSolution {
    static var year: Int = 2015
    static var day: Int = 1
    
    static func solvePartOne(input: String) -> String {
        let result = input.reduce(0) { floor, direction in
            direction == "(" ? floor + 1 : floor - 1
        }
        return "\(result)"
    }
    
    static func solvePartTwo(input: String) -> String {
        var floor = 0
        for (index, character) in input.enumerated() {
            floor += (character == "(" ? 1 : -1)
            if floor == -1 {
                return "\(index + 1)"  // Problem starts from position 1
            }
        }
        return "Did not enter basement, reached floor \(floor)"
    }
}
