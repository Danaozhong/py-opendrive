from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
from lxml import etree

from py_opendrive.model.enumerations import TrafficRule, RoadType as RoadTypeEnum
from py_opendrive.model.lanes.road_lanes import RoadLanes


@dataclass
class RoadType:
    country: Optional[str] = None
    s: int = 0
    type: RoadTypeEnum = RoadTypeEnum.UNKNOWN


RoadLink = int
RoadObjects = int
RoadSignals = int
RoadRailroad = int


@dataclass
class Road:
    id: str = ""
    junction: str = ""

    # Total length of the reference line in the xy-plane in meters. Change in length due to elevation is not considered.
    length: float = 0.0

    # Name of the road. May be chosen freely.
    name: Optional[str] = None
    rule: Optional[TrafficRule] = None

    link: Optional[RoadLink] = None
    lanes: RoadLanes = field(default_factory=RoadLanes)
    road_objects: Optional[RoadObjects] = None
    road_signals: Optional[RoadSignals] = None
    road_railroad: Optional[RoadRailroad] = None

    type: list[RoadType] = field(default_factory=list)

    @staticmethod
    def from_xml(elem: etree._Element) -> Road:
        """Creates a Road instance from an XML node."""

        id = elem.get("id")
        junction = elem.get("junction")
        length = float(elem.get("length"))
        name = elem.get("name", None)
        rule = TrafficRule[elem.find("rule")] if elem.find("rule") else None

        lanes_element = elem.find("lanes")
        road_lanes = RoadLanes.from_xml(lanes_element)
        return Road(
            id=id,
            junction=junction,
            length=length,
            name=name,
            rule=rule,
            link=None,
            lanes=road_lanes,
            road_objects=None,
            road_signals=None,
            road_railroad=None,
            type=[],
        )

    def to_xml(self) -> etree._Element:
        """Creates an XML element from the Road instance."""
        elem = etree.Element("road")
        elem.set("id", self.id)
        elem.set("junction", self.junction)
        elem.set("length", str(self.length))
        if self.name:
            elem.set("name", self.name)
        if self.rule:
            elem.set("rule", self.rule.name)

        lanes_element = self.lanes.to_xml()
        elem.append(lanes_element)

        return elem
