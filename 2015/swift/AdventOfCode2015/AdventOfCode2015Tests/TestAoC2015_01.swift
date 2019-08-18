//
//  201501Test.swift
//  AdventOfCode2015Tests
//
//  Created by Rob Wells on 2019-08-18.
//  Copyright © 2019 Rob Wells. All rights reserved.
//

import XCTest

class TestAoC2015_01: XCTestCase {
    static let input: String = loadInputString(year: 2015, day: 1)
    
    func testKnownResultForPartOne() {
        XCTAssertEqual(
            AoC2015_01.solvePartOne(input: TestAoC2015_01.input),
            "280"
        )
    }
    
    func testKnownResultForPartTwo() {
        XCTAssertEqual(
            AoC2015_01.solvePartTwo(input: TestAoC2015_01.input),
            "1797"
        )
    }
}
