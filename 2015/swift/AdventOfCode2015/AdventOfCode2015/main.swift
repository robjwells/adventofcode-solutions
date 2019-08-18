//
//  main.swift
//  AdventOfCode2015
//
//  Created by Rob Wells on 2019-08-18.
//  Copyright © 2019 Rob Wells. All rights reserved.
//

import Foundation

protocol AdventOfCodeSolution {
    static var year: Int { get }
    static var day: Int { get }
    
    static func solvePartOne(input: String) -> String
    static func solvePartTwo(input: String) -> String
}


func main() {
    
}

func formatInputFileName(year: Int, day: Int) -> String {
    return String(format: "%4d-%02d.txt", year, day)
}

func loadInputString(year: Int, day: Int) -> String {
    let fileName = formatInputFileName(year: year, day: day)
    let inputDirectory = "projects/adventofcode-solutions/\(year)/input/\(fileName)"
    let homeDirectory = FileManager.default.homeDirectoryForCurrentUser
    let maybeURL = URL(string: inputDirectory, relativeTo: homeDirectory)

    guard let fileURL = maybeURL?.absoluteURL else {
        print("Failed to open input file \(fileName).")
        exit(1)
    }
    
    do {
        return try String(contentsOf: fileURL)
    } catch {
        print("Error opening file \(fileName) for reading")
        exit(1)
    }
}

let result = loadInputString(year: 2015, day: 01)
print(result)

main()
