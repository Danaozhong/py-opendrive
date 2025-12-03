from __future__ import annotations
from dataclasses import dataclass
from lxml import etree


@dataclass
class LaneRule:
    """A class to store `t_road_lanes_laneSection_lr_lane_rule`."""

    s_offset: float = 0.0
    value: str = ""

    @staticmethod
    def from_xml(elem: etree._Element) -> LaneRule:
        """Creates a LaneRule instance from an XML node."""
        s_offset = float(elem.get("sOffset", 0.0))
        value = elem.get("value", "")
        return LaneRule(s_offset=s_offset, value=value)

    def to_xml(self) -> etree._Element:
        """Creates an XML element from the LaneRule instance."""
        elem = etree.Element("rule")
        elem.set("sOffset", str(self.s_offset))
        elem.set("value", self.value)
        return elem
