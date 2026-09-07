from hypothesis import given
from hypothesis import strategies as st

from spd_validator_b.models import ResourceLimits, ValidationReport
from spd_validator_b.passive import Inspector


class MemoryPackage:
    def __init__(self, data):
        self.data = data
        self.paths = set(data)
        self.limits = ResourceLimits()

    def read(self, path, **kwargs):
        return self.data[path]

    def exists(self, path):
        return path in self.data


def inspect(data):
    report = ValidationReport('memory')
    Inspector(MemoryPackage(data), report).run()
    return report


def test_escaped_nested_css_and_inert_string_are_distinct():
    report = inspect({'a.css': br'@media screen {p{--x:u\72l(https://example.invalid/a.png);background:var(--x)}}'})
    assert set(report.violation_requirement_ids) == {'SPD-SEC-003', 'SPD-SEC-006', 'SPD-SEC-008'}
    assert not inspect({'a.css': b'p::after{content:"https://example.invalid/inert"}'}).violation_requirement_ids


def test_namespace_svg_without_extension_and_local_fragment():
    report = inspect({'art': b'<s:svg xmlns:s="http://www.w3.org/2000/svg"><s:script>void(0)</s:script></s:svg>'})
    assert {'SPD-SEC-001','SPD-SEC-007'} <= set(report.violation_requirement_ids)
    assert not inspect({'art': b'<svg xmlns="http://www.w3.org/2000/svg"><defs><rect id="r"/></defs><use href="#r"/></svg>'}).violation_requirement_ids


def test_dynamic_string_consumer_is_not_silently_passed():
    report = inspect({'a.css': b'p{background:image-set(var(--source) 1x)}'})
    assert 'SPD-SEC-008' in report.not_tested_requirement_ids


@given(st.text(max_size=2048))
def test_css_token_inspection_does_not_crash(text):
    inspect({'a.css': text.encode('utf-8')})
