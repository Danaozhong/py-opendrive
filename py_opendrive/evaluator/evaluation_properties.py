from dataclasses import dataclass


@dataclass
class EvaluationProperties:
    """A class to specify how the OpenDRIVE data is evaluated."""

    # Specify how many shape points should be generated when evaluating the OpenDRIVE geometries.
    # By default, one shape point per meter is generated.
    shape_points_per_meter: float = 1.0

    # The distance for which two s values are considered equal, in meters.
    s_epsilon: float = 0.01  # ~1 cm.

    # In case of linear geometries, trivial shape points (i.e., points that lie exactly on a straight line between two other points)
    # can be removed to reduce the number of shape points.
    remove_trivial_shape_points: bool = False

    # Whether to include shape points at geometry boundaries (e.g. when a road reference line geometry changes).
    include_shape_points_at_geometry_boundaries: bool = False
