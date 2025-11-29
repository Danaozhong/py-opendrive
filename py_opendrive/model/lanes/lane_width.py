from __future__ import annotations
from dataclasses import dataclass
from lxml import etree


@dataclass
class LaneWidth:
    a: float = 0.0
    b: float = 0.0
    c: float = 0.0
    d: float = 0.0
    s_offset: float = 0.0

    @staticmethod
    def from_xml(elem: etree._Element) -> LaneWidth:
        """Creates a LaneWidth instance from an XML node."""
        a = float(elem.get("a", 0.0))
        b = float(elem.get("b", 0.0))
        c = float(elem.get("c", 0.0))
        d = float(elem.get("d", 0.0))
        s_offset = float(elem.get("sOffset", 0.0))

        return LaneWidth(a=a, b=b, c=c, d=d, s_offset=s_offset)

    def to_xml(self) -> etree._Element:
        """Creates an XML element from the LaneWidth instance."""
        elem = etree.Element("width")
        elem.set("a", str(self.a))
        elem.set("b", str(self.b))
        elem.set("c", str(self.c))
        elem.set("d", str(self.d))
        elem.set("sOffset", str(self.s_offset))
        return elem
