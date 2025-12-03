from __future__ import annotations
from dataclasses import dataclass, field

from typing import Union
from py_opendrive.geometries.line import Line
from py_opendrive.geometries.spiral import Spiral
from py_opendrive.geometries.parametric_cubic_curve import ParametricCubicCurve
from py_opendrive.geometries.arc import Arc
from lxml import etree

Geometries = Union[Line, Spiral, ParametricCubicCurve, Arc]


@dataclass
class RoadReferenceLine:
    """Represents the reference line geometry of a road."""

    geometries: list[Geometries] = field(default_factory=list)

    def get_total_length(self) -> float:
        """Calculates the total length of the road reference line in meters."""
        return sum(geometry.length for geometry in self.geometries)

    @staticmethod
    def from_xml(elem) -> RoadReferenceLine:
        """Creates a RoadReferenceLine instance from an XML node."""
        geometries = []
        for geometry_elem in elem.findall("geometry"):
            if geometry_elem.find("line") is not None:
                geometry = Line.from_xml(geometry_elem)
            elif geometry_elem.find("spiral") is not None:
                geometry = Spiral.from_xml(geometry_elem)
            elif geometry_elem.find("paramPoly3") is not None:
                geometry = ParametricCubicCurve.from_xml(geometry_elem)
            elif geometry_elem.find("arc") is not None:
                geometry = Arc.from_xml(geometry_elem)
            else:
                raise NotImplementedError("Geometry type not supported.")
            geometries.append(geometry)
        return RoadReferenceLine(geometries=geometries)

    def to_xml(self) -> etree._Element:
        """Creates an XML element from the RoadReferenceLine instance."""
        elem = etree.Element("planView")
        for geometry in self.geometries:
            geometry_elem = geometry.to_xml()
            elem.append(geometry_elem)
        return elem
