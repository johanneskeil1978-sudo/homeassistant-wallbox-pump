
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfPower, UnitOfEnergy, UnitOfTime
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    did = coordinator.device_id
    entities = [
        WallboxStatusSensor(coordinator, did),
        WallboxPowerSensor(coordinator, did),
        WallboxEnergySensor(coordinator, did),
        WallboxSessionDurationSensor(coordinator, did),
        WallboxSessionIdSensor(coordinator, did),
    ]
    async_add_entities(entities)

def _device_info(device_id: str) -> DeviceInfo:
    return DeviceInfo(
        identifiers={(DOMAIN, device_id)},
        manufacturer="PUMP",
        model="Generic Wallbox",
        name="Wallbox",
    )

class BasePumpSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, device_id: str, suffix: str):
        super().__init__(coordinator)
        self._attr_has_entity_name = True
        self._attr_device_info = _device_info(device_id)
        self._attr_unique_id = f"{DOMAIN}_{device_id}_{suffix}"

class WallboxStatusSensor(BasePumpSensor):
    _attr_name = "Status"
    def __init__(self, coordinator, device_id):
        super().__init__(coordinator, device_id, "status")
    @property
    def native_value(self):
        dev = self.coordinator.data.get("raw_device") or {}
        return dev.get("status", "UNKNOWN")

class WallboxPowerSensor(BasePumpSensor):
    _attr_name = "Power"
    _attr_device_class = SensorDeviceClass.POWER
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_state_class = SensorStateClass.MEASUREMENT
    def __init__(self, coordinator, device_id):
        super().__init__(coordinator, device_id, "power_w")
    @property
    def native_value(self):
        return self.coordinator.data.get("power_w", 0)

class WallboxEnergySensor(BasePumpSensor):
    _attr_name = "Energy"
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    def __init__(self, coordinator, device_id):
        super().__init__(coordinator, device_id, "energy_kwh")
    @property
    def native_value(self):
        return self.coordinator.data.get("energy_kwh", 0.0)

class WallboxSessionDurationSensor(BasePumpSensor):
    _attr_name = "Session Duration"
    _attr_native_unit_of_measurement = UnitOfTime.SECONDS
    _attr_state_class = SensorStateClass.MEASUREMENT
    def __init__(self, coordinator, device_id):
        super().__init__(coordinator, device_id, "session_duration_s")
    @property
    def native_value(self):
        return self.coordinator.data.get("duration_seconds", 0)

class WallboxSessionIdSensor(BasePumpSensor):
    _attr_name = "Active Session ID"
    def __init__(self, coordinator, device_id):
        super().__init__(coordinator, device_id, "active_session_id")
    @property
    def native_value(self):
        return self.coordinator.data.get("session_id") or ""
