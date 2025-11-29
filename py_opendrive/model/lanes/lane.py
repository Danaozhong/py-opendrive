from __future__ import annotations
from py_opendrive.model.lanes.lane_border import LaneBorder
from py_opendrive.model.lanes.lane_link import LaneLink
from py_opendrive.model.lanes.lane_width import LaneWidth
from py_opendrive.model.enumerations import LaneDirection, LaneType, LaneAdvisory
from dataclasses import dataclass, field
from typing import Optional
from lxml import etree


@dataclass
class Lane:
    id: int

    advisory: Optional[LaneAdvisory] = None
    direction: LaneDirection = LaneDirection.STANDARD
    dynamic_lane_direction: Optional[bool] = None
    level: Optional[bool] = None
    road_works: bool = False
    type: LaneType = LaneType.NONE

    width: list[LaneWidth] = field(default_factory=list)
    border: list[LaneBorder] = field(default_factory=list)
    link: Optional[LaneLink] = None

    @staticmethod
    def from_xml(elem: etree._Element) -> Lane:
        """Creates a Lane instance from an XML node."""
        id = int(elem.get("id"))
        advisory = (
            LaneAdvisory(elem.find("advisory"))
            if elem.find("advisory") is not None
            else None
        )
        direction = LaneDirection(elem.find("direction"))
        dynamic_lane_direction = (
            bool(elem.get("dynamicLaneDirection"))
            if elem.get("dynamicLaneDirection") is not None
            else None
        )
        level = bool(elem.get("level")) if elem.get("level") is not None else None
        road_works = (
            bool(elem.get("roadWorks")) if elem.get("roadWorks") is not None else False
        )
        type = (
            LaneType(elem.find("type"))
            if elem.find("type") is not None
            else LaneType.NONE
        )

        width: list[LaneWidth] = []
        border: list[LaneBorder] = []
        width = [LaneWidth.from_xml(width_elem) for width_elem in elem.findall("width")]
        border = [
            LaneBorder.from_xml(border_elem) for border_elem in elem.findall("border")
        ]

        link = (
            LaneLink.from_xml(elem.find("link"))
            if elem.find("link") is not None
            else None
        )

        return Lane(
            id=id,
            advisory=advisory,
            direction=direction,
            dynamic_lane_direction=dynamic_lane_direction,
            level=level,
            road_works=road_works,
            type=type,
            width=width,
            border=border,
            link=link,
        )

    def to_xml(self) -> etree._Element:
        """Creates an XML element from the Lane instance."""
        elem = etree.Element("lane")
        elem.set("id", str(self.id))
        if self.advisory is not None:
            elem.set("advisory", self.advisory.value)

        elem.set("direction", self.direction.value)

        if self.dynamic_lane_direction is not None:
            elem.set("dynamicLaneDirection", str(self.dynamic_lane_direction).lower())
        if self.level is not None:
            elem.set("level", str(self.level).lower())
        if self.road_works:
            elem.set("roadWorks", str(self.road_works).lower())

        elem.set("type", self.type.value)

        for width_elem in self.width:
            elem.append(width_elem.to_xml())
        for border_elem in self.border:
            elem.append(border_elem.to_xml())
        if self.link is not None:
            elem.append(self.link.to_xml())
        return elem
