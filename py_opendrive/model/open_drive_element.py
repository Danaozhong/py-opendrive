from dataclasses import dataclass, field
from py_opendrive.model.roads.road import Road


@dataclass
class OpenDriveElement:
    roads: list[Road] = field(default_factory=list)
