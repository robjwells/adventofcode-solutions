//
//  AdventOfCode2015Tests.swift
//  AdventOfCode2015Tests
//
//  Created by Rob Wells on 2019-08-18.
//  Copyright © 2019 Rob Wells. All rights reserved.
//

import XCTest

class AdventOfCode2015Tests: XCTestCase {
    
    func testFormatFileNameZeroPadded() {
        let result = formatInputFileName(year: 2015, day: 1)
        XCTAssertEqual("2015-01.txt", result)
    }
    
    func testFormatFileNameTwoDigitDay() {
        let result = formatInputFileName(year: 2015, day: 11)
        XCTAssertEqual("2015-11.txt", result)
    }
    
    
    func testLoadInputString() {
        let expected = """
            Sugar: capacity 3, durability 0, flavor 0, texture -3, calories 2
            Sprinkles: capacity -3, durability 3, flavor 0, texture 0, calories 9
            Candy: capacity -1, durability 0, flavor 4, texture 0, calories 1
            Chocolate: capacity 0, durability 0, flavor -2, texture 2, calories 8

            """
        XCTAssertEqual(loadInputString(year: 2015, day: 15), expected)
    }
    
}
