from collections import defaultdict
import math
import numpy.typing as npt
import numpy as np
from py_opendrive.evaluator.evaluate_geometry import evaluate_geometry_at_p
from py_opendrive.evaluator.evaluated_lane_section import (
    EvaluatedLane,
    EvaluatedLaneSection,
)
from py_opendrive.evaluator.evaluation_properties import EvaluationProperties
from py_opendrive.geometries.road_reference_line import RoadReferenceLine
from py_opendrive.model.header import GeoRef
from py_opendrive.model.lanes.lane import Lane
from py_opendrive.model.lanes.lane_section import LaneSection
from py_opendrive.model.lanes.road_lanes import RoadLanes
import geopandas as gpd
import pandas as pd
from shapely.affinity import translate
from py_opendrive.evaluator.s_index_evaluation import SIndexEvaluationProperties


def evaluate_road_reference_line_at_s(
    road_reference_line: RoadReferenceLine, s: float
) -> npt.NDArray[np.float32]:
    """Evaluates the road reference line at a specific s position.

    Args:
        road_reference_line: The road reference line to evaluate.
        s: The s position along the road reference line.

    Returns:
        A tuple (x, y) representing the evaluated position.
    """
    s_start = 0.0

    for segment_index, geometry_segment in enumerate(road_reference_line.geometries):
        segment_length = geometry_segment.length
        s_end = s_start + segment_length

        if s <= s_end or segment_index == len(road_reference_line.geometries) - 1:
            p = s - s_start
            st_coordinates = evaluate_geometry_at_p(
                geometry_segment, np.array([p], dtype=np.float32)
            )
            xy_coordinates = st_coordinates_to_xy_coordinates(
                st_coordinates,
                geometry_segment.x,
                geometry_segment.y,
                geometry_segment.hdg,
            )
            return xy_coordinates[0]

        s_start = s_end

    raise ValueError(f"s value {s} is out of bounds for the given road reference line.")


def apply_offset(
    xy_coords: npt.NDArray[np.float32], global_transformation: GeoRef
) -> npt.NDArray[np.float32]:
    """Applies the geo reference offset to the given coordinates.

    Args:
        coords: An array of [x,y] coordinates to transform.
        global_transformation: The global transformation to apply.

    Returns:
        The transformed coordinates.
    """
    if global_transformation.offset is not None:
        rotation_matrix = np.array(
            [
                [1, 0],
                [0, 1],
            ],
            dtype=np.float32,
        )
        if global_transformation.offset.heading != 0.0:
            c, s = (
                np.cos(global_transformation.offset.heading),
                np.sin(global_transformation.offset.heading),
            )
            rotation_matrix = np.array([[c, -s], [s, c]], dtype=np.float32)

        # Translate and rotate the coordinates.
        xy_coords = np.dot(rotation_matrix, xy_coords.T).T
        xy_coords = xy_coords + np.array(
            [global_transformation.offset.x, global_transformation.offset.y],
            dtype=np.float32,
        )

    return xy_coords


