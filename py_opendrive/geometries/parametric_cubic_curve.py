from __future__ import annotations
from dataclasses import dataclass, field
from lxml import etree
from py_opendrive.model.enumerations import PolyRange
from py_opendrive.geometries.basic import GeometryType


@dataclass
class CubicPolynomial:
    r"""Class representing the Cubic polynomial.

    $$y(x) = a + b*x + c*x2 + d*x^3$$

    Parameters
    ----------
    a : float
        a parameter in the interpolation equation.
    b : float
        b parameter in the interpolation equation.
    c : float
        c parameter in the interpolation equation.
    d : float
        d parameter in the interpolation equation.
    """

    a: float = 0.0
    b: float = 0.0
    c: float = 0.0
    d: float = 0.0


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

    u_poly: CubicPolynomial = field(default_factory=CubicPolynomial)
    v_poly: CubicPolynomial = field(default_factory=CubicPolynomial)

    # How to interpret the length. If normalized, length is in [0,1], otherwise in meters.
    p_range: PolyRange = PolyRange.ARC_LENGTH

    def type(self) -> GeometryType:
        """Returns the geometry type."""
        return GeometryType.PARAMPOLY3

    @staticmethod
    def from_xml(elem: etree._Element) -> ParametricCubicCurve:
        """Creates a ParametricCubicCurve instance from an XML node."""

        s = float(elem.get("s"))
        x = float(elem.get("x"))
        y = float(elem.get("y"))
        hdg = float(elem.get("hdg"))
        length = float(elem.get("length"))
        poly_element = elem.find("paramPoly3")

        u_poly = CubicPolynomial(
            a=float(poly_element.get("aU")),
            b=float(poly_element.get("bU")),
            c=float(poly_element.get("cU")),
            d=float(poly_element.get("dU")),
        )

        v_poly = CubicPolynomial(
            a=float(poly_element.get("aV")),
            b=float(poly_element.get("bV")),
            c=float(poly_element.get("cV")),
            d=float(poly_element.get("dV")),
        )

        p_range = PolyRange(poly_element.get("pRange"))

        return ParametricCubicCurve(
            s=s,
            x=x,
            y=y,
            hdg=hdg,
            length=length,
            u_poly=u_poly,
            v_poly=v_poly,
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
        parametric_element.set("aU", str(self.u_poly.a))
        parametric_element.set("bU", str(self.u_poly.b))
        parametric_element.set("cU", str(self.u_poly.c))
        parametric_element.set("dU", str(self.u_poly.d))
        parametric_element.set("aV", str(self.v_poly.a))
        parametric_element.set("bV", str(self.v_poly.b))
        parametric_element.set("cV", str(self.v_poly.c))
        parametric_element.set("dV", str(self.v_poly.d))
        parametric_element.set("pRange", self.p_range.value)
        elem.append(parametric_element)
        return elem
