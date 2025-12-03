from __future__ import annotations
from py_opendrive.model.lanes.lane_border import LaneBorder
from py_opendrive.model.lanes.lane_link import LaneLink
from py_opendrive.model.lanes.lane_width import LaneWidth
from py_opendrive.model.lanes.lane_rule import LaneRule
from py_opendrive.model.lanes.lane_material import LaneMaterial
from py_opendrive.model.lanes.lane_speed import LaneSpeed
from py_opendrive.model.lanes.lane_access import LaneAccess
from py_opendrive.model.enumerations import LaneDirection, LaneType, LaneAdvisory
from dataclasses import dataclass, field
from typing import Optional
from lxml import etree


@dataclass
class Lane:
    id: int

    advisory: Optional[LaneAdvisory] = None
    direction: Optional[LaneDirection] = None
    dynamic_lane_direction: Optional[bool] = None
    level: Optional[bool] = None
    road_works: bool = False
    type: LaneType = LaneType.NONE

    width: list[LaneWidth] = field(default_factory=list)
    border: list[LaneBorder] = field(default_factory=list)
    link: Optional[LaneLink] = None

    rules: list[LaneRule] = field(default_factory=list)
    material: list[LaneMaterial] = field(default_factory=list)
    speed: list[LaneSpeed] = field(default_factory=list)
    access: list[LaneAccess] = field(default_factory=list)
    # height: list[LaneRoadMark] = field(default_factory=list)

    @staticmethod
    def from_xml(elem: etree._Element) -> Lane:
        """Creates a Lane instance from an XML node."""
        id = int(elem.get("id"))
        advisory = (
            LaneAdvisory(elem.find("advisory"))
            if elem.find("advisory") is not None
            else None
        )
        direction = None
        if elem.find("direction") is not None:
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

        rules = [LaneRule.from_xml(rule_elem) for rule_elem in elem.findall("rule")]
        material = [
            LaneMaterial.from_xml(material_elem)
            for material_elem in elem.findall("material")
        ]
        speed = [LaneSpeed.from_xml(speed_elem) for speed_elem in elem.findall("speed")]
        access = [
            LaneAccess.from_xml(access_elem) for access_elem in elem.findall("access")
        ]

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
            rules=rules,
            material=material,
            speed=speed,
            access=access,
        )

    def to_xml(self) -> etree._Element:
        """Creates an XML element from the Lane instance."""
        elem = etree.Element("lane")
        elem.set("id", str(self.id))
        if self.advisory is not None:
            elem.set("advisory", self.advisory.value)

        if self.direction is not None:
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

        for rule_elem in self.rules:
            elem.append(rule_elem.to_xml())
        for material_elem in self.material:
            elem.append(material_elem.to_xml())
        for speed_elem in self.speed:
            elem.append(speed_elem.to_xml())
        for access_elem in self.access:
            elem.append(access_elem.to_xml())
        return elem
