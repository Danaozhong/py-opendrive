from __future__ import annotations
from dataclasses import dataclass
from lxml import etree


@dataclass
class Line:
    """
    Represents a line geometry in the OpenDRIVE format.
    """

    # The length of the line in the s-coordinate.
    s: float = 0.0

    # The x coordinate of the line in the local coordinate system.
    x: float = 0.0

    # The y coordinate of the line in the local coordinate system.
    y: float = 0.0

    # The heading of the line in the local coordinate system.
    hdg: float = 0.0

    # The length of the line.
    length: float = 0.0

    def from_xml(elem: etree._Element) -> Line:
        """Creates a Line instance from an XML node."""
        s = float(elem.get("s"))
        x = float(elem.get("x"))
        y = float(elem.get("y"))
        hdg = float(elem.get("hdg"))
        length = float(elem.get("length"))
        return Line(
            s=s,
            x=x,
            y=y,
            hdg=hdg,
            length=length,
        )

    def to_xml(self) -> etree._Element:
        """Creates an XML element from the Line instance."""
        elem = etree.Element("geometry")
        elem.set("s", str(self.s))
        elem.set("x", str(self.x))
        elem.set("y", str(self.y))
        elem.set("hdg", str(self.hdg))
        elem.set("length", str(self.length))
        return elem
