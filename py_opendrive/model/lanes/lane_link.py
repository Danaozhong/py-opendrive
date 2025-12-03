from __future__ import annotations
from dataclasses import dataclass, field
from lxml import etree


@dataclass
class LaneLink:
    predecessor: list[int] = field(default_factory=list)
    successor: list[int] = field(default_factory=list)

    @staticmethod
    def from_xml(elem: etree._Element) -> LaneLink:
        """Creates a LaneLink instance from an XML node."""
        predecessor: list[int] = []
        successor: list[int] = []

        for predecessor_elem in elem.findall("predecessor"):
            predecessor.append(int(predecessor_elem.get("id")))

        for successor_elem in elem.findall("successor"):
            successor.append(int(successor_elem.get("id")))

        return LaneLink(
            predecessor=predecessor,
            successor=successor,
        )

    def to_xml(self) -> etree._Element:
        """Creates an XML element from the LaneLink instance."""
        elem = etree.Element("link")

        for pred_id in self.predecessor:
            pred_elem = etree.Element("predecessor")
            pred_elem.set("id", str(pred_id))
            elem.append(pred_elem)

        for succ_id in self.successor:
            succ_elem = etree.Element("successor")
            succ_elem.set("id", str(succ_id))
            elem.append(succ_elem)

        return elem
