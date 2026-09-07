use clap::{Parser, Subcommand, ValueEnum};
use spd_validator::{
    OperationalStatus, Outcome, ValidationOptions, explain_requirement, validate_path,
};
use std::path::PathBuf;

#[derive(Parser)]
#[command(
    name = "spd-validator",
    version,
    about = "SPD Format 0.1 Reference Conformance Validator A"
)]
struct Cli {
    #[command(subcommand)]
    cmd: Cmd,
}

#[derive(Subcommand)]
enum Cmd {
    Validate {
        file: PathBuf,
        #[arg(long, value_enum, default_value = "text")]
        format: Format,
        #[arg(long)]
        epubcheck: Option<PathBuf>,
        #[arg(long, default_value_t = 536_870_912)]
        max_package_bytes: u64,
        #[arg(long, default_value_t = 268_435_456)]
        max_entry_bytes: u64,
        #[arg(long, default_value_t = 1_073_741_824)]
        max_total_uncompressed_bytes: u64,
    },
    Explain {
        id: String,
    },
}

#[derive(Clone, ValueEnum)]
enum Format {
    Text,
    Json,
}

fn main() {
    let code = match Cli::parse().cmd {
        Cmd::Explain { id } => match explain_requirement(&id) {
            Some(x) => {
                println!("{x}");
                0
            }
            None => {
                eprintln!("unknown requirement: {id}");
                5
            }
        },
        Cmd::Validate {
            file,
            format,
            epubcheck,
            max_package_bytes,
            max_entry_bytes,
            max_total_uncompressed_bytes,
        } => {
            let options = ValidationOptions {
                epubcheck,
                max_package_bytes,
                max_entry_bytes,
                max_total_uncompressed_bytes,
                ..Default::default()
            };
            let report = validate_path(file, &options);
            match format {
                Format::Json => println!("{}", serde_json::to_string_pretty(&report).unwrap()),
                Format::Text => {
                    println!("SPD Format 0.1 Validator A\n\nBase: {:?}", report.base);
                    for (key, value) in &report.capabilities {
                        println!("{key}: {value}");
                    }
                    for finding in &report.findings {
                        println!(
                            "\n{:?} {}\n{}{}",
                            finding.severity,
                            finding.requirement_id,
                            finding.message,
                            finding
                                .resource
                                .as_ref()
                                .map(|p| format!("\nResource: {p}"))
                                .unwrap_or_default()
                        );
                    }
                }
            }
            match report.operational_status {
                OperationalStatus::ResourceLimit => 3,
                OperationalStatus::InternalError => 4,
                OperationalStatus::ToolUnavailable | OperationalStatus::ToolError
                    if report.base == Outcome::NotTested =>
                {
                    2
                }
                _ if report.base == Outcome::Fail => 1,
                _ if report.base == Outcome::NotTested => 2,
                _ => 0,
            }
        }
    };
    std::process::exit(code)
}
