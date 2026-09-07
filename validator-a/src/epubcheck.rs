use crate::ToolEvidence;
use serde_json::json;
use sha2::{Digest, Sha256};
use std::{
    io::Read,
    path::Path,
    process::{Command, Stdio},
    thread,
    time::Duration,
};
use wait_timeout::ChildExt;

const OUTPUT_CAPTURE_LIMIT: usize = 1024 * 1024;

fn drain_bounded(mut stream: impl Read + Send + 'static) -> thread::JoinHandle<Vec<u8>> {
    thread::spawn(move || {
        let mut captured = Vec::new();
        let mut buffer = [0_u8; 8192];
        while let Ok(count) = stream.read(&mut buffer) {
            if count == 0 {
                break;
            }
            let remaining = OUTPUT_CAPTURE_LIMIT.saturating_sub(captured.len());
            captured.extend_from_slice(&buffer[..count.min(remaining)]);
        }
        captured
    })
}

fn command(tool: &Path) -> Command {
    if tool
        .extension()
        .and_then(|s| s.to_str())
        .is_some_and(|s| s.eq_ignore_ascii_case("jar"))
    {
        let mut cmd = Command::new("java");
        cmd.arg("-jar").arg(tool);
        cmd
    } else {
        Command::new(tool)
    }
}

fn capture(mut cmd: Command, timeout: Duration) -> Result<(i32, String, String), String> {
    let mut child = cmd
        .stdin(Stdio::null())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .map_err(|e| e.to_string())?;
    let stdout = child.stdout.take().map(drain_bounded);
    let stderr = child.stderr.take().map(drain_bounded);
    let status = match child.wait_timeout(timeout) {
        Ok(Some(s)) => Ok(s.code().unwrap_or(-1)),
        other => {
            let _ = child.kill();
            let _ = child.wait();
            Err(format!("external process did not complete: {other:?}"))
        }
    };
    let out = stdout.and_then(|h| h.join().ok()).unwrap_or_default();
    let err = stderr.and_then(|h| h.join().ok()).unwrap_or_default();
    Ok((
        status?,
        String::from_utf8_lossy(&out).into_owned(),
        String::from_utf8_lossy(&err).into_owned(),
    ))
}

pub fn run(tool: &Path, input: &Path, timeout: Duration) -> ToolEvidence {
    let mut result = ToolEvidence {
        name: "EPUBCheck".into(),
        profile: "EPUB 3.3".into(),
        outcome: "TOOL_ERROR".into(),
        ..Default::default()
    };
    result.detail.insert("executed".into(), json!(false));
    result
        .detail
        .insert("attributionVersion".into(), json!("0.1.2"));
    if let Ok(bytes) = std::fs::read(input) {
        result.detail.insert(
            "fixtureSha256".into(),
            json!(hex::encode(Sha256::digest(bytes))),
        );
    }
    let mut version_cmd = command(tool);
    version_cmd.arg("--version");
    let version = capture(version_cmd, Duration::from_secs(20));
    let valid_version = version.as_ref().is_ok_and(|(code, out, err)| {
        *code == 0 && format!("{out}{err}").contains("EPUBCheck v5.3.0")
    });
    if !valid_version {
        result.detail.insert(
            "skipReason".into(),
            json!(format!(
                "EPUBCheck 5.3.0 version verification failed: {version:?}"
            )),
        );
        return result;
    }
    result.version = Some("5.3.0".into());
    let mut cmd = command(tool);
    cmd.arg(input);
    match capture(cmd, timeout) {
        Ok((code, out, err)) => {
            let output = format!("{out}\n{err}");
            let completed = output.contains("EPUBCheck completed") && matches!(code, 0 | 1);
            let codes: std::collections::BTreeSet<_> =
                regex::Regex::new(r"\b[A-Z]{2,8}-[0-9]{3}[a-z]?\b")
                    .unwrap()
                    .find_iter(&output)
                    .map(|m| m.as_str().to_owned())
                    .collect();
            result.exit_code = Some(code);
            result.outcome = if code == 0 && completed {
                "PASS"
            } else if !completed
                || code < 0
                || !crate::policy::attribute(&output).contains(&"SPD-BASE-002".into())
            {
                "TOOL_ERROR"
            } else {
                "FAIL"
            }
            .into();
            result.detail.extend([
                ("executed".into(), json!(true)),
                ("skipReason".into(), json!(null)),
                ("diagnosticCodes".into(), json!(codes)),
                (
                    "normalizedSpdAttributionIds".into(),
                    json!(if completed {
                        crate::policy::attribute(&output)
                    } else {
                        Vec::<String>::new()
                    }),
                ),
                ("stdout".into(), json!(out)),
                ("stderr".into(), json!(err)),
            ]);
        }
        Err(err) => {
            result.detail.insert("skipReason".into(), json!(err));
        }
    }
    result
}
