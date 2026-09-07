from __future__ import annotations

FORMAT_RC1_SHA256 = "19df8ce9b5d242a60cb0a9c035eadf1b93697fe0bea6bcc94fd3b5f7f44fd208"
REQUIREMENTS_SHA256 = "44e2080186cada6c68e16f38635c03fe9d578e782a6932fc80cf104230375eb0"
FORMAT_VERSION = "0.1"

RELATIONSHIPS = {
    "document-state": "urn:uuid:0f55d1fb-e1b0-50bb-8a92-53d09c9aa7fc",
    "resource-inventory": "urn:uuid:08f2982f-d258-5482-abdc-cd6e2b86d990",
    "lifecycle-state": "urn:uuid:ec3f5340-bab9-5d57-8c81-77e08906aa4c",
}
CAPABILITY_IRIS = {
    "urn:uuid:bc7ad5f0-9b06-5b01-af4e-7b24ebe724aa": "Base",
    "urn:uuid:7e37d29a-41ac-5151-b843-5bca73555514": "Mapping",
    "urn:uuid:ab0f83fe-b584-5726-b289-4892bd823bcb": "Accessible",
    "urn:uuid:92e65973-5fbe-5e41-b604-fcfc88aabcb5": "Fixed-Experimental",
    "urn:uuid:f8ff21ff-6200-5cf2-9ca1-3c1935fbf329": "Archive-Experimental",
}
CAPABILITIES = set(CAPABILITY_IRIS.values())
STABLE_NODE_SELECTOR = "urn:uuid:95d3b3f6-45bb-50fd-9aa5-8bba8186649f"
CANONICAL_SCHEMAS = {
    "document-state": "document-state.schema.json",
    "resource-inventory": "resource-inventory.schema.json",
    "lifecycle-state": "state.schema.json",
    "mapping": "mapping.schema.json",
    "annotation": "annotation-extension.schema.json",
    "conformance-result": "conformance-result.schema.json",
}

XHTML_NS = "http://www.w3.org/1999/xhtml"
XML_NS = "http://www.w3.org/XML/1998/namespace"
OCF_NS = "urn:oasis:names:tc:opendocument:xmlns:container"
OPF_NS = "http://www.idpf.org/2007/opf"
DC_NS = "http://purl.org/dc/elements/1.1/"

