from __future__ import annotations

from dataclasses import dataclass

from lxml import etree


@dataclass
class Spiral:
    """
    Represents a spiral geometry in the OpenDRIVE format.
    See https://publications.pages.asam.net/standards/ASAM_OpenDRIVE/ASAM_OpenDRIVE_Specification/latest/specification/09_geometries/09_04_spiral.html
    """

    # The length of the spiral in the s coordinate.
    s: float = 0.0

    # The x coordinate of the spiral in the local coordinate system.
    x: float = 0.0

    # The y coordinate of the spiral in the local coordinate system.
    y: float = 0.0

    # The heading of the spiral in the local coordinate system.
    hdg: float = 0.0

    # The length of the spiral.
    length: float = 0.0

    # Curvature at the start of the element in 1/m.
    curv_start: float = 0.0

    # Curvature at the end of the element in 1/m.
    curv_end: float = 0.0

    def from_xml(elem: etree._Element) -> Spiral:
        """Creates a Spiral instance from an XML node."""
        s = float(elem.get("s"))
        x = float(elem.get("x"))
        y = float(elem.get("y"))
        hdg = float(elem.get("hdg"))
        length = float(elem.get("length"))
        spiral_elem = elem.find("spiral")
        curv_start = float(spiral_elem.get("curvStart"))
        curv_end = float(spiral_elem.get("curvEnd"))
        return Spiral(
            s=s,
            x=x,
            y=y,
            hdg=hdg,
            length=length,
            curv_start=curv_start,
            curv_end=curv_end,
        )

    def to_xml(self) -> etree._Element:
        """Creates an XML element from the Spiral instance."""
        elem = etree.Element("geometry")
        elem.set("s", str(self.s))
        elem.set("x", str(self.x))
        elem.set("y", str(self.y))
        elem.set("hdg", str(self.hdg))
        elem.set("length", str(self.length))

        # Write the spiral-specific elements in a sub-element.
        spiral_element = etree.Element("spiral")
        spiral_element.set("curvStart", str(self.curv_start))
        spiral_element.set("curvEnd", str(self.curv_end))
        elem.append(spiral_element)
        return elem
