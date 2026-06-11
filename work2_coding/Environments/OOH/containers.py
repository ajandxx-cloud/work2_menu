from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

@dataclass
class Location:
    x: float
    y: float
    id_num: int #id only used for loaded data
    time: int#arrival time
    def __getitem__(self, item):
        return getattr(self, item)

@dataclass
class ParcelPoint:
    location: Location
    remainingCapacity: int
    id_num: int

@dataclass
class ParcelPoints:
    parcelpoints: List[ParcelPoint]
    def __getitem__(self, item):
        return getattr(self, item)

@dataclass
class Vehicle:
    routePlan: []
    capacity: int
    id_num: int
    def __getitem__(self, item):
        return getattr(self, item)
    
@dataclass
class Fleet:
    fleet: List[Vehicle]
    def __getitem__(self, item):
        return getattr(self, item)
    
@dataclass
class Customer:
    home: Location
    incentiveSensitivity: float
    home_util: float
    service_time: float
    id_num: int

@dataclass
class ServiceBundle:
    bundle_id: str
    location: Location
    is_home: bool
    parcelpoint_id: int
    window_start: float
    window_end: float
    window_center: float
    window_width: float
    remaining_capacity: float

    @property
    def window(self) -> Tuple[float, float]:
        return (self.window_start, self.window_end)

    def __getitem__(self, item):
        return getattr(self, item)

@dataclass
class MenuOffer:
    bundle: ServiceBundle
    predicted_cost: float
    price: float = 0.0
    predicted_eta: float = 0.0
    predicted_in_vehicle_time: float = 0.0
    walk_distance: float = 0.0
    time_deviation: float = 0.0
    predicted_utility: float = 0.0
    expected_profit: float = 0.0
    metadata: Optional[Dict[str, Any]] = field(default_factory=dict)

    @property
    def bundle_id(self) -> str:
        return self.bundle.bundle_id

    @property
    def is_home(self) -> bool:
        return self.bundle.is_home

    @property
    def location(self) -> Location:
        return self.bundle.location

    @property
    def parcelpoint_id(self) -> int:
        return self.bundle.parcelpoint_id

    @property
    def window(self) -> Tuple[float, float]:
        return self.bundle.window

    def __getitem__(self, item):
        return getattr(self, item)

@dataclass
class ChoiceResult:
    outcome: str
    location: Optional[Location]
    offer: Optional[MenuOffer]
    price: float
    parcelpoint_id: int
    route_mutates: bool
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def accepted_home(cls, location, offer=None, price=0.0, metadata=None):
        return cls(
            outcome="accepted_home",
            location=location,
            offer=offer,
            price=float(price),
            parcelpoint_id=-1,
            route_mutates=True,
            metadata=metadata or {},
        )

    @classmethod
    def accepted_meeting_point(cls, location, parcelpoint_id, offer=None, price=0.0, metadata=None):
        return cls(
            outcome="accepted_meeting_point",
            location=location,
            offer=offer,
            price=float(price),
            parcelpoint_id=int(parcelpoint_id),
            route_mutates=True,
            metadata=metadata or {},
        )

    @classmethod
    def opted_out(cls, metadata=None):
        return cls(
            outcome="opted_out",
            location=None,
            offer=None,
            price=0.0,
            parcelpoint_id=-1,
            route_mutates=False,
            metadata=metadata or {},
        )

    def __getitem__(self, item):
        return getattr(self, item)
