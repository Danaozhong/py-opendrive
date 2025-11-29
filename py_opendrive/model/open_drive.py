from __future__ import annotations
from dataclasses import dataclass, field

from py_opendrive.model.roads.road import Road
from py_opendrive.model.header import Header
from lxml import etree


@dataclass
class OpenDrive:
    header: Header
    roads: list[Road] = field(default_factory=list)

    # junctions: list[Junction] = field(default_factory=list)

    @staticmethod
    def from_xml(elem) -> OpenDrive:
        """Creates an OpenDrive instance from an XML node."""
        header = Header.from_xml(elem.find("header"))

        roads = []
        for road_elem in elem.findall("road"):
            road = Road.from_xml(road_elem)
            roads.append(road)

        return OpenDrive(
            header=header,
            roads=roads,
        )

    def to_xml(self) -> etree._Element:
        """Creates an XML element from the OpenDrive instance."""
        elem = etree.Element("OpenDRIVE")

        header_elem = self.header.to_xml()
        elem.append(header_elem)

        for road in self.roads:
            road_elem = road.to_xml()
            elem.append(road_elem)

        return elem
