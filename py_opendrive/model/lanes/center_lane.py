from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from py_opendrive.model.enumerations import LaneType
from py_opendrive.model.lanes.lane_link import LaneLink
from lxml import etree


@dataclass
class CenterLane:
    id: int
    level: Optional[bool] = None
    type: Optional[LaneType] = None
    link: Optional[LaneLink] = None

    @staticmethod
    def from_xml(elem: etree._Element) -> CenterLane:
        """Creates a CenterLane instance from an XML node."""
        id = int(elem.get("id"))
        level = bool(elem.get("level")) if elem.get("level") is not None else None
        type = LaneType(elem.find("type")) if elem.find("type") is not None else None

        link = None
        if elem.find("link") is not None:
            link = LaneLink.from_xml(elem.find("link"))

        return CenterLane(
            id=id,
            level=level,
            type=type,
            link=link,
        )
