from enum import Enum


class UnitDistance(Enum):
    FOOT = "ft"
    KILOMETER = "km"
    METER = "m"
    MILE = "mile"


class UnitSlope(Enum):
    PERCENT = "%"


class DataQualityRawDataSource(Enum):
    CADASTER = "cadaster"
    CUSTOM = "custom"
    SENSOR = "sensor"


class SpeedUnit(Enum):
    KILOMETER_PER_HOUR = "km/h"
    METER_PER_SECOND = "m/s"
    MILE_PER_HOUR = "mph"


class UnitMass(Enum):
    KILOGRAM = "kg"
    TON = "t"


class YesNo(Enum):
    NO = "no"
    YES = "yes"


class JunctionType(Enum):
    CROSSING = "crossing"
    DEFAULT = "default"
    DIRECT = "direct"
    VIRTUAL = "virtual"


class JunctionSegmentType(Enum):
    JOINT = "joint"
    LANE = "lane"


class JunctionGroupType(Enum):
    COMPLEX_JUNCTION = "complexJunction"
    HIGHWAY_INTERCHANGE = "highwayInterchange"
    ROUNDABOUT = "roundabout"
    UNKNOWN = "unknown"


class TrafficRule(Enum):
    LEFT_HAND_TRAFFIC = "LHT"
    RIGHT_HAND_TRAFFIC = "RHT"


class PolyRange(Enum):
    ARC_LENGTH = "arcLength"
    NORMALIZED = "normalized"


class RoadType(Enum):
    BICYCLE = "bicycle"
    LOW_SPEED = "lowSpeed"
    MOTORWAY = "motorway"
    PEDESTRIAN = "pedestrian"
    RURAL = "rural"
    TOWN_ARTERIAL = "townArterial"
    TOWN_COLLECTOR = "townCollector"
    TOWN_EXPRESSWAY = "townExpressway"
    TOWN_LOCAL = "townLocal"
    TOWN_PLAY_STREET = "townPlayStreet"
    TOWN_PRIVATE = "townPrivate"
    TOWN = "town"
    UNKNOWN = "unknown"


class LaneAdvisory(Enum):
    BOTH = "both"
    INNER = "inner"
    NONE = "none"
    OUTER = "outer"


class LaneDirection(Enum):
    BOTH = "both"
    REVERSED = "reversed"
    STANDARD = "standard"


class LaneType(Enum):
    HOV = "HOV"
    BIDIRECTIONAL = "bidirectional"
    BIKING = "biking"
    BORDER = "border"
    BUS = "bus"
    CONNECTING_RAMP = "connectingRamp"
    CURB = "curb"
    DRIVING = "driving"
    ENTRY = "entry"
    EXIT = "exit"
    MEDIAN = "median"
    MWY_ENTRY = "mwyEntry"
    MWY_EXIT = "mwyExit"
    NONE = "none"
    OFF_RAMP = "offRamp"
    ON_RAMP = "onRamp"
    PARKING = "parking"
    RAIL = "rail"
    RESTRICTED = "restricted"
    ROAD_WORKS = "roadWorks"
    SHARED = "shared"
    SHOULDER = "shoulder"
    SIDEWALK = "sidewalk"
    SLIP_LANE = "slipLane"
    SPECIAL1 = "special1"
    SPECIAL2 = "special2"
    SPECIAL3 = "special3"
    STOP = "stop"
    TAXI = "taxi"
    TRAM = "tram"
    WALKING = "walking"


class SignalSemanticsSpeed(Enum):
    MAXIMUM_END = "maximumEnd"
    MAXIMUM = "maximum"
    MINIMUM_END = "minimumEnd"
    MINIMUM = "minimum"
    RECOMMENDED_END = "recommendedEnd"
    RECOMMENDED = "recommended"
    ZONE_END = "zoneEnd"
    ZONE = "zone"
