from __future__ import annotations
from dataclasses import dataclass
from lxml import etree
from py_opendrive.model.enumerations import PolyRange


@dataclass
class ParametricCubicCurve:
    """
    Represents a cubic parametric curve in the OpenDRIVE format.
    """

    s: float = 0.0
    x: float = 0.0
    y: float = 0.0
    hdg: float = 0.0
    length: float = 0.0

    # Coefficients for the u and v parametric equations.
    a_u: float = 0.0
    b_u: float = 0.0
    c_u: float = 0.0
    d_u: float = 0.0

    a_v: float = 0.0
    b_v: float = 0.0
    c_v: float = 0.0
    d_v: float = 0.0

    # How to interpret the length. If normalized, length is in [0,1], otherwise in meters.
    p_range: PolyRange = PolyRange.ARC_LENGTH

    @staticmethod
    def from_xml(elem: etree._Element) -> ParametricCubicCurve:
        """Creates a ParametricCubicCurve instance from an XML node."""

        s = float(elem.get("s"))
        x = float(elem.get("x"))
        y = float(elem.get("y"))
        hdg = float(elem.get("hdg"))
        length = float(elem.get("length"))
        poly_element = elem.find("paramPoly3")

        a_u = float(poly_element.get("aU"))
        b_u = float(poly_element.get("bU"))
        c_u = float(poly_element.get("cU"))
        d_u = float(poly_element.get("dU"))

        a_v = float(poly_element.get("aV"))
        b_v = float(poly_element.get("bV"))
        c_v = float(poly_element.get("cV"))
        d_v = float(poly_element.get("dV"))

        p_range = PolyRange(poly_element.get("pRange"))

        return ParametricCubicCurve(
            s=s,
            x=x,
            y=y,
            hdg=hdg,
            length=length,
            a_u=a_u,
            b_u=b_u,
            c_u=c_u,
            d_u=d_u,
            a_v=a_v,
            b_v=b_v,
            c_v=c_v,
            d_v=d_v,
            p_range=p_range,
        )

    def to_xml(self) -> etree._Element:
        """Creates an XML element from the ParametricCubicCurve instance."""
        elem = etree.Element("geometry")
        elem.set("s", str(self.s))
        elem.set("x", str(self.x))
        elem.set("y", str(self.y))
        elem.set("hdg", str(self.hdg))
        elem.set("length", str(self.length))

        # Write the spiral-specific elements in a sub-element.
        parametric_element = etree.Element("paramPoly3")
        parametric_element.set("aU", str(self.a_u))
        parametric_element.set("bU", str(self.b_u))
        parametric_element.set("cU", str(self.c_u))
        parametric_element.set("dU", str(self.d_u))
        parametric_element.set("aV", str(self.a_v))
        parametric_element.set("bV", str(self.b_v))
        parametric_element.set("cV", str(self.c_v))
        parametric_element.set("dV", str(self.d_v))
        parametric_element.set("pRange", self.p_range.value)
        elem.append(parametric_element)
        return elem
