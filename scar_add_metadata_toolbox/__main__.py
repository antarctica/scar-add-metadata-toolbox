from datetime import datetime, timezone, date
from pathlib import Path

# noinspection PyPackageRequirements
# Exempting Bandit security issue (Using Element to parse untrusted XML data is known to be vulnerable to XML attacks)
#
# We don't currently allow untrusted/user-provided XML so this is not a risk
from lxml.etree import ElementTree, ProcessingInstruction, fromstring, tostring  # nosec

from bas_metadata_library.standards.iso_19115_2_v1 import MetadataRecordConfig, MetadataRecord

minimal_record_config = {
    "language": "eng",
    "character_set": "utf8",
    "hierarchy_level": "dataset",
    "contacts": [{"organisation": {"name": "UK Polar Data Centre"}, "role": ["pointOfContact"]}],
    "date_stamp": datetime(2018, 10, 18, 14, 40, 44, tzinfo=timezone.utc),
    "resource": {
        "title": {"value": "Test Record"},
        "dates": [{"date": date(2018, 1, 1), "date_precision": "year", "date_type": "creation"}],
        "abstract": "Test Record for ISO 19115 metadata standard family (no profile), with required properties only.",
        "character_set": "utf8",
        "language": "eng",
        "topics": ["environment", "climatologyMeteorologyAtmosphere"],
        "extent": {
            "geographic": {
                "bounding_box": {
                    "west_longitude": -45.61521,
                    "east_longitude": -27.04976,
                    "south_latitude": -68.1511,
                    "north_latitude": -54.30761,
                }
            }
        },
    },
}
configuration = MetadataRecordConfig(**minimal_record_config)

record = MetadataRecord(configuration=configuration)
document = record.generate_xml_document()

record_iso_html = ElementTree(fromstring(document))
record_iso_html_root = record_iso_html.getroot()
record_iso_html_root.addprevious(
    ProcessingInstruction(
        "xml-stylesheet", 'type="text/xsl" href="http://localhost:9000/stylesheets/iso-html/xml-to-html-ISO.xsl"',
    )
)
document_iso_html = tostring(record_iso_html, pretty_print=True, xml_declaration=True, encoding="utf-8")


record_iso_rubric = ElementTree(fromstring(document))
record_iso_rubric_root = record_iso_rubric.getroot()
record_iso_rubric_root.addprevious(
    ProcessingInstruction(
        "xml-stylesheet", 'type="text/xsl" href="http://localhost:9000/stylesheets/iso-rubric/isoRubricHTML.xsl"',
    )
)
document_iso_rubric = tostring(record_iso_rubric, pretty_print=True, xml_declaration=True, encoding="utf-8")


if __name__ == "__main__":
    with open(Path("output/candidate-record.xml"), "w") as file:
        file.write(document.decode())

    with open(Path("output/candidate-record-iso-html.xml"), "w") as file:
        file.write(document_iso_html.decode())

    with open(Path("output/candidate-record-iso-rubric.xml"), "w") as file:
        file.write(document_iso_rubric.decode())
