use crate::{Finding, Outcome, Severity, ValidationOptions};
use percent_encoding::percent_decode_str;
use sha2::{Digest, Sha256};
use std::{
    collections::{BTreeMap, HashSet},
    io::{Read, Seek, SeekFrom},
};
use unicode_normalization::UnicodeNormalization;
use zip::{CompressionMethod, ZipArchive};

#[derive(Debug, Clone)]
pub struct Entry {
    pub bytes: Vec<u8>,
    pub sha256: String,
    pub size: u64,
}
#[derive(Debug)]
pub struct PackageFacts {
    pub entries: BTreeMap<String, Entry>,
    pub findings: Vec<Finding>,
}

fn finding(resource: Option<String>, message: String) -> Finding {
    Finding {
        requirement_id: "SPD-BASE-002".into(),
        outcome: Outcome::Fail,
        severity: Severity::Error,
        capability: "Base".into(),
        stage: "package".into(),
        resource,
        node_id: None,
        revision_id: None,
        message,
        evidence: serde_json::Value::Null,
        source: "Validator A".into(),
    }
}

pub fn scan<R: Read + Seek>(mut reader: R, o: &ValidationOptions) -> Result<PackageFacts, String> {
    let size = reader.seek(SeekFrom::End(0)).map_err(|e| e.to_string())?;
    reader.seek(SeekFrom::Start(0)).map_err(|e| e.to_string())?;
    if size > o.max_package_bytes {
        return Err(format!(
            "RESOURCE_LIMIT package bytes {size} > {}",
            o.max_package_bytes
        ));
    }
    // Verify the local headers against central-directory identities before any
    // decompression. This prevents parser-dependent entry selection.
    let metadata = {
        let mut archive =
            ZipArchive::new(&mut reader).map_err(|e| format!("MALFORMED_INPUT ZIP: {e}"))?;
        if archive.len() > o.max_entries {
            return Err("RESOURCE_LIMIT entry count".into());
        }
        let mut records = Vec::new();
        for i in 0..archive.len() {
            let f = archive.by_index_raw(i).map_err(|e| e.to_string())?;
            records.push((
                f.header_start(),
                f.data_start(),
                f.compressed_size(),
                f.name_raw().to_vec(),
                match f.compression() {
                    CompressionMethod::Stored => 0,
                    CompressionMethod::Deflated => 8,
                    _ => u16::MAX,
                },
            ));
        }
        records
    };
    let mut ranges = Vec::new();
    for (offset, data, compressed, name, method) in metadata {
        reader
            .seek(SeekFrom::Start(offset))
            .map_err(|e| e.to_string())?;
        let mut header = [0u8; 30];
        reader.read_exact(&mut header).map_err(|e| e.to_string())?;
        let len = u16::from_le_bytes([header[26], header[27]]) as usize;
        let mut local_name = vec![0; len];
        reader
            .read_exact(&mut local_name)
            .map_err(|e| e.to_string())?;
        let end = data
            .checked_add(compressed)
            .ok_or("MALFORMED_INPUT ZIP bounds overflow")?;
        if &header[..4] != b"PK\x03\x04"
            || local_name != name
            || u16::from_le_bytes([header[8], header[9]]) != method
            || end > size
        {
            return Err("MALFORMED_INPUT inconsistent ZIP header/bounds".into());
        }
        ranges.push((offset, end));
    }
    ranges.sort_unstable();
    if ranges.windows(2).any(|r| r[0].1 > r[1].0) {
        return Err("MALFORMED_INPUT overlapping ZIP entries".into());
    }
    reader.seek(SeekFrom::Start(0)).map_err(|e| e.to_string())?;
    let mut z = ZipArchive::new(reader).map_err(|e| format!("MALFORMED_INPUT ZIP: {e}"))?;
    if z.len() > o.max_entries {
        return Err(format!(
            "RESOURCE_LIMIT entries {} > {}",
            z.len(),
            o.max_entries
        ));
    }
    let mut names = HashSet::new();
    let mut normalized = HashSet::new();
    let mut decoded_names = HashSet::new();
    let mut findings = Vec::new();
    let mut entries = BTreeMap::new();
    let mut total = 0u64;
    for i in 0..z.len() {
        let mut f = z.by_index(i).map_err(|e| e.to_string())?;
        let raw = f.name_raw();
        let name = match std::str::from_utf8(raw) {
            Ok(s) => s.to_owned(),
            Err(_) => {
                findings.push(finding(None, "ZIP entry name is not UTF-8".into()));
                continue;
            }
        };
        if !names.insert(name.clone()) {
            findings.push(finding(
                Some(name.clone()),
                "duplicate ZIP entry name".into(),
            ));
            continue;
        }
        let nfc: String = name.nfc().collect();
        if nfc != name {
            findings.push(finding(Some(name.clone()), "entry path is not NFC".into()))
        }
        if !normalized.insert(nfc) {
            findings.push(finding(
                Some(name.clone()),
                "entry paths collide after NFC normalization".into(),
            ))
        }
        if let Ok(decoded) = percent_decode_str(&name).decode_utf8()
            && !decoded_names.insert(decoded.nfc().collect::<String>())
        {
            findings.push(finding(
                Some(name.clone()),
                "percent-decoded entry identity collision".into(),
            ));
            let mut resource_finding = finding(
                Some(name.clone()),
                "ambiguous inventory path identity".into(),
            );
            resource_finding.requirement_id = "SPD-RES-002".into();
            findings.push(resource_finding);
        }
        let unsafe_path = name.starts_with('/')
            || name.starts_with('\\')
            || name.contains('\\')
            || name.contains("//")
            || name.split('/').any(|p| p == "." || p == "..")
            || name.contains(':')
            || name.chars().any(|c| c < ' ');
        if unsafe_path {
            findings.push(finding(Some(name.clone()), "unsafe OCF entry path".into()));
            continue;
        }
        if f.is_dir() {
            continue;
        }
        if !matches!(
            f.compression(),
            CompressionMethod::Stored | CompressionMethod::Deflated
        ) {
            findings.push(finding(
                Some(name.clone()),
                format!("unsupported compression method {:?}", f.compression()),
            ));
            continue;
        }
        if let Some(mode) = f.unix_mode()
            && !matches!(mode & 0o170000, 0 | 0o100000 | 0o040000)
        {
            findings.push(finding(
                Some(name.clone()),
                "symlink/device/special entry is prohibited".into(),
            ));
        }
        let declared = f.size();
        if declared > o.max_entry_bytes {
            return Err(format!("RESOURCE_LIMIT entry {name} bytes {declared}"));
        }
        total = total.saturating_add(declared);
        if total > o.max_total_uncompressed_bytes {
            return Err("RESOURCE_LIMIT total uncompressed bytes".into());
        }
        if f.compressed_size() > 0
            && declared / f.compressed_size().max(1) > o.max_compression_ratio
        {
            return Err(format!("RESOURCE_LIMIT compression ratio for {name}"));
        }
        let mut bytes = Vec::with_capacity(declared.min(16 * 1024 * 1024) as usize);
        (&mut f)
            .take(o.max_entry_bytes.saturating_add(1))
            .read_to_end(&mut bytes)
            .map_err(|e| e.to_string())?;
        if bytes.len() as u64 > o.max_entry_bytes {
            return Err("RESOURCE_LIMIT actual expanded entry bytes".into());
        }
        if bytes.len() as u64 != declared {
            return Err(format!("MALFORMED_INPUT size mismatch for {name}"));
        }
        let digest = format!("sha256:{}", hex::encode(Sha256::digest(&bytes)));
        entries.insert(
            name,
            Entry {
                bytes,
                sha256: digest,
                size: declared,
            },
        );
    }
    Ok(PackageFacts { entries, findings })
}