def evaluate_segment_road_reference_line(
    road_reference_line: RoadReferenceLine,
    evaluation_properties: EvaluationProperties,
    s_properties: SIndexEvaluationProperties,
    global_transformation: GeoRef,
) -> gpd.GeoDataFrame:
    """Evaluates the road reference line geometry."""
    unique_forced_s_offsets = set(s_properties.forced_s_offsets)
    assert len(unique_forced_s_offsets) == len(s_properties.forced_s_offsets), (
        "Duplicate forced s offsets are not allowed."
    )

    # Determine where the current range should end.
    s_end = s_properties.s_end
    if s_end is None:
        s_end = road_reference_line.get_total_length()

    s_range = np.linspace(
        s_properties.s_start,
        s_end,
        num=int(
            (s_end - s_properties.s_start)
            * evaluation_properties.shape_points_per_meter
        )
        + 2,
    )

    assert s_end != s_properties.s_start, "s_end and s_start cannot be the same."
    forced_s = (
        np.array(s_properties.forced_s_offsets, dtype=np.float32) + s_properties.s_start
    )
    s_range = np.unique(np.concatenate((s_range, forced_s)))

    # Find the indices of the s values that correspond to the forced s offsets.
    s_index = 0

    s_properties.forced_s_offset_geometry_indices = []
    for forced_s_value in forced_s:
        while not np.isclose(
            forced_s[s_index], forced_s_value, atol=evaluation_properties.s_epsilon
        ):
            s_index += 1
            if s_index == len(forced_s):
                raise AssertionError(
                    f"Forced s value {forced_s_value} not found in s_range."
                )
        s_properties.forced_s_offset_geometry_indices.append(s_index)
    assert len(s_properties.forced_s_offset_geometry_indices) == len(
        s_properties.forced_s_offsets
    ), "Not all forced s offsets were found in the s range."

    xy_coordinates = np.empty((0, 2), dtype=np.float32)
    debug_attributes: dict[str, list] = defaultdict(list)

    s_idx_start = 0
    current_s_start = 0.0
    for geometry_segment_index, geometry_segment in enumerate(
        road_reference_line.geometries
    ):
        # Determine the s range for the current geometry segment.
        current_s_end = current_s_start + geometry_segment.length
        # Check if the current geometry segment contains any s values to evaluate.

        if (
            geometry_segment_index < len(road_reference_line.geometries) - 1
            or s_properties.s_end is not None
            or s_idx_start < len(s_range) - 1
        ):
            # If the segment starts after the current s_end, skip it.
            if s_range[s_idx_start] > current_s_end:
                current_s_start = current_s_end
                continue
        else:
            # This else branch is only here for documentation purposes. If the complete geometry
            # of the road reference line is evaluated, we want to make sure to include the last point.
            pass

        # end index is exclusive.
        s_idx_end = s_idx_start + 1
        while (
            s_idx_end < len(s_range)
            and s_range[s_idx_end - 1] < s_end
            and s_range[s_idx_end - 1] < current_s_end
        ):
            s_idx_end += 1

        if (
            s_properties.s_end is None
            and geometry_segment_index == len(road_reference_line.geometries) - 1
        ):
            s_idx_end = len(s_range)

        # Now we have the range [s_idx_start, s_idx_end) for the current segment.
        p_range = s_range[s_idx_start:s_idx_end] - current_s_start

        # Remember the geometry index and p for debugging purposes.
        debug_attributes["p"].extend(p_range.tolist())
        debug_attributes["geometry_index"].extend(
            [geometry_segment_index] * len(p_range)
        )
        debug_attributes["geometry_type"].extend(
            [geometry_segment.type().value] * len(p_range)
        )

        # Evaluate the geometry segment at the s values.
        st_coordinates = evaluate_geometry_at_p(geometry_segment, p_range)
        xy_coordinates = np.concatenate(
            (
                xy_coordinates,
                st_coordinates_to_xy_coordinates(
                    st_coordinates,
                    geometry_segment.x,
                    geometry_segment.y,
                    geometry_segment.hdg,
                ),
            ),
            axis=0,
        )

        if s_idx_end == len(s_range):
            break
        # Update the accumulated length.
        s_idx_start = s_idx_end
        current_s_start = current_s_end

    # Export everything as a GeoDataFrame.
    if len(s_range) != len(debug_attributes["p"]):
        raise AssertionError("Mismatch in lengths of s_range and debug attributes.")
    debug_attributes["s"] = s_range.tolist()

    reference_line_df = pd.DataFrame(debug_attributes)
    # We are using MERCATOR projection, because the units in ODR are in meters.
    reference_line_gdf = gpd.GeoDataFrame(
        data=reference_line_df,
        geometry=gpd.points_from_xy(
            xy_coordinates[:, 0], xy_coordinates[:, 1], crs=global_transformation.proj
        ),
    )

    # Apply the geo reference offset, if available.
    reference_line_gdf["geometry"] = reference_line_gdf["geometry"].transform(
        lambda coords: apply_offset(coords, global_transformation=global_transformation)
    )
    return reference_line_gdf


