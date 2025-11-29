import numpy as np
from py_opendrive.geometries.line import Line
from py_opendrive.geometries.road_reference_line import Geometries


def evaluate_geometry_at_s(geometry: Geometries, s: float):
    if isinstance(geometry, Line):
        return
    """Evaluates a given geometry at position s.
    
    Args:
        geometry: The geometry object to evaluate.
        s (float): The position along the geometry to evaluate.
    
    Returns:
        A tuple (x, y, hdg) representing the evaluated position and heading.
    """
    # TODO implement evaluation logic based on geometry type.
    pass


def evaluate_line_geometry(line: Line, s: float):
    """Evaluates a line geometry at position s."""
    x = line.x + s * np.cos(line.hdg)
    y = line.y + s * np.sin(line.hdg)
    hdg = line.hdg
    return x, y, hdg
