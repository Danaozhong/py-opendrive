from pathlib import Path
from lxml import etree

from py_opendrive.model.open_drive import OpenDrive


def read_file(file_path: Path) -> OpenDrive:
    """Reads an `*.xodr` file and decodes it into an OpenDrive instance."""
    tree = etree.parse(file_path)

    # 2. Get the root element of the XML tree
    root = tree.getroot()

    # 3. Create an OpenDrive instance from the root element
    open_drive = OpenDrive.from_xml(root)

    return open_drive
