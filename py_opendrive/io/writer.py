from pathlib import Path
from lxml import etree
from py_opendrive.model.open_drive import OpenDrive


def write_file(open_drive: OpenDrive, file_path: Path) -> None:
    """Writes an OpenDrive instance into an `*.xodr` file."""
    xml_content = etree.tostring(
        open_drive.to_xml(), pretty_print=True, xml_declaration=True, encoding="UTF-8"
    )
    with open(file_path, "wb") as file:
        file.write(xml_content)
