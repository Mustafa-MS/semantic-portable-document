//! Passive resource inspection using CSS Syntax tokens and namespace-aware XML.
use crate::{Finding, Outcome, Severity, package::Entry};
use cssparser::{Parser, ParserInput, Token};
use percent_encoding::percent_decode_str;
use roxmltree::Document;
use std::collections::{BTreeMap, BTreeSet};
use unicode_normalization::UnicodeNormalization;

const SVG: &str = "http://www.w3.org/2000/svg";
const HTML: &str = "http://www.w3.org/1999/xhtml";
const MATH: &str = "http://www.w3.org/1998/Math/MathML";

#[derive(Default)]
struct CssFacts {
    urls: Vec<(String, &'static str, bool)>,
    code: bool,
    local_font: bool,
    unresolved: bool,
    malformed: bool,
    limited: bool,
}

fn tokens(
    input: &mut Parser<'_, '_>,
    role: &'static str,
    strings: bool,
    depth: usize,
    out: &mut CssFacts,
) {
    if depth > 128 {
        out.limited = true;
        return;
    }
    let mut import = false;
    let mut font = false;
    while let Ok(token) = input.next_including_whitespace_and_comments().cloned() {
        match token {
            Token::AtKeyword(name) => {
                import = name.eq_ignore_ascii_case("import");
                font = name.eq_ignore_ascii_case("font-face");
            }
            Token::UnquotedUrl(value) => {
                out.urls.push((
                    value.to_string(),
                    if import { "stylesheet" } else { role },
                    import,
                ));
                import = false;
            }
            Token::QuotedString(value) if import || strings => {
                out.urls.push((
                    value.to_string(),
                    if import { "stylesheet" } else { role },
                    import,
                ));
                import = false;
            }
            Token::Ident(name)
                if matches!(
                    name.to_ascii_lowercase().as_str(),
                    "behavior" | "-moz-binding"
                ) =>
            {
                out.code = true
            }
            Token::Function(name) => {
                let name = name.to_ascii_lowercase();
                if strings && matches!(name.as_str(), "var" | "attr" | "env") {
                    out.unresolved = true;
                }
                let _: Result<(), cssparser::ParseError<'_, ()>> =
                    input.parse_nested_block(|nested| {
                        match name.as_str() {
                            "url" | "src" => {
                                if let Ok(value) = nested.expect_string_cloned() {
                                    if nested.is_exhausted() {
                                        out.urls.push((
                                            value.to_string(),
                                            if import { "stylesheet" } else { role },
                                            import,
                                        ));
                                    } else {
                                        out.unresolved = true;
                                    }
                                } else {
                                    out.unresolved = true;
                                }
                            }
                            "local" if role == "font" => out.local_font = true,
                            "expression" => out.code = true,
                            _ => tokens(
                                nested,
                                role,
                                matches!(
                                    name.as_str(),
                                    "image" | "image-set" | "-webkit-image-set"
                                ),
                                depth + 1,
                                out,
                            ),
                        }
                        Ok(())
                    });
                import = false;
            }
            Token::CurlyBracketBlock | Token::SquareBracketBlock | Token::ParenthesisBlock => {
                let _: Result<(), cssparser::ParseError<'_, ()>> =
                    input.parse_nested_block(|nested| {
                        tokens(
                            nested,
                            if font { "font" } else { role },
                            false,
                            depth + 1,
                            out,
                        );
                        Ok(())
                    });
                font = false;
                import = false;
            }
            Token::BadUrl(_) | Token::BadString(_) => out.malformed = true,
            Token::Semicolon => {
                import = false;
                font = false;
            }
            _ => {}
        }
    }
}

struct Inspection<'a> {
    entries: &'a BTreeMap<String, Entry>,
    documents: BTreeMap<String, Document<'a>>,
    findings: &'a mut Vec<Finding>,
    edges: BTreeMap<String, BTreeSet<String>>,
}

