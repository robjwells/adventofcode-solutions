pub fn run() -> String {
    let title = "Day 1: Not Quite Lisp";
    let input = get_input();
    format!(
        "{}\n{}\nPart one: {}\nPart two: {}",
        title,
        "=".repeat(title.len()),
        solve_part_one(&input),
        solve_part_two(&input).unwrap()
    )
}

fn get_input() -> &'static str {
    let input: &'static str = include_str!("../../input/2015-01.txt");
    input
}

fn direction_to_integer(direction: char) -> i32 {
    if direction == '(' {
        1
    } else {
        -1
    }
}

/// Report the floor number that Santa finishes on
fn solve_part_one(input: &str) -> i32 {
    input.chars().map(direction_to_integer).sum()
}

/// Report the instruction number which puts Santa in the basement
fn solve_part_two(input: &str) -> Option<usize> {
    let mut floor: i32 = 0;
    for (index, direction) in input.chars().enumerate() {
        floor += direction_to_integer(direction);
        if floor == -1 {
            return Some(index + 1); // Puzzle starts counting at 1
        }
    }
    None // Did not enter the basement
}

mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        vec![
            ("(())", 0),
            ("()()", 0),
            ("(((", 3),
            ("(()(()(", 3),
            ("))(((((", 3),
            ("())", -1),
            ("))(", -1),
            (")))", -3),
            (")())())", -3),
        ]
        .iter()
        .for_each(|(input, expected)| {
            assert_eq!(solve_part_one(input), *expected);
        });
    }

    #[test]
    fn test_part_two() {
        vec![(")", 1), ("()())", 5)]
            .iter()
            .for_each(|(input, expected)| {
                assert_eq!(solve_part_two(input).unwrap(), *expected);
            });
    }

    #[test]
    fn test_part_one_known_result() {
        assert_eq!(solve_part_one(get_input()), 280);
    }

    #[test]
    fn test_part_two_known_result() {
        assert_eq!(solve_part_two(get_input()).unwrap(), 1797);
    }
}
