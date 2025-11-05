from dataclasses import dataclass


@dataclass
class Arc:
    """
    Represents an arc geometry in the OpenDRIVE format.
    """

    s: float = 0.0
    x: float = 0.0
    hdg: float = 0.0
    length: float = 0.0

    # The curvature of the arc.
    curvature: float = 0.0