impl Inspection<'_> {
    fn issue(&mut self, path: &str, id: &str, message: &str, outcome: Outcome) {
        self.findings.push(Finding {
            requirement_id: id.into(),
            outcome,
            severity: if outcome == Outcome::Fail {
                Severity::Error
            } else {
                Severity::NotTested
            },
            capability: "Base".into(),
            stage: "security".into(),
            resource: Some(path.into()),
            node_id: None,
            revision_id: None,
            message: message.into(),
            evidence: serde_json::Value::Null,
            source: "Validator A".into(),
        });
    }
    fn fail(&mut self, path: &str, id: &str) {
        self.issue(path, id, "passive profile violation", Outcome::Fail);
    }

    fn reference(
        &mut self,
        path: &str,
        raw: &str,
        role: &str,
        svg: bool,
        link: bool,
        source: Option<String>,
    ) {
        let value = raw
            .trim_matches([' ', '\t', '\r', '\n', '\u{c}'])
            .replace(['\t', '\r', '\n'], "");
        let scheme = value
            .split_once(':')
            .map(|(s, _)| s.to_ascii_lowercase())
            .unwrap_or_default();
        if link && matches!(scheme.as_str(), "http" | "https") && value.contains("://") {
            return;
        }
        if !scheme.is_empty() || value.starts_with(['/', '\\']) {
            if matches!(scheme.as_str(), "javascript" | "vbscript") {
                self.fail(path, "SPD-SEC-001");
            }
            self.fail(path, "SPD-SEC-008");
            if !link {
                self.fail(path, "SPD-SEC-003");
                match role {
                    "font" => self.fail(path, "SPD-SEC-004"),
                    "stylesheet" => self.fail(path, "SPD-SEC-005"),
                    "image" => self.fail(path, "SPD-SEC-006"),
                    _ => {}
                }
            }
            if svg {
                self.fail(path, "SPD-SEC-007");
            }
            return;
        }
        let (raw_path, fragment) = value.split_once('#').unwrap_or((&value, ""));
        let Ok(decoded) = percent_decode_str(raw_path).decode_utf8() else {
            self.fail(path, "SPD-SEC-008");
            return;
        };
        let mut parts: Vec<&str> = if decoded.is_empty() {
            path.split('/').collect()
        } else {
            path.rsplit_once('/')
                .map(|(p, _)| p.split('/').collect())
                .unwrap_or_default()
        };
        let mut unsafe_path = decoded.starts_with('/') || decoded.contains(['\\', ':', '?']);
        if !decoded.is_empty() {
            for part in decoded.split('/') {
                match part {
                    "." | "" => {}
                    ".." => {
                        if parts.pop().is_none() {
                            unsafe_path = true;
                        }
                    }
                    p => parts.push(p),
                }
            }
        }
        let target = parts.join("/");
        if unsafe_path
            || target.nfc().collect::<String>() != target
            || !self.entries.contains_key(&target)
        {
            self.fail(path, "SPD-SEC-008");
            return;
        }
        let Ok(fragment) = percent_decode_str(fragment).decode_utf8() else {
            self.fail(path, "SPD-SEC-008");
            return;
        };
        if !fragment.is_empty()
            && !self.documents.get(&target).is_some_and(|doc| {
                doc.descendants()
                    .any(|n| n.attribute("id") == Some(fragment.as_ref()))
            })
        {
            self.fail(path, "SPD-SEC-008");
        }
        if !link && let Some(source) = source {
            self.edges
                .entry(source)
                .or_default()
                .insert(if fragment.is_empty() {
                    target
                } else {
                    format!("{target}#{fragment}")
                });
        }
    }

    fn css(&mut self, path: &str, text: &str, svg: bool) {
        let mut input = ParserInput::new(text);
        let mut facts = CssFacts::default();
        tokens(&mut Parser::new(&mut input), "image", false, 0, &mut facts);
        if facts.code {
            self.fail(path, "SPD-SEC-001");
        }
        if facts.local_font {
            self.fail(path, "SPD-SEC-004");
        }
        if facts.malformed {
            self.fail(path, "SPD-SEC-005");
        }
        if facts.unresolved || facts.limited {
            self.issue(
                path,
                "SPD-SEC-008",
                if facts.limited {
                    "RESOURCE_LIMIT CSS nesting"
                } else {
                    "dynamic URL consumer not resolved"
                },
                Outcome::NotTested,
            );
        }
        for (url, role, import) in facts.urls {
            self.reference(
                path,
                &url,
                role,
                svg,
                false,
                import.then(|| path.to_owned()),
            );
        }
    }

    fn xml(&mut self, path: &str, doc: &Document<'_>) {
        for pi in doc
            .descendants()
            .filter_map(|n| n.pi())
            .filter(|p| p.target == "xml-stylesheet")
        {
            let wrapped = format!("<style {}/>", pi.value.unwrap_or(""));
            if let Ok(attrs) = Document::parse(&wrapped) {
                if let Some(href) = attrs.root_element().attribute("href") {
                    self.reference(path, href, "stylesheet", false, false, None);
                }
            } else {
                self.fail(path, "SPD-SEC-005");
            }
        }
        for n in doc.descendants().filter(|n| n.is_element()) {
            let ns = n.tag_name().namespace().unwrap_or("");
            if ![HTML, SVG, MATH].contains(&ns) {
                continue;
            }
            let name = n.tag_name().name().to_ascii_lowercase();
            let svg = n.ancestors().any(|a| a.tag_name().namespace() == Some(SVG));
            if name == "script" {
                self.fail(path, "SPD-SEC-001");
                if svg {
                    self.fail(path, "SPD-SEC-007");
                }
            }
            if ["iframe", "object", "embed", "applet"].contains(&name.as_str()) {
                self.fail(path, "SPD-SEC-002");
                self.fail(path, "SPD-PASS-002");
            }
            if ["form", "base", "canvas"].contains(&name.as_str())
                || n.attribute(("http://www.w3.org/XML/1998/namespace", "base"))
                    .is_some()
            {
                self.fail(path, "SPD-PASS-002");
            }
            if name == "foreignobject" && svg {
                self.fail(path, "SPD-SEC-007");
                self.fail(path, "SPD-PASS-002");
            }
            if ["input", "button"].contains(&name.as_str()) {
                let label = n
                    .attribute("aria-label")
                    .or(n.attribute("aria-labelledby"))
                    .is_some()
                    || (name == "button"
                        && n.descendants()
                            .any(|t| t.is_text() && !t.text().unwrap_or("").trim().is_empty()))
                    || n.attribute("id").is_some_and(|id| {
                        doc.descendants()
                            .any(|l| l.has_tag_name("label") && l.attribute("for") == Some(id))
                    });
                let bad_attr = n.attributes().any(|a| {
                    [
                        "form",
                        "formaction",
                        "formenctype",
                        "formmethod",
                        "formtarget",
                        "formnovalidate",
                        "command",
                        "commandfor",
                        "popovertarget",
                        "popovertargetaction",
                    ]
                    .contains(&a.name())
                });
                let kind = n
                    .attribute("type")
                    .unwrap_or(if name == "button" { "submit" } else { "text" })
                    .to_ascii_lowercase();
                if n.attribute("disabled").is_none()
                    || !label
                    || bad_attr
                    || ["password", "file", "submit", "image", "reset"].contains(&kind.as_str())
                    || (name == "button" && kind != "button")
                    || (name == "input"
                        && n.attribute("value").is_none()
                        && !["checkbox", "radio"].contains(&kind.as_str()))
                {
                    self.fail(path, "SPD-PASS-002");
                }
            }
            if name == "meta"
                && n.attribute("http-equiv")
                    .is_some_and(|v| v.eq_ignore_ascii_case("refresh"))
            {
                self.fail(path, "SPD-SEC-003");
                self.fail(path, "SPD-PASS-002");
            }
            if n.attribute("autoplay").is_some() {
                self.fail(path, "SPD-PASS-003");
            }
            let rel = n.attribute("rel").unwrap_or("").to_ascii_lowercase();
            if n.attribute("ping").is_some()
                || rel
                    .split_whitespace()
                    .any(|v| ["prefetch", "preconnect", "dns-prefetch", "prerender"].contains(&v))
            {
                self.fail(path, "SPD-SEC-003");
            }
            if name == "style" {
                let text: String = n
                    .descendants()
                    .filter(|v| v.is_text())
                    .filter_map(|v| v.text())
                    .collect();
                self.css(path, &text, svg);
            }
            for a in n.attributes() {
                let attr = a.name().to_ascii_lowercase();
                if attr.starts_with("on") {
                    self.fail(path, "SPD-SEC-001");
                    if svg {
                        self.fail(path, "SPD-SEC-007");
                    }
                }
                if attr == "style"
                    || (svg
                        && [
                            "fill",
                            "stroke",
                            "filter",
                            "clip-path",
                            "mask",
                            "cursor",
                            "marker-start",
                            "marker-mid",
                            "marker-end",
                        ]
                        .contains(&attr.as_str()))
                {
                    self.css(path, a.value(), svg);
                }
                if !["href", "src", "srcset", "poster", "data", "background"]
                    .contains(&attr.as_str())
                {
                    continue;
                }
                if name == "base" {
                    continue;
                }
                let link = attr == "href"
                    && (["a", "area"].contains(&name.as_str()) || (ns == MATH && name != "mglyph"));
                let mut role = if name == "link"
                    && rel.split_whitespace().any(|s| s == "stylesheet")
                {
                    "stylesheet"
                } else if [
                    "img", "image", "use", "feimage", "mglyph", "audio", "video", "source", "track",
                ]
                .contains(&name.as_str())
                    || ["poster", "background"].contains(&attr.as_str())
                {
                    "image"
                } else {
                    "other"
                };
                if name == "link"
                    && rel
                        .split_whitespace()
                        .any(|s| matches!(s, "preload" | "modulepreload"))
                {
                    role = match n.attribute("as") {
                        Some("font") => "font",
                        Some("style") => "stylesheet",
                        Some("image") => "image",
                        _ => role,
                    };
                }
                let values: Vec<&str> = if attr == "srcset" {
                    a.value()
                        .split(',')
                        .filter_map(|v| v.split_whitespace().next())
                        .collect()
                } else {
                    vec![a.value()]
                };
                for value in values {
                    let source = (svg && !link).then(|| {
                        n.ancestors()
                            .find_map(|a| a.attribute("id"))
                            .map(|id| format!("{path}#{id}"))
                            .unwrap_or_else(|| path.to_owned())
                    });
                    self.reference(path, value, role, svg, link, source);
                }
            }
        }
    }
}

