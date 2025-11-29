from dataclasses import dataclass, field


@dataclass
class LaneLink:
    predecessor: list[int] = field(default_factory=list)
    successor: list[int] = field(default_factory=list)
