from __future__ import annotations
from lxml import etree
from dataclasses import dataclass, field
from typing import Optional

from py_opendrive.model.enumerations import RoadType
from py_opendrive.model.signals.semantics import Semantics


@dataclass
class HeaderOffset:
    heading: float = 0.0
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    @staticmethod
    def from_xml(elem: etree._Element) -> HeaderOffset:
        """Creates a HeaderOffset instance from an XML node."""
        heading = float(elem.get("heading", 0))
        x = float(elem.get("x", 0))
        y = float(elem.get("y", 0))
        z = float(elem.get("z", 0))

        return HeaderOffset(
            heading=heading,
            x=x,
            y=y,
            z=z,
        )

    def to_xml(self) -> etree._Element:
        """Creates an XML element from the HeaderOffset instance."""
        elem = etree.Element("headerOffset")
        elem.set("heading", str(self.heading))
        elem.set("x", str(self.x))
        elem.set("y", str(self.y))
        elem.set("z", str(self.z))
        return elem


GeoReference = str


@dataclass
class GeoRef:
    offset: Optional[HeaderOffset]
    proj: str


@dataclass
class License:
    name: str
    resource: Optional[str] = None
    spdxid: Optional[str] = None
    text: Optional[str] = None

    @staticmethod
    def from_xml(elem: etree._Element) -> License:
        """Creates a License instance from an XML node."""
        name = elem.get("name")
        resource = elem.get("resource", None)
        spdxid = elem.get("spdxid", None)
        text = elem.get("text", None)

        return License(
            name=name,
            resource=resource,
            spdxid=spdxid,
            text=text,
        )

    def to_xml(self) -> etree._Element:
        """Creates an XML element from the License instance."""
        elem = etree.Element("license")
        elem.set("name", self.name)
        if self.resource is not None:
            elem.set("resource", self.resource)
        if self.spdxid is not None:
            elem.set("spdxid", self.spdxid)
        if self.text is not None:
            elem.set("text", self.text)
        return elem


@dataclass
class RoadRegulations:
    type: RoadType
    semantics: Optional[Semantics] = None


@dataclass
class SignalRegulation:
    type: str
    subtype: str
    semantics: Optional[Semantics] = None


@dataclass
class DefaultRegulations:
    road_regulations: list[RoadRegulations] = field(default_factory=list)
    signal_regulations: list[SignalRegulation] = field(default_factory=list)


@dataclass
class Header:
    date: Optional[str] = None
    east: Optional[float] = None
    name: Optional[str] = None
    north: Optional[float] = None
    rev_major: int = 0
    rev_minor: int = 0
    south: Optional[float] = None
    vendor: Optional[str] = None
    version: Optional[str] = None
    west: Optional[float] = None
    # Children nodes
    geo_reference: Optional[GeoReference] = None
    offset: Optional[HeaderOffset] = None
    license: Optional[License] = None

    def get_geo_reference(self) -> GeoRef:
        """Returns the geo reference if available."""
        return GeoRef(
            offset=self.offset,
            proj=self.geo_reference if self.geo_reference is not None else "EPSG:4326",
        )

    @staticmethod
    def from_xml(elem: etree._Element) -> Header:
        """Creates a Header instance from an XML node."""
        date = elem.get("date", None)
        east = float(elem.get("east")) if elem.get("east") is not None else None
        name = elem.get("name", None)
        north = float(elem.get("north")) if elem.get("north") is not None else None
        rev_major = int(elem.get("revMajor")) if elem.get("revMajor") is not None else 0
        rev_minor = int(elem.get("revMinor")) if elem.get("revMinor") is not None else 0
        south = float(elem.get("south")) if elem.get("south") is not None else None
        vendor = elem.get("vendor", None)
        version = elem.get("version", None)
        west = float(elem.get("west")) if elem.get("west") is not None else None

        # Children nodes
        geo_reference: Optional[GeoReference] = (
            elem.find("geoReference", None).text
            if elem.find("geoReference") is not None
            else None
        )
        offset: Optional[HeaderOffset] = None
        license: Optional[License] = None
        if elem.find("offset") is not None:
            offset = HeaderOffset.from_xml(elem.find("offset"))
        if elem.find("license") is not None:
            license = License.from_xml(elem.find("license"))

        return Header(
            date=date,
            east=east,
            name=name,
            north=north,
            rev_major=rev_major,
            rev_minor=rev_minor,
            south=south,
            vendor=vendor,
            version=version,
            west=west,
            geo_reference=geo_reference,
            offset=offset,
            license=license,
        )

    def to_xml(self) -> etree._Element:
        """Creates an XML element from the Header instance."""
        elem = etree.Element("header")
        if self.date is not None:
            elem.set("date", self.date)
        if self.east is not None:
            elem.set("east", str(self.east))
        if self.name is not None:
            elem.set("name", self.name)
        if self.north is not None:
            elem.set("north", str(self.north))
        if self.rev_major is not None:
            elem.set("revMajor", str(self.rev_major))
        if self.rev_minor is not None:
            elem.set("revMinor", str(self.rev_minor))
        if self.south is not None:
            elem.set("south", str(self.south))
        if self.vendor is not None:
            elem.set("vendor", self.vendor)
        if self.version is not None:
            elem.set("version", self.version)
        if self.west is not None:
            elem.set("west", str(self.west))

        # Children nodes
        if self.geo_reference is not None:
            geo_reference = etree.Element("geoReference")
            geo_reference.text = self.geo_reference
            elem.append(geo_reference)
        if self.offset is not None:
            elem.append(self.offset.to_xml())
        if self.license is not None:
            elem.append(self.license.to_xml())

        return elem