pub fn inspect(entries: &BTreeMap<String, Entry>, findings: &mut Vec<Finding>) {
    let xml_text: BTreeMap<_, _> = entries
        .iter()
        .filter_map(|(p, e)| {
            let b = &e.bytes;
            let text = if b.starts_with(&[0xff, 0xfe]) || b.starts_with(b"<\0") {
                let start = if b.starts_with(&[0xff, 0xfe]) { 2 } else { 0 };
                if (b.len() - start) % 2 != 0 {
                    return None;
                }
                String::from_utf16(
                    &b[start..]
                        .as_chunks::<2>()
                        .0
                        .iter()
                        .map(|c| u16::from_le_bytes([c[0], c[1]]))
                        .collect::<Vec<_>>(),
                )
                .ok()?
            } else if b.starts_with(&[0xfe, 0xff]) || b.starts_with(b"\0<") {
                let start = if b.starts_with(&[0xfe, 0xff]) { 2 } else { 0 };
                if (b.len() - start) % 2 != 0 {
                    return None;
                }
                String::from_utf16(
                    &b[start..]
                        .as_chunks::<2>()
                        .0
                        .iter()
                        .map(|c| u16::from_be_bytes([c[0], c[1]]))
                        .collect::<Vec<_>>(),
                )
                .ok()?
            } else {
                std::str::from_utf8(b)
                    .ok()?
                    .trim_start_matches('\u{feff}')
                    .to_owned()
            };
            if !text.trim_start().starts_with('<') {
                return None;
            }
            Some((p.clone(), text))
        })
        .collect();
    let documents: BTreeMap<_, _> = xml_text
        .iter()
        .filter_map(|(p, text)| Document::parse(text).ok().map(|d| (p.clone(), d)))
        .collect();
    let mut scan = Inspection {
        entries,
        documents,
        findings,
        edges: BTreeMap::new(),
    };
    // Separate parse handles avoid mutable/immutable aliasing during inspection.
    let paths: Vec<_> = scan.documents.keys().cloned().collect();
    let mut css_paths: BTreeSet<String> = entries
        .keys()
        .filter(|p| p.ends_with(".css"))
        .cloned()
        .collect();
    for path in paths {
        if let Some(text) = xml_text.get(&path)
            && let Ok(doc) = Document::parse(text)
        {
            if doc.root_element().tag_name().namespace() == Some("http://www.idpf.org/2007/opf") {
                for item in doc.descendants().filter(|n| n.has_tag_name("item")) {
                    if item.attribute("media-type").is_some_and(|m| {
                        matches!(
                            m,
                            "text/javascript"
                                | "application/javascript"
                                | "text/ecmascript"
                                | "application/ecmascript"
                        )
                    }) {
                        scan.fail(&path, "SPD-SEC-001");
                    }
                }
                for item in doc
                    .descendants()
                    .filter(|n| n.attribute("media-type") == Some("text/css"))
                {
                    if let Some(href) = item.attribute("href")
                        && !href.contains(':')
                    {
                        let base = path
                            .rsplit_once('/')
                            .map(|(p, _)| format!("{p}/"))
                            .unwrap_or_default();
                        css_paths.insert(format!("{base}{href}"));
                    }
                }
            }
            scan.xml(&path, &doc);
        }
    }
    for path in css_paths {
        if let Some(entry) = entries.get(&path) {
            if let Ok(text) = std::str::from_utf8(&entry.bytes) {
                scan.css(&path, text.trim_start_matches('\u{feff}'), false);
            } else {
                scan.fail(&path, "SPD-SEC-005");
            }
        }
    }
    let mut done = BTreeSet::new();
    let roots: Vec<_> = scan.edges.keys().cloned().collect();
    for root in roots {
        let mut active = BTreeSet::new();
        let mut stack = vec![(root.clone(), false)];
        while let Some((node, leave)) = stack.pop() {
            if leave {
                active.remove(&node);
                done.insert(node);
            } else if active.contains(&node) {
                scan.fail(root.split('#').next().unwrap_or(&root), "SPD-SEC-008");
            } else if !done.contains(&node) {
                active.insert(node.clone());
                stack.push((node.clone(), true));
                if let Some(children) = scan.edges.get(&node) {
                    stack.extend(children.iter().map(|v| (v.clone(), false)));
                }
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    fn css(text: &str) -> CssFacts {
        let mut source = ParserInput::new(text);
        let mut result = CssFacts::default();
        tokens(
            &mut Parser::new(&mut source),
            "image",
            false,
            0,
            &mut result,
        );
        result
    }
    #[test]
    fn nested_escaped_resource_consumers_and_inert_strings() {
        let parsed = css(
            r#"@media screen { a { --x: u\72l(https://example.invalid/x); background:var(--x); } }"#,
        );
        assert_eq!(parsed.urls[0].0, "https://example.invalid/x");
        assert!(
            css(r#"p::after {content:"https://example.invalid/inert"}"#)
                .urls
                .is_empty()
        );
        assert_eq!(css(r#"@import "local.css" print;"#).urls[0].1, "stylesheet");
        assert_eq!(
            css(r#"@font-face { src: url(font.ttf) }"#).urls[0].1,
            "font"
        );
        assert!(css(r#"p {background:image-set(var(--source) 1x)}"#).unresolved);
    }
    #[test]
    fn namespace_context_does_not_hide_active_svg() {
        let entries = BTreeMap::from([("no-extension".into(), Entry { bytes: br#"<svg:svg xmlns:svg="http://www.w3.org/2000/svg"><svg:script>void(0)</svg:script></svg:svg>"#.to_vec(), size: 0, sha256: String::new() })]);
        let mut findings = Vec::new();
        inspect(&entries, &mut findings);
        for id in ["SPD-SEC-001", "SPD-SEC-007"] {
            assert!(findings.iter().any(|f| f.requirement_id == id));
        }
    }
    proptest::proptest! {
        #[test]
        fn arbitrary_css_is_bounded_and_does_not_panic(text in ".{0,4096}") { let _ = css(&text); }
    }
}
