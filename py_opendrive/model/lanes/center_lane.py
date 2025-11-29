from dataclasses import dataclass
from typing import Optional
from py_opendrive.model.enumerations import LaneType
from py_opendrive.model.lanes.lane_link import LaneLink


@dataclass
class CenterLane:
    id: int
    level: Optional[bool] = None
    type: Optional[LaneType] = None
    link: Optional[LaneLink] = None
