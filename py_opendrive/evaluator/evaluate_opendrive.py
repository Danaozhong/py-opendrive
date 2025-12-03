from py_opendrive.evaluator.evaluated_lane_section import (
    EvaluatedOpenDrive,
    EvaluatedRoad,
)
from py_opendrive.model.open_drive import OpenDrive
from py_opendrive.evaluator.evaluate_road_reference_line import evaluate_lane_geometries
from py_opendrive.evaluator.s_index_evaluation import SIndexEvaluationProperties
from py_opendrive.evaluator.evaluation_properties import EvaluationProperties
from typing import Optional


def evaluate_open_drive(
    opendrive: OpenDrive, evaluation_properties: EvaluationProperties
) -> EvaluatedOpenDrive:
    evaluated_open_drive = EvaluatedOpenDrive(evaluated_roads=[])

    for road in opendrive.roads:
        evaluated_road = EvaluatedRoad(evaluated_lane_sections=[], road=road)

        # The geometry need to be evaluated whenever a section starts.
        for lane_section_idx, lane_section in enumerate(road.lanes.lane_section):
            # Find the start and end s values for the lane section.
            start_s = lane_section.s
            end_s: Optional[float] = None
            if lane_section_idx + 1 < len(road.lanes.lane_section):
                end_s = road.lanes.lane_section[lane_section_idx + 1].s

            # Identify all s points where a geometry evaluation is needed. Any property change within the lane section requires an evaluation of the geometry as well, for example changes in speed limit.
            s_offset_values: set[int] = set()

            for lane in lane_section.left + lane_section.right:
                for width in lane.width:
                    s_offset_values.add(width.s_offset)
                for border in lane.border:
                    s_offset_values.add(border.s_offset)
                for rule in lane.rules:
                    s_offset_values.add(rule.s_offset)
                for material in lane.material:
                    s_offset_values.add(material.s_offset)

            s_properties = SIndexEvaluationProperties(
                s_start=start_s,
                s_end=end_s,
                forced_s_offsets=sorted(list(s_offset_values)),
                forced_s_offset_geometry_indices=[],
            )
            # evaluate the lanes
            evaluated_road.evaluated_lane_sections.append(
                evaluate_lane_geometries(
                    road.plan_view,
                    road.lanes,
                    lane_section,
                    evaluation_properties,
                    s_properties,
                    opendrive.header.get_geo_reference(),
                )
            )
        evaluated_open_drive.evaluated_roads.append(evaluated_road)
    return evaluated_open_drive
