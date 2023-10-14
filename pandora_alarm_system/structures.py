import logging
from copy import copy
from time import time
from types import MappingProxyType
from typing import (
    Any,
    Collection,
    Mapping,
    TypeVar,
    SupportsFloat,
    SupportsInt,
    MutableMapping,
    Final,
)

import attr

from .enums import (
    BitStatus,
    PrimaryEventID,
)

_LOGGER: Final = logging.getLogger(__name__)

_TKwargs = TypeVar("_TKwargs", bound=MutableMapping[str, Any])

_T = TypeVar("_T")


def _e(x: _T) -> _T | None:
    return x or None


def _f(x: SupportsFloat | None) -> float | None:
    try:
        return None if x is None else float(x)
    except (TypeError, ValueError):
        _LOGGER.warning(
            f"Could not convert value '{x}' to float, returning None"
        )
        return None


def _b(x: Any) -> bool | None:
    return None if x is None else bool(x)


def _i(x: SupportsInt | None) -> int | None:
    try:
        return None if x is None else int(x)
    except (TypeError, ValueError):
        _LOGGER.warning(
            f"Could not convert value '{x}' to int, returning None"
        )
        return None


def _degrees_to_direction(degrees: float):
    sides = (
        "N",
        "NNE",
        "NE",
        "ENE",
        "E",
        "ESE",
        "SE",
        "SSE",
        "S",
        "SSW",
        "SW",
        "WSW",
        "W",
        "WNW",
        "NW",
        "NNW",
    )
    return sides[round(degrees / (360 / len(sides))) % len(sides)]


def _dict_from_dict(
    data: Mapping[str, Any],
    kwargs: _TKwargs,
    to_merge: Mapping[str, str],
) -> _TKwargs:
    for kwarg, key in to_merge.items():
        if kwarg not in kwargs and key in data:
            kwargs[kwarg] = data[key]
    return kwargs


@attr.s(frozen=True, slots=True)
class BalanceState:
    value: float = attr.ib(converter=float)
    currency: str = attr.ib()

    def __float__(self) -> float:
        return self.value

    def __int__(self) -> int:
        return int(self.value)

    def __round__(self, n=None):
        return round(self.value, n)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any | None]):
        try:
            if data:
                return cls(
                    value=data["value"],
                    currency=data["cur"],
                )
        except (LookupError, TypeError, ValueError):
            pass


@attr.s(kw_only=True, frozen=True, slots=True)
class FuelTank:
    id: int = attr.ib()
    value: float = attr.ib()
    ras: float | None = attr.ib(default=None)
    ras_t: float | None = attr.ib(default=None)

    def __float__(self) -> float:
        return self.value

    def __int__(self) -> int:
        return int(self.value)

    def __round__(self, n=None):
        return round(self.value, n)


_TIMESTAMP_SOURCE: Final[str] = "timestamp_source"


