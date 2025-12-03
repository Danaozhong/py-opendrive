import numpy as np
import numpy.typing as npt
from py_opendrive.geometries.arc import Arc
from py_opendrive.geometries.line import Line
from py_opendrive.geometries.parametric_cubic_curve import (
    CubicPolynomial,
    ParametricCubicCurve,
)
from py_opendrive.geometries.spiral import Spiral
from py_opendrive.geometries.road_reference_line import Geometries
from py_opendrive.model.enumerations import PolyRange


def evaluate_geometry_at_p(
    geometry: Geometries, p_values: npt.NDArray[np.float32]
) -> npt.NDArray[np.float32]:
    """Evaluates a given geometry at positions p.

    Args:
        geometry: The geometry object to evaluate.
        p_values: The positions along the geometry to evaluate.

    Returns:
        A tuple (x, y, hdg) representing the evaluated position and heading.
    """

    if isinstance(geometry, Line):
        return evaluate_line_geometry_at_p(geometry, p_values)
    elif isinstance(geometry, Spiral):
        return evaluate_spiral_geometry_at_p(geometry, p_values)
    elif isinstance(geometry, Arc):
        return evaluate_arc_geometry_at_p(geometry, p_values)
    elif isinstance(geometry, ParametricCubicCurve):
        return evaluate_parametric_cubic_curve_at_p(geometry, p_values)
    else:
        raise NotImplementedError(f"Evaluation not implemented for {type(geometry)}")


def evaluate_line_geometry_at_p(
    _: Line, p_values: npt.NDArray[np.float32]
) -> npt.NDArray[np.float32]:
    """Evaluates a line geometry at all positions p."""
    return np.array([p_values, np.zeros_like(p_values)], dtype=np.float32).T


def evaluate_spiral_geometry_at_p(
    spiral: Spiral, p_values: npt.NDArray[np.float32]
) -> npt.NDArray[np.float32]:
    """Evaluates a spiral geometry at all positions p."""
    # TODO implement spiral evaluation logic.
    pass


def evaluate_arc_geometry_at_p(
    arc: Arc, p_values: npt.NDArray[np.float32]
) -> npt.NDArray[np.float32]:
    """Evaluates an arc geometry at all positions p."""
    radius_of_curvature = 1.0 / arc.curvature
    circle_centre = np.array([0.0, radius_of_curvature])
    origin_coordinates_tensor = np.tile(
        np.array([circle_centre[0], circle_centre[1]]), (len(p_values), 1)
    )
    # From equation of arc length of circle and total length of arc
    max_theta = 1.0 / radius_of_curvature
    theta_array = p_values * max_theta
    u = radius_of_curvature * np.sin(theta_array)
    v = -radius_of_curvature * np.cos(theta_array)
    return np.array([u, v]).T + origin_coordinates_tensor


def evaluate_polynomial_at_p(
    polynomial: CubicPolynomial, p_array: npt.NDArray[np.float32]
) -> npt.NDArray[np.float32]:
    r"""Return local (p, v) coordinates from an array of parameter $p \in [0.0, 1.0]$.

    (p, v) coordinates are in their own x,y frame: start at origin, and initial
    heading is along the x axis.

    Parameters
    ----------
    p_array : np.ndarray
        p values $\in [0.0, 1.0]$ to compute parametric coordinates.

    Returns:
    -------
    np.ndarray
        Array of local (p, v) coordinate pairs.
    """
    return (
        polynomial.a * np.ones_like(p_array)
        + polynomial.b * p_array
        + polynomial.c * np.power(p_array, 2)
        + polynomial.d * np.power(p_array, 3)
    )


def evaluate_parametric_cubic_curve_at_p(
    curve: ParametricCubicCurve, p_array: npt.NDArray[np.float32]
) -> npt.NDArray[np.float32]:
    r"""Return local (u, v) coordinates from an array of parameter $p \in [0.0, 1.0]$.

    (u, v) coordinates are in their own x,y frame: start at origin, and initial
    heading is along the x axis.

    Parameters
    ----------
    p_array : np.ndarray
        p values $\in [0.0, 1.0]$ to compute parametric coordinates.

    Returns:
    -------
    np.ndarray
        Array of local (u, v) coordinate pairs.
    """
    if curve.p_range == PolyRange.NORMALIZED:
        # Normalize p_array to [0, 1]
        p_array = p_array / curve.length

    u_array = evaluate_polynomial_at_p(curve.u_poly, p_array)
    v_array = evaluate_polynomial_at_p(curve.v_poly, p_array)

    return np.stack((u_array, v_array), axis=1)
