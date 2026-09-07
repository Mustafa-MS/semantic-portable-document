#![no_main]
use libfuzzer_sys::fuzz_target;
use spd_validator::{validate_reader, ValidationOptions};
use std::io::Cursor;

fuzz_target!(|data: &[u8]| {
    let options = ValidationOptions {
        max_package_bytes: 2 * 1024 * 1024,
        max_entry_bytes: 512 * 1024,
        max_total_uncompressed_bytes: 4 * 1024 * 1024,
        max_entries: 256,
        ..Default::default()
    };
    let _ = validate_reader(Cursor::new(data), &options);
});
