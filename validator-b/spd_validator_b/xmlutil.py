from __future__ import annotations

from lxml import etree


class XMLValidationError(ValueError):
    pass


def parse_xml(data: bytes, *, resource: str) -> etree._Element:
    upper = data[:4096].upper()
    if b"<!DOCTYPE" in upper or b"<!ENTITY" in upper:
        raise XMLValidationError(f"DTD/entity declarations are prohibited in {resource}")
    parser = etree.XMLParser(
        resolve_entities=False,
        no_network=True,
        load_dtd=False,
        dtd_validation=False,
        recover=False,
        remove_comments=False,
        remove_pis=False,
        huge_tree=False,
        ns_clean=False,
    )
    try:
        root = etree.fromstring(data, parser=parser, base_url=resource)
    except (etree.XMLSyntaxError, ValueError) as exc:
        raise XMLValidationError(str(exc)) from exc
    if root.getroottree().docinfo.doctype:
        raise XMLValidationError(f"DOCTYPE is prohibited in {resource}")
    return root


def local_name(element: etree._Element) -> str:
    return etree.QName(element).localname

