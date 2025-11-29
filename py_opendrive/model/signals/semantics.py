from dataclasses import dataclass, field

from py_opendrive.model.enumerations import (
    SignalSemanticsSpeed as SignalSemanticsSpeedEnum,
    SpeedUnit,
)


@dataclass
class SignalSemanticsSpeed:
    type: SignalSemanticsSpeedEnum
    unit: SpeedUnit
    value: float


StreetName = str
Tourist = str
Warning = str


@dataclass
class Semantics:
    speed: list[SignalSemanticsSpeed] = field(default_factory=list)
    street_name: list[StreetName] = field(default_factory=list)
    tourist: list[Tourist] = field(default_factory=list)
    warning: list[Warning] = field(default_factory=list)
