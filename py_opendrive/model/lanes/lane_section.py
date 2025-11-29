from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
from py_opendrive.model.lanes.lane import Lane
from py_opendrive.model.lanes.center_lane import CenterLane
from lxml import etree


@dataclass
class LaneSection:
    # s-coordinate of start position, must be > 0.
    s: float
    single_side: Optional[bool] = None

    left: list[Lane] = field(default_factory=list)
    center: Optional[CenterLane] = None
    right: list[Lane] = field(default_factory=list)

    @staticmethod
    def from_xml(elem: etree._Element) -> LaneSection:
        """Creates a LaneSection instance from an XML node."""
        s = float(elem.get("s"))

        single_side = None
        if elem.get("singleSide") is not None:
            single_side = bool(elem.get("singleSide"))

        left: list[Lane] = []
        right: list[Lane] = []
        if elem.get("left") is not None:
            left = [
                Lane.from_xml(lane_elem)
                for lane_elem in elem.get("left").findall("lane")
            ]
        if elem.get("right") is not None:
            right = [
                Lane.from_xml(lane_elem)
                for lane_elem in elem.get("right").findall("lane")
            ]

        center = None
        if elem.get("center") is not None:
            center = CenterLane.from_xml(elem.get("center").get("lane"))

        return LaneSection(
            s=s,
            single_side=single_side,
            left=left,
            center=center,
            right=right,
        )

    def to_xml(self) -> etree._Element:
        """Creates an XML element from the LaneSection instance."""
        elem = etree.Element("laneSection")
        elem.set("s", str(self.s))
        if self.single_side is not None:
            elem.set("singleSide", str(self.single_side).lower())

        for lane_elem in self.left:
            elem.append(lane_elem.to_xml())
        if self.center is not None:
            elem.append(self.center.to_xml())
        for lane_elem in self.right:
            elem.append(lane_elem.to_xml())

        return elem