def st_coordinates_to_xy_coordinates(
    local_coords: npt.NDArray[np.float32],
    x_offset: float,
    y_offset: float,
    heading_offset: float,
) -> npt.NDArray[np.float32]:
    """Apply x and y (translation) and heading (rotation) offsets to local coords.

    Thereby generating coords in the global frame from coords in the local frame.
    N = number of coordinates
    D = dimension

    Parameters
    ----------
    local_coords : np.ndarray
        Array of local coords, [N, D].
    x_offset : float
        x offset value to be added to all local coordinates.
    y_offset : float
        y offset value to be added to all local coordinates.
    heading_offset : float
        Heading value (in radians) to rotate all local coordinates by.

    Returns:
    -------
    np.ndarray
        Resultant coordinates in the global frame.
    """
    offset_coordinates = np.array([x_offset, y_offset])

    # Rotate the shape points.
    c, s = np.cos(heading_offset), np.sin(heading_offset)
    rotation_matrix = np.array(((c, -s), (s, c)))

    # Translate to the set x and y positions.
    rotated_coords = np.dot(rotation_matrix, local_coords.T).T
    global_coords = rotated_coords + offset_coordinates

    return global_coords


def evaluate_lane_offset_at_s(road_lanes: RoadLanes, s: float) -> float:
    for lane_offset_idx, lane_offset in enumerate(road_lanes.lane_offset):
        if (
            lane_offset_idx == len(road_lanes.lane_offset) - 1
            or s < road_lanes.lane_offset[lane_offset_idx + 1].s
        ):
            ds = s - lane_offset.s
            return (
                lane_offset.a
                + lane_offset.b * ds
                + lane_offset.c * ds**2
                + lane_offset.d * ds**3
            )
    raise AssertionError(f"s value {s} not found in lane offsets.")


def evaluate_lane_width_at_s_offset(lane: Lane, s: float, s_start: float) -> float:
    s_offset = s - s_start
    for lane_width_idx, lane_width in enumerate(lane.width):
        if (
            lane_width_idx == len(lane.width) - 1
            or s_offset < lane.width[lane_width_idx + 1].s_offset
        ):
            ds = s_offset - lane_width.s_offset
            return (
                lane_width.a
                + lane_width.b * ds
                + lane_width.c * ds**2
                + lane_width.d * ds**3
            )
    # If no lane width is defined, the width is configured using the lane border.
    return math.nan


def evaluate_lane_border_at_s_offset(lane: Lane, s: float, s_start: float) -> float:
    s_offset = s - s_start
    for lane_border_idx, lane_border in enumerate(lane.border):
        if (
            lane_border_idx == len(lane.border) - 1
            or s_offset < lane.border[lane_border_idx + 1].s_offset
        ):
            ds = s_offset - lane_border.s_offset
            return (
                lane_border.a
                + lane_border.b * ds
                + lane_border.c * ds**2
                + lane_border.d * ds**3
            )
    # If no lane border is defined, the border is configured using the lane width.
    return math.nan


def get_lane_offset_vector_at_s(
    road_reference_line: RoadReferenceLine, s: float
) -> npt.NDArray[np.float32]:
    point1 = evaluate_road_reference_line_at_s(road_reference_line, s - 0.01)
    point2 = evaluate_road_reference_line_at_s(road_reference_line, s + 0.01)
    tangent_vector = point2 - point1
    tangent_vector = tangent_vector / np.linalg.norm(tangent_vector)
    orthogonal_vector = np.cross(
        np.array([0.0, 0.0, 1.0]), np.array([tangent_vector[0], tangent_vector[1], 0.0])
    )
    orthogonal_vector = orthogonal_vector[:2]
    return orthogonal_vector


