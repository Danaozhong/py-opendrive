import numpy.typing as npt
import numpy as np
from py_opendrive.geometries.road_reference_line import RoadReferenceLine


def evaluate_road_reference_line(
    road_reference_line: RoadReferenceLine, s_indices: npt.NDArray[np.float64]
) -> npt.NDArray[np.float64]:
    """Evaluates the road reference line geometry."""
    # s_points = calculate_geometry_evaluation_points(road_reference_line)

    current_geometry_index = 0
    current_geometry = road_reference_line.geometries[current_geometry_index]
    for s in s_indices:
        while (
            s > current_geometry.length
            and current_geometry_index < len(road_reference_line.geometries) - 1
        ):
            current_geometry_index += 1
            current_geometry = road_reference_line.geometries[current_geometry_index]
        # Evaluate the current geometry at s.

    # TODO implement evaluation logic.
