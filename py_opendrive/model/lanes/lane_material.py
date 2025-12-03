from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from lxml import etree


@dataclass
class LaneMaterial:
    """A class to store `t_road_lanes_laneSection_lr_lane_material`."""

    friction: float = 0.0
    roughness: Optional[float] = None
    s_offset: float = 0.0
    surface: Optional[str] = None

    @staticmethod
    def from_xml(elem: etree._Element) -> LaneMaterial:
        """Creates a LaneMaterial instance from an XML node."""
        friction = float(elem.get("friction", 0.0))
        roughness = (
            float(elem.get("roughness")) if elem.get("roughness") is not None else None
        )
        s_offset = float(elem.get("sOffset", 0.0))
        surface = elem.get("surface") if elem.get("surface") is not None else None
        return LaneMaterial(
            friction=friction,
            roughness=roughness,
            s_offset=s_offset,
            surface=surface,
        )

    def to_xml(self) -> etree._Element:
        """Creates an XML element from the LaneMaterial instance."""
        elem = etree.Element("material")
        elem.set("friction", str(self.friction))
        if self.roughness is not None:
            elem.set("roughness", str(self.roughness))
        elem.set("sOffset", str(self.s_offset))
        if self.surface is not None:
            elem.set("surface", self.surface)
        return elem
