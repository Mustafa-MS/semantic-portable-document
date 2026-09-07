//! Read-only reference validator for SPD Format 0.1 RC1.

mod epubcheck;
mod model;
mod package;
mod passive;
mod policy;
mod strict_json;
mod validator;

pub use model::*;
pub use validator::{explain_requirement, validate_path, validate_reader};

pub const VALIDATOR_VERSION: &str = env!("CARGO_PKG_VERSION");
pub const SPEC_VERSION: &str = "Format 0.1 RC1";
pub const UNICODE_VERSION: (u8, u8, u8) = unicode_normalization::UNICODE_VERSION;
