from __future__ import annotations
from dataclasses import dataclass
from lxml import etree
from py_opendrive.geometries.basic import GeometryType


@dataclass
class Arc:
    """
    Represents an arc geometry in the OpenDRIVE format.
    """

    s: float = 0.0
    x: float = 0.0
    y: float = 0.0
    hdg: float = 0.0
    length: float = 0.0

    # The curvature of the arc.
    curvature: float = 0.0

    def type(self) -> GeometryType:
        """Returns the geometry type."""
        return GeometryType.ARC

    @staticmethod
    def from_xml(elem) -> Arc:
        """Creates an Arc instance from an XML node."""
        s = float(elem.get("s"))
        x = float(elem.get("x"))
        y = float(elem.get("y"))
        hdg = float(elem.get("hdg"))
        length = float(elem.get("length"))
        arc_elem = elem.find("arc")
        curvature = float(arc_elem.get("curvature"))
        return Arc(
            s=s,
            x=x,
            y=y,
            hdg=hdg,
            length=length,
            curvature=curvature,
        )

    def to_xml(self) -> etree._Element:
        """Creates an XML element from the Arc instance."""
        elem = etree.Element("geometry")
        elem.set("s", str(self.s))
        elem.set("x", str(self.x))
        elem.set("y", str(self.y))
        elem.set("hdg", str(self.hdg))
        elem.set("length", str(self.length))

        arc_elem = etree.SubElement(elem, "arc")
        arc_elem.set("curvature", str(self.curvature))

        return elem
