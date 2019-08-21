pub fn run() -> String {
    let title = "Day 2: I Was Told There Would Be No Math";
    let parsed_input = parse_input(get_input());

    format!(
        "{}\n{}\nPart one: {}\nPart two: {}",
        title,
        "=".repeat(title.len()),
        solve_part_one(&parsed_input),
        solve_part_two(&parsed_input),
    )
}

fn get_input() -> &'static str {
    let input: &'static str = include_str!("../../input/2015-02.txt");
    input
}

#[derive(PartialEq, Eq, Debug)]
struct Present {
    length: u32,
    width: u32,
    height: u32,
}

impl Present {
    fn new(length: u32, width: u32, height: u32) -> Present {
        Present {
            length: length,
            width: width,
            height: height,
        }
    }

    fn surface_area(&self) -> u32 {
        (2 * self.length * self.width)
            + (2 * self.width * self.height)
            + (2 * self.height * self.length)
    }

    fn slack(&self) -> u32 {
        let mut sides = vec![self.length, self.width, self.height];
        sides.sort();
        sides[0] * sides[1]
    }

    fn total_paper(&self) -> u32 {
        self.surface_area() + self.slack()
    }
}

fn parse_input(input: &str) -> Vec<Present> {
    input
        .lines()
        .map(|line: &str| {
            let split: Vec<u32> = line
                .split("x")
                .map(|num_str| num_str.parse::<u32>().expect("Parsing present failed"))
                .collect();
            assert!(split.len() == 3);
            Present::new(split[0], split[1], split[2])
        })
        .collect()
}

fn solve_part_one(input: &Vec<Present>) -> u32 {
    input.iter().map(Present::total_paper).sum()
}

fn solve_part_two(input: &Vec<Present>) -> u32 {
    42
}

mod tests {
    use super::*;

    #[test]
    fn test_parse() {
        assert_eq!(
            parse_input("1x2x3\n6x5x4\n"),
            vec![Present::new(1, 2, 3), Present::new(6, 5, 4),]
        );
    }

    #[test]
    fn test_surface_area() {
        assert_eq!(Present::new(2, 3, 4).surface_area(), 52);
        assert_eq!(Present::new(1, 1, 10).surface_area(), 42);
    }

    #[test]
    fn test_slack() {
        assert_eq!(Present::new(2, 3, 4).slack(), 6);
        assert_eq!(Present::new(1, 1, 10).slack(), 1);
    }

    #[test]
    fn test_total() {
        assert_eq!(Present::new(2, 3, 4).total_paper(), 58);
        assert_eq!(Present::new(1, 1, 10).total_paper(), 43);
    }

    #[test]
    fn test_known_part_one_result() {
        let parsed = parse_input(get_input());
        assert_eq!(solve_part_one(&parsed), 1588178);
    }
}
