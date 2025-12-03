from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SIndexEvaluationProperties:
    s_start: float = 0.0
    s_end: Optional[float] = None
    forced_s_offsets: list[float] = field(default_factory=list)

    # After evaluation of the geometry, this list tracks the indices of the geometry that correspond to `forced_s_offsets`.
    forced_s_offset_geometry_indices: list[int] = field(default_factory=list)
