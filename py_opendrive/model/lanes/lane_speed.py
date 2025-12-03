from __future__ import annotations
from dataclasses import dataclass
from lxml import etree
from typing import Optional
from py_opendrive.model.enumerations import UnitSpeed


@dataclass
class LaneSpeed:
    """A class to store `t_road_lanes_laneSection_lr_lane_speed`."""

    # The maximum speed limit in this section.
    max: float = 0.0
    s_offset: float = 0.0
    unit: Optional[UnitSpeed] = None

    @staticmethod
    def from_xml(elem: etree._Element) -> LaneSpeed:
        """Creates a LaneSpeed instance from an XML node."""
        max_speed = float(elem.get("max", 0.0))
        s_offset = float(elem.get("sOffset", 0.0))
        unit = (
            UnitSpeed(elem.get("unit").lower())
            if elem.get("unit") is not None
            else None
        )
        return LaneSpeed(
            max=max_speed,
            s_offset=s_offset,
            unit=unit,
        )

    def to_xml(self) -> etree._Element:
        """Creates an XML element from the LaneSpeed instance."""
        elem = etree.Element("speed")
        elem.set("max", str(self.max))
        elem.set("sOffset", str(self.s_offset))
        if self.unit is not None:
            elem.set("unit", self.unit.value)
        return elem
