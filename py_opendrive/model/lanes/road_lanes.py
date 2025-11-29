from __future__ import annotations
from dataclasses import dataclass, field
from py_opendrive.model.lanes.lane_offset import LaneOffset
from py_opendrive.model.lanes.lane_section import LaneSection
from lxml import etree


@dataclass
class RoadLanes:
    lane_section: list[LaneSection] = field(default_factory=list)
    lane_offset: list[LaneOffset] = field(default_factory=list)

    @staticmethod
    def from_xml(elem: etree._Element) -> RoadLanes:
        """Creates a RoadLanes instance from an XML node."""
        lane_sections: list[LaneSection] = []
        for lane_section_elem in elem.findall("laneSection"):
            lane_section = LaneSection.from_xml(lane_section_elem)
            lane_sections.append(lane_section)

        lane_offsets: list[LaneOffset] = []
        for lane_offset_elem in elem.findall("laneOffset"):
            lane_offset = LaneOffset.from_xml(lane_offset_elem)
            lane_offsets.append(lane_offset)

        return RoadLanes(
            lane_section=lane_sections,
            lane_offset=lane_offsets,
        )

    def to_xml(self) -> etree._Element:
        """Creates an XML element from the RoadLanes instance."""
        elem = etree.Element("lanes")

        for lane_section in self.lane_section:
            lane_section_elem = lane_section.to_xml()
            elem.append(lane_section_elem)

        for lane_offset in self.lane_offset:
            lane_offset_elem = lane_offset.to_xml()
            elem.append(lane_offset_elem)

        return elem