@attr.s(kw_only=True, frozen=True, slots=True)
class CurrentState:
    identifier: int = attr.ib(converter=int)
    is_online: bool | None = attr.ib(default=None)
    latitude: float | None = attr.ib(default=None, converter=_f)
    longitude: float | None = attr.ib(default=None, converter=_f)
    speed: float | None = attr.ib(default=None, converter=_f)
    bit_state: BitStatus | None = attr.ib(default=None)
    engine_rpm: int | None = attr.ib(default=None, converter=_i)
    engine_temperature: float | None = attr.ib(default=None, converter=_f)
    interior_temperature: float | None = attr.ib(default=None, converter=_f)
    exterior_temperature: float | None = attr.ib(default=None, converter=_f)
    fuel: float | None = attr.ib(default=None, converter=_f)
    voltage: float | None = attr.ib(default=None, converter=_f)
    gsm_level: int | None = attr.ib(default=None, converter=_i)
    balance: BalanceState | None = attr.ib(default=None)
    balance_other: BalanceState | None = attr.ib(default=None)
    mileage: float | None = attr.ib(default=None, converter=_f)
    can_mileage: float | None = attr.ib(default=None, converter=_f)
    tag_number: int | None = attr.ib(default=None, converter=_i)
    key_number: int | None = attr.ib(default=None, converter=_i)
    relay: int | None = attr.ib(default=None, converter=_i)
    is_moving: bool | None = attr.ib(default=None, converter=_b)
    is_evacuating: bool | None = attr.ib(default=None, converter=_b)
    lock_latitude: float | None = attr.ib(default=None, converter=_f)
    lock_longitude: float | None = attr.ib(default=None, converter=_f)
    rotation: float | None = attr.ib(default=None, converter=_f)
    phone: str | None = attr.ib(default=None, converter=_e)
    imei: int | None = attr.ib(default=None, converter=_e)
    phone_other: str | None = attr.ib(default=None, converter=_e)
    active_sim: int | None = attr.ib(default=None)
    tracking_remaining: float | None = attr.ib(default=None, converter=_e)

    can_seat_taken: bool | None = attr.ib(default=None)
    can_average_speed: float | None = attr.ib(default=None)
    can_consumption: float | None = attr.ib(default=None)
    can_consumption_after: float | None = attr.ib(default=None)
    can_need_pads_exchange: bool | None = attr.ib(default=None)
    can_days_to_maintenance: int | None = attr.ib(default=None)
    can_tpms_front_left: float | None = attr.ib(default=None)
    can_tpms_front_right: float | None = attr.ib(default=None)
    can_tpms_back_left: float | None = attr.ib(default=None)
    can_tpms_back_right: float | None = attr.ib(default=None)
    can_tpms_reserve: float | None = attr.ib(default=None)
    can_glass_driver: bool | None = attr.ib(default=None)
    can_glass_passenger: bool | None = attr.ib(default=None)
    can_glass_back_left: bool | None = attr.ib(default=None)
    can_glass_back_right: bool | None = attr.ib(default=None)
    can_belt_driver: bool | None = attr.ib(default=None)
    can_belt_passenger: bool | None = attr.ib(default=None)
    can_belt_back_left: bool | None = attr.ib(default=None)
    can_belt_back_right: bool | None = attr.ib(default=None)
    can_belt_back_center: bool | None = attr.ib(default=None)
    can_low_liquid: bool | None = attr.ib(default=None)
    can_mileage_by_battery: float | None = attr.ib(default=None)
    can_mileage_to_empty: float | None = attr.ib(default=None)
    can_mileage_to_maintenance: float | None = attr.ib(default=None)

    ev_state_of_charge: float | None = attr.ib(default=None)
    ev_state_of_health: float | None = attr.ib(default=None)
    ev_charging_connected: bool | None = attr.ib(default=None)
    ev_charging_slow: bool | None = attr.ib(default=None)
    ev_charging_fast: bool | None = attr.ib(default=None)
    ev_status_ready: bool | None = attr.ib(default=None)
    battery_temperature: int | None = attr.ib(default=None)

    # undecoded parameters
    smeter: int | None = attr.ib(default=None)
    tconsum: int | None = attr.ib(default=None)
    loadaxis: Any = attr.ib(default=None)
    land: int | None = attr.ib(default=None)
    bunker: int | None = attr.ib(default=None)
    ex_status: int | None = attr.ib(default=None)
    fuel_tanks: Collection[FuelTank] = attr.ib(default=())

    state_timestamp: int | None = attr.ib(default=None)
    state_timestamp_utc: int | None = attr.ib(default=None)
    online_timestamp: int | None = attr.ib(default=None)
    online_timestamp_utc: int | None = attr.ib(default=None)
    settings_timestamp_utc: int | None = attr.ib(default=None)
    command_timestamp_utc: int | None = attr.ib(default=None)

    _attribute_timestamps: dict[str, int | None] = attr.ib(factory=dict)

    _timestamp_whitelist = frozenset(
        (
            "identifier",
            "state_timestamp",
            "state_timestamp_utc",
            "online_timestamp",
            "online_timestamp_utc",
            "settings_timestamp_utc",
            "command_timestamp_utc",
            "_attribute_timestamps",
        )
    )

    @property
    def newest_update_timestamp(self) -> int | None:
        newest = None
        # max doesn't work well with None-values
        for key, value in self._attribute_timestamps.items():
            if value is not None and (newest is None or value > newest):
                newest = value
        return newest

    @property
    def oldest_update_timestamp(self) -> int | None:
        oldest = None
        # min doesn't work well with None-values
        for key, value in self._attribute_timestamps.items():
            if value is not None and (oldest is None or value < oldest):
                oldest = value
        return oldest

    @property
    def direction(self) -> str:
        """Textual interpretation of rotation."""
        return _degrees_to_direction(self.rotation or 0.0)

    @property
    def attribute_timestamps(self) -> Mapping[str, Any]:
        """Get proxy mapping of last updates."""
        return MappingProxyType(self._attribute_timestamps)

    @classmethod
    def filter_timestamp_args(
        cls, state: "CurrentState", state_timestamp: int = None, **kwargs
    ) -> dict[str, Any]:
        """
        Filters new keyword arguments for state evolving.
        If state timestamp is provided, checks against existing values.
        If state timestamp is missing, uses current timestamp for new values.
        :param state: Existing state object
        :param state_timestamp:
        :param kwargs:
        :return:
        """
        if "attribute_timestamps" in kwargs:
            raise ValueError(
                "setting attribute timestamps on init is forbidden"
            )

        # reduces getattrs
        timestamps = {} if state is None else state._attribute_timestamps

        if state_timestamp is None:
            if state is not None:
                # prepare for timestamp copying
                state_timestamp = state.state_timestamp
        else:
            # filter invalid kwargs
            for kwarg in tuple(kwargs.keys() - cls._timestamp_whitelist):
                if (
                    ts := timestamps.get(kwarg)
                ) is not None and ts > state_timestamp:
                    kwargs.pop(kwarg)

        # init new timestamps dictionary
        timestamps = copy(timestamps)
        for kwarg in kwargs.keys() - cls._timestamp_whitelist:
            timestamps[kwarg] = state_timestamp

        kwargs["attribute_timestamps"] = timestamps
        kwargs["state_timestamp"] = state_timestamp

        return kwargs

    @classmethod
    def get_common_dict_args(
        cls, data: Mapping[str, Any], **kwargs
    ) -> dict[str, Any]:
        if "identifier" not in kwargs:
            try:
                device_id = data["dev_id"]
            except KeyError:
                device_id = data["id"]
            kwargs["identifier"] = int(device_id)
        if "balance" not in kwargs and "balance" in data:
            kwargs["balance"] = BalanceState.from_dict(data["balance"])
        if "balance_other" not in kwargs and "balance1" in data:
            kwargs["balance_other"] = BalanceState.from_dict(data["balance"])
        if "bit_state" not in kwargs and "bit_state_1" in data:
            kwargs["bit_state"] = BitStatus(int(data["bit_state_1"]))
        # dtime
        # dtime_rec
        # land
        # liquid_sensor
        # online -- different on HTTP, value not timestamp
        # smeter
        # tanks -- unknown for http
        return _dict_from_dict(
            data,
            kwargs,
            {
                "active_sim": "active_sim",
                "key_number": "brelok",
                "bunker": "bunker",
                "interior_temperature": "cabin_temp",
                "engine_rpm": "engine_rpm",
                "engine_temperature": "engine_temp",
                "is_evacuating": "evaq",
                "ex_status": "ex_status",
                "fuel": "fuel",
                "gsm_level": "gsm_level",
                "tag_number": "metka",
                "mileage": "mileage",
                "can_mileage": "mileage_CAN",
                "is_moving": "move",
                "exterior_temperature": "out_temp",
                "relay": "relay",
                "rotation": "rot",
                "speed": "speed",
                "voltage": "voltage",
                "latitude": "x",
                "longitude": "y",
            },
        )

    @classmethod
    def get_can_args(cls, data: Mapping[str, Any], **kwargs) -> dict[str, Any]:
        return _dict_from_dict(
            data,
            kwargs,
            {
                # Tire pressure
                "can_tpms_front_left": "CAN_TMPS_forvard_left",
                "can_tpms_front_right": "CAN_TMPS_forvard_right",
                "can_tpms_back_left": "CAN_TMPS_back_left",
                "can_tpms_back_right": "CAN_TMPS_back_right",
                "can_tpms_reserve": "CAN_TMPS_reserve",
                # Glasses
                "can_glass_driver": "CAN_driver_glass",
                "can_glass_passenger": "CAN_passenger_glass",
                "can_glass_back_left": "CAN_back_left_glass",
                "can_glass_back_right": "CAN_back_right_glass",
                # Belts
                "can_belt_driver": "CAN_driver_belt",
                "can_belt_passenger": "CAN_passenger_belt",
                "can_belt_back_left": "CAN_back_left_belt",
                "can_belt_back_right": "CAN_back_right_belt",
                "can_belt_back_center": "CAN_back_center_belt",
                # Mileages (non-generic)
                "can_mileage_by_battery": "CAN_mileage_by_battery",
                "can_mileage_to_empty": "CAN_mileage_to_empty",
                "can_mileage_to_maintenance": "CAN_mileage_to_maintenance",
                # EV-related
                "ev_charging_connected": "charging_connect",
                "ev_charging_slow": "charging_slow",
                "ev_charging_fast": "charging_fast",
                "ev_state_of_charge": "SOC",
                "ev_state_of_health": "SOH",
                "ev_status_ready": "ev_status_ready",
                "battery_temperature": "battery_temperature",
                # Miscellaneous
                "can_average_speed": "CAN_average_speed",
                "can_low_liquid": "CAN_low_liquid",
                "can_seat_taken": "CAN_seat_taken",
                "can_consumption": "CAN_consumption",
                "can_consumption_after": "CAN_consumption_after",
                "can_need_pads_exchange": "CAN_need_pads_exchange",
                "can_days_to_maintenance": "CAN_days_to_maintenance",
            },
        )

    @classmethod
    def get_ws_state_args(
        cls, data: Mapping[str, Any], **kwargs
    ) -> dict[str, Any]:
        if "is_online" not in kwargs and "online_mode" in data:
            kwargs["is_online"] = bool(data["online_mode"])
        if "lock_latitude" not in kwargs and "lock_x" in data:
            if (lock_x := data["lock_x"]) is not None:
                lock_x = float(lock_x) / 1000000
            kwargs["lock_latitude"] = lock_x
        if "lock_longitude" not in kwargs and "lock_y" in data:
            if (lock_y := data["lock_y"]) is not None:
                lock_y = float(lock_y) / 1000000
            kwargs["lock_longitude"] = lock_y / 1000000
        # if "tanks" in data:
        #     kwargs["fuel_tanks"] = FuelTank.parse_fuel_tanks(data["tanks"])
        return _dict_from_dict(
            data,
            cls.get_common_dict_args(data, **cls.get_can_args(data, **kwargs)),
            {
                "state_timestamp": "state",
                "state_timestamp_utc": "state_utc",
                "online_timestamp": "online",
                "online_timestamp_utc": "online_utc",
                "settings_timestamp_utc": "setting_utc",
                "command_timestamp_utc": "command_utc",
                "active_sim": "active_sim",
                "tracking_remaining": "track_remains",
            },
        )

    @classmethod
    def get_ws_point_args(
        cls, data: Mapping[str, Any], **kwargs
    ) -> dict[str, Any]:
        # flags ...
        # max_speed ...
        # timezone ...
        # Lbs_coords ...
        return cls.get_common_dict_args(data, **kwargs)

    @classmethod
    def get_http_dict_args(
        cls, data: Mapping[str, Any], **kwargs
    ) -> dict[str, Any]:
        # parse CAN data if present
        if can := data.get("can"):
            kwargs = cls.get_can_args(can, **kwargs)
        return cls.get_common_dict_args(data, **kwargs)


