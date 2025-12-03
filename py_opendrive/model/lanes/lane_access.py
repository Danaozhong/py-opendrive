from __future__ import annotations
from dataclasses import dataclass, field
from lxml import etree
from typing import Optional
from py_opendrive.model.enumerations import AccessRestrictionType
from enum import Enum


class LaneAccessRule(Enum):
    ALLOW = "allow"
    DENY = "deny"


@dataclass
class LaneAccess:
    """A class to store `t_road_lanes_laneSection_lr_lane_access`."""

    rule: Optional[LaneAccessRule] = None
    s_offset: float = 0.0
    restrictions: list[AccessRestrictionType] = field(default_factory=list)

    @staticmethod
    def from_xml(elem: etree._Element) -> LaneAccess:
        """Creates a LaneAccess instance from an XML node."""
        rule = LaneAccessRule[elem.get("rule").upper()] if elem.get("rule") else None
        s_offset = float(elem.get("sOffset", 0.0))
        restrictions = [
            AccessRestrictionType[child.tag.upper()]
            for child in elem
            if child.tag in AccessRestrictionType.__members__
        ]
        return LaneAccess(rule=rule, s_offset=s_offset, restrictions=restrictions)

    def to_xml(self) -> etree._Element:
        """Creates an XML element from the LaneAccess instance."""
        elem = etree.Element("access")
        if self.rule is not None:
            elem.set("rule", self.rule.value)
        elem.set("sOffset", str(self.s_offset))
        for restriction in self.restrictions:
            etree.SubElement(elem, restriction.value)
        return elem
