from dataclasses import dataclass, field
import geopandas as gpd
from py_opendrive.evaluator.s_index_evaluation import SIndexEvaluationProperties
from py_opendrive.model.roads.road import Road
from py_opendrive.model.lanes.lane import Lane
from py_opendrive.model.lanes.lane_section import LaneSection
import numpy as np


@dataclass
class EvaluatedLane:
    lane: Lane
    left_boundary_index: int
    right_boundary_index: int


@dataclass
class EvaluatedLaneSection:
    lane_section: LaneSection = field(default_factory=LaneSection)
    reference_line_geometry: gpd.GeoDataFrame = field(default_factory=gpd.GeoDataFrame)
    boundaries: list[gpd.GeoDataFrame] = field(default_factory=list)
    left_lanes: list[EvaluatedLane] = field(default_factory=list)
    right_lanes: list[EvaluatedLane] = field(default_factory=list)

    s_properties: SIndexEvaluationProperties = field(
        default_factory=SIndexEvaluationProperties
    )

    def get_geometry_index_for_s(self, s: float) -> int:
        """Gets the geometry index for a given s position within the lane section."""
        s_values = self.reference_line_geometry["s"].values

        for i in range(len(s_values) - 1):
            if np.isclose(s, s_values[i]):
                return i
        raise AssertionError(
            f"s value {s} not found in reference line geometry s values."
        )


@dataclass
class EvaluatedRoad:
    evaluated_lane_sections: list[EvaluatedLaneSection]

    road: Road


@dataclass
class EvaluatedOpenDrive:
    evaluated_roads: list[EvaluatedRoad]
