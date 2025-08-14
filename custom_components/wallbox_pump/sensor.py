from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.const import POWER_WATT, ENERGY_KILO_WATT_HOUR, TIME_SECONDS
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = [
        WallboxStatusSensor(coordinator),
        WallboxPowerSensor(coordinator),
        WallboxEnergySensor(coordinator),
        WallboxSessionDurationSensor(coordinator),
        WallboxSessionIdSensor(coordinator),
    ]
    async_add_entities(entities)

class BasePumpSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_has_entity_name = True
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.device_id)},
            "manufacturer": "PUMP",
            "model": "Generic Wallbox",
            "name": "Wallbox",
        }

class WallboxStatusSensor(BasePumpSensor):
    _attr_name = "Status"
    @property
    def native_value(self):
        dev = self.coordinator.data.get("raw_device") or {}
        return dev.get("status", "UNKNOWN")

class WallboxPowerSensor(BasePumpSensor):
    _attr_name = "Power"
    _attr_device_class = SensorDeviceClass.POWER
    _attr_native_unit_of_measurement = POWER_WATT
    _attr_state_class = SensorStateClass.MEASUREMENT
    @property
    def native_value(self):
        return self.coordinator.data.get("power_w", 0)

class WallboxEnergySensor(BasePumpSensor):
    _attr_name = "Energy"
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_native_unit_of_measurement = ENERGY_KILO_WATT_HOUR
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    @property
    def native_value(self):
        return self.coordinator.data.get("energy_kwh", 0.0)

class WallboxSessionDurationSensor(BasePumpSensor):
    _attr_name = "Session Duration"
    _attr_native_unit_of_measurement = TIME_SECONDS
    _attr_state_class = SensorStateClass.MEASUREMENT
    @property
    def native_value(self):
        return self.coordinator.data.get("duration_seconds", 0)

class WallboxSessionIdSensor(BasePumpSensor):
    _attr_name = "Active Session ID"
    @property
    def native_value(self):
        return self.coordinator.data.get("session_id") or ""
