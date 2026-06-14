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
class ServiceProduct:
    product_id: str
    product_mode: str
    time_window_mode: str
    menu_mode: str
    location: Optional[Location]
    window_start: Optional[float] = None
    window_end: Optional[float] = None
    window_center: Optional[float] = None
    window_width: Optional[float] = None
    price: float = 0.0
    is_home: bool = False
    parcelpoint_id: int = -1
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def window(self) -> Optional[Tuple[float, float]]:
        if self.window_start is None or self.window_end is None:
            return None
        return (self.window_start, self.window_end)

    @property
    def is_opt_out(self) -> bool:
        return self.location is None and self.metadata.get("outcome") == "opted_out"

    @classmethod
    def from_bundle(
        cls,
        bundle,
        product_mode="m+w",
        time_window_mode="fixed_window",
        menu_mode="optimized_menu",
        price=0.0,
        metadata=None,
    ):
        return cls(
            product_id=bundle.bundle_id,
            product_mode=product_mode,
            time_window_mode=time_window_mode,
            menu_mode=menu_mode,
            location=bundle.location,
            window_start=bundle.window_start,
            window_end=bundle.window_end,
            window_center=bundle.window_center,
            window_width=bundle.window_width,
            price=float(price),
            is_home=bool(bundle.is_home),
            parcelpoint_id=int(bundle.parcelpoint_id),
            metadata=dict(metadata or {}),
        )

    @classmethod
    def from_offer(
        cls,
        offer,
        product_mode=None,
        time_window_mode=None,
        menu_mode=None,
    ):
        metadata = dict(offer.metadata or {})
        return cls.from_bundle(
            offer.bundle,
            product_mode=product_mode or metadata.get("product_mode", "m+w+p"),
            time_window_mode=time_window_mode or metadata.get("time_window_mode", "fixed_window"),
            menu_mode=menu_mode or metadata.get("menu_mode", "optimized_menu"),
            price=offer.price,
            metadata=metadata,
        )

    @classmethod
    def opt_out(cls, metadata=None):
        meta = dict(metadata or {})
        meta.setdefault("outcome", "opted_out")
        return cls(
            product_id="opt_out",
            product_mode="outside_option",
            time_window_mode="no_time_window",
            menu_mode="outside_option",
            location=None,
            price=0.0,
            is_home=False,
            parcelpoint_id=-1,
            metadata=meta,
        )

    def to_bundle(self, remaining_capacity=0.0):
        if self.location is None:
            raise ValueError("opt-out service product cannot be converted to ServiceBundle")
        window_start = 0.0 if self.window_start is None else float(self.window_start)
        window_end = window_start if self.window_end is None else float(self.window_end)
        window_center = (window_start + window_end) / 2.0 if self.window_center is None else float(self.window_center)
        window_width = max(window_end - window_start, 0.0) if self.window_width is None else float(self.window_width)
        return ServiceBundle(
            bundle_id=self.product_id,
            location=self.location,
            is_home=bool(self.is_home),
            parcelpoint_id=int(self.parcelpoint_id),
            window_start=window_start,
            window_end=window_end,
            window_center=window_center,
            window_width=window_width,
            remaining_capacity=float(remaining_capacity),
        )

    def to_offer(self, predicted_cost=0.0, **kwargs):
        metadata = dict(self.metadata or {})
        metadata.update({
            "product_mode": self.product_mode,
            "time_window_mode": self.time_window_mode,
            "menu_mode": self.menu_mode,
        })
        return MenuOffer(
            bundle=self.to_bundle(remaining_capacity=kwargs.pop("remaining_capacity", 0.0)),
            predicted_cost=float(predicted_cost),
            price=float(self.price),
            metadata=metadata,
            **kwargs,
        )

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