def evaluate_lane_geometries(
    road_reference_line: RoadReferenceLine,
    road_lanes: RoadLanes,
    lane_section: LaneSection,
    evaluation_properties: EvaluationProperties,
    s_properties: SIndexEvaluationProperties,
    global_transformation: GeoRef,
) -> EvaluatedLaneSection:
    # Start by evaluating the reference line.

    reference_line_gdf = evaluate_segment_road_reference_line(
        road_reference_line,
        evaluation_properties,
        s_properties,
        global_transformation,
    )

    # Calculate the lane offset geometry, that is used to span out of all other lane geometries.
    lane_offset_gdf = reference_line_gdf[["s", "geometry"]].copy()

    lane_offset_gdf["normal_vector"] = lane_offset_gdf["s"].apply(
        lambda s: get_lane_offset_vector_at_s(road_reference_line, s)
    )
    lane_offset_gdf["lane_offset"] = lane_offset_gdf["s"].apply(
        lambda s: evaluate_lane_offset_at_s(road_lanes, s)
    )
    # Calculate the geometry shape points.
    lane_offset_gdf["geometry"] = lane_offset_gdf.apply(
        lambda row: translate(
            row["geometry"],
            xoff=row["normal_vector"][0] * row["lane_offset"],
            yoff=row["normal_vector"][1] * row["lane_offset"],
        ),
        axis=1,
    )

    boundaries_gdf: list[gpd.GeoDataFrame] = [lane_offset_gdf]
    left_lanes: list[EvaluatedLane] = []
    right_lanes: list[EvaluatedLane] = []
    # Calculate the lane geometries
    lane_collection: list[tuple[int, list[Lane]]] = [
        (1, lane_section.left),
        (-1, lane_section.right),
    ]

    for side, lanes in lane_collection:
        for lane_idx, lane in enumerate(lanes):
            lane_df = lane_offset_gdf[
                ["s", "normal_vector", "lane_offset", "geometry"]
            ].copy()
            if len(lane.width) > 0:
                lane_df["lane_width"] = lane_df.apply(
                    lambda row: evaluate_lane_width_at_s_offset(
                        lane,
                        row["s"],
                        s_properties.s_start,
                    ),
                    axis=1,
                )
                if lane_idx > 0:
                    # Add the width of all previous lanes.
                    lane_df["lane_width"] += boundaries_gdf[-1]["lane_width"]
            else:
                lane_df["lane_width"] = lane_df.apply(
                    lambda row: evaluate_lane_border_at_s_offset(
                        lane,
                        row["s"],
                        s_properties.s_start,
                    ),
                    axis=1,
                )

            # Calculate the geometry shape points.
            lane_df["geometry"] = lane_df.apply(
                lambda row: translate(
                    row["geometry"],
                    xoff=row["normal_vector"][0] * row["lane_width"],
                    yoff=row["normal_vector"][1] * row["lane_width"],
                ),
                axis=1,
            )

            # Store additional debug properties
            lane_df["lane_id"] = lane.id
            lane_df["lane_side"] = side

            # Lanes to the right have a negative index, lanes to the left have a positive index.
            lane_df["lane_number"] = (lane_idx + 1) * side
            boundaries_gdf.append(lane_df)

            evaluated_lane = EvaluatedLane(
                lane=lane,
                left_boundary_index=len(boundaries_gdf) - 2
                if side == 1
                else len(boundaries_gdf) - 1,
                right_boundary_index=len(boundaries_gdf) - 1
                if side == 1
                else len(boundaries_gdf) - 2,
            )

            if side == 1:
                left_lanes.append(evaluated_lane)
            else:
                right_lanes.append(evaluated_lane)

    return EvaluatedLaneSection(
        lane_section=lane_section,
        reference_line_geometry=reference_line_gdf,
        s_properties=s_properties,
        boundaries=[],
        left_lanes=left_lanes,
        right_lanes=right_lanes,
    )
