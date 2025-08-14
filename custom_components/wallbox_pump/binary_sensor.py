
from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([WallboxChargingBinarySensor(coordinator, entry)])

class WallboxChargingBinarySensor(CoordinatorEntity, BinarySensorEntity):
    _attr_name = "Charging"
    _attr_device_class = BinarySensorDeviceClass.POWER
    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self._attr_has_entity_name = True
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.device_id)},
            "manufacturer": "PUMP",
            "model": "Generic Wallbox",
            "name": "Wallbox",
        }
    def is_on(self):
        status = self.coordinator.data.get("session_status")
        power_w = self.coordinator.data.get("power_w", 0)
        return (status in ("ACTIVE", "STARTING")) or (power_w and power_w > 0)
