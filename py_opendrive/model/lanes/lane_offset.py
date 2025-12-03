from __future__ import annotations
from lxml import etree

from dataclasses import dataclass


@dataclass
class LaneOffset:
    a: float = 0.0
    b: float = 0.0
    c: float = 0.0
    d: float = 0.0
    s: float = 0.0

    @staticmethod
    def from_xml(elem: etree._Element) -> LaneOffset:
        """Creates a LaneOffset instance from an XML node."""
        a = float(elem.get("a", 0.0))
        b = float(elem.get("b", 0.0))
        c = float(elem.get("c", 0.0))
        d = float(elem.get("d", 0.0))
        s = float(elem.get("s", 0.0))

        return LaneOffset(a=a, b=b, c=c, d=d, s=s)

    def to_xml(self) -> etree._Element:
        """Creates an XML element from the LaneOffset instance."""
        elem = etree.Element("laneOffset")
        elem.set("a", str(self.a))
        elem.set("b", str(self.b))
        elem.set("c", str(self.c))
        elem.set("d", str(self.d))
        elem.set("s", str(self.s))
        return elem