@attr.s(kw_only=True, frozen=True, slots=True)
class TrackingEvent:
    identifier: int = attr.ib()
    device_id: int = attr.ib()
    bit_state: BitStatus = attr.ib()
    cabin_temperature: float = attr.ib()
    engine_rpm: float = attr.ib()
    engine_temperature: float = attr.ib()
    event_id_primary: int = attr.ib()
    event_id_secondary: int = attr.ib()
    fuel: int = attr.ib()
    gsm_level: int = attr.ib()
    exterior_temperature: int = attr.ib()
    voltage: float = attr.ib()
    latitude: float = attr.ib()
    longitude: float = attr.ib()
    timestamp: int = attr.ib()
    recorded_timestamp: int = attr.ib()

    @property
    def primary_event_enum(self) -> PrimaryEventID:
        return PrimaryEventID(self.event_id_primary)

    @classmethod
    def get_dict_args(cls, data: Mapping[str, Any], **kwargs):
        if "identifier" not in kwargs:
            kwargs["identifier"] = int(data["id"])
        if "device_id" not in kwargs:
            kwargs["device_id"] = int(data["dev_id"])
        if "bit_state" not in kwargs:
            kwargs["bit_state"] = BitStatus(int(data["bit_state_1"]))
        if "cabin_temperature" not in kwargs:
            kwargs["cabin_temperature"] = data["cabin_temp"]
        if "engine_rpm" not in kwargs:
            kwargs["engine_rpm"] = data["engine_rpm"]
        if "engine_temperature" not in kwargs:
            kwargs["engine_temperature"] = data["engine_temp"]
        if "event_id_primary" not in kwargs:
            kwargs["event_id_primary"] = data["eventid1"]
        if "event_id_secondary" not in kwargs:
            kwargs["event_id_secondary"] = data["eventid2"]
        if "fuel" not in kwargs:
            kwargs["fuel"] = data["fuel"]
        if "gsm_level" not in kwargs:
            kwargs["gsm_level"] = data["gsm_level"]
        if "exterior_temperature" not in kwargs:
            kwargs["exterior_temperature"] = data["out_temp"]
        if "timestamp" not in kwargs:
            try:
                timestamp = data["dtime"]
            except KeyError:
                timestamp = data["time"]
            kwargs["timestamp"] = timestamp
        if "recorded_timestamp" not in kwargs:
            kwargs["recorded_timestamp"] = data["dtime_rec"]
        if "voltage" not in kwargs:
            kwargs["voltage"] = data["voltage"]
        if "latitude" not in kwargs:
            kwargs["latitude"] = data["x"]
        if "longitude" not in kwargs:
            kwargs["longitude"] = data["y"]
        return kwargs

    @classmethod
    def from_dict(cls, data: Mapping[str, Any], **kwargs):
        return cls(**cls.get_dict_args(data, **kwargs))


@attr.s(kw_only=True, frozen=True, slots=True)
class TrackingPoint:
    device_id: int = attr.ib()
    latitude: float = attr.ib()
    longitude: float = attr.ib()
    track_id: int | None = attr.ib(default=None)
    timestamp: float = attr.ib(default=time)
    fuel: int | None = attr.ib(default=None)
    speed: float | None = attr.ib(default=None)
    max_speed: float | None = attr.ib(default=None)
    length: float | None = attr.ib(default=None)
