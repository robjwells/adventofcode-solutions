mod aoc_2015_01;

fn main() {
    let days = [aoc_2015_01::run];
    if let Some(day_arg) = std::env::args().nth(1) {
        // Try to run specific day's solution
        match day_arg.parse::<usize>() {
            // Day is in bounds for solutions in `days` array
            Ok(day) if { day <= days.len() && day > 0 } => {
                println!("{}", days[day - 1]());
            }
            // Day is out of bounds for `days` array
            Ok(_) => {
                println!(
                    "Given day ({}) is out of bounds for currently registered solutions.",
                    day_arg
                );
                std::process::exit(1);
            }
            // Could not parse the day argument given
            Err(e) => {
                println!("Cannot parse argument ({}) as a number. {}", day_arg, e);
                std::process::exit(1);
            }
        }
    } else {
        // Run all days
        days.iter().for_each(|day| println!("{}", day()));
    }
}
