from dataclasses import dataclass, field

from typing import Union
from py_opendrive.geometries.line import Line
from py_opendrive.geometries.spiral import Spiral
from py_opendrive.geometries.parametric_cubic_curve import ParametricCubicCurve
from py_opendrive.geometries.arc import Arc

Geometries = Union[Line, Spiral, ParametricCubicCurve, Arc]


@dataclass
class RoadReferenceLine:
    """Represents the reference line geometry of a road."""

    geometries: list[Geometries] = field(default_factory=list)
