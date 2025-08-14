
from __future__ import annotations

import aiohttp
from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN, API_BASE

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    did = coordinator.device_id
    async_add_entities([WallboxStartButton(coordinator, did), WallboxStopButton(coordinator, did)])

def _device_info(device_id: str) -> DeviceInfo:
    return DeviceInfo(
        identifiers={(DOMAIN, device_id)},
        manufacturer="PUMP",
        model="Generic Wallbox",
        name="Wallbox",
    )

class BasePumpButton(CoordinatorEntity, ButtonEntity):
    def __init__(self, coordinator, device_id: str, suffix: str):
        super().__init__(coordinator)
        self._attr_has_entity_name = True
        self._attr_device_info = _device_info(device_id)
        self._attr_unique_id = f"{DOMAIN}_{device_id}_{suffix}"

class WallboxStartButton(BasePumpButton):
    _attr_name = "Start"
    def __init__(self, coordinator, device_id: str):
        super().__init__(coordinator, device_id, "start")
    async def async_press(self):
        headers = {"x-api-key": self.coordinator.api_key, "Content-Type": "application/json", "Accept-Encoding": "gzip"}
        async with aiohttp.ClientSession(headers=headers) as session:
            await session.post(f"{API_BASE}/devices/{self.coordinator.device_id}/remote-start", json={"connector_id": 1})
        await self.coordinator.async_request_refresh()

class WallboxStopButton(BasePumpButton):
    _attr_name = "Stop"
    def __init__(self, coordinator, device_id: str):
        super().__init__(coordinator, device_id, "stop")
    async def async_press(self):
        session_id = self.coordinator.data.get("session_id")
        if not session_id:
            return
        headers = {"x-api-key": self.coordinator.api_key, "Accept-Encoding": "gzip"}
        async with aiohttp.ClientSession(headers=headers) as session:
            await session.post(f"{API_BASE}/sessions/{session_id}/remote-stop")
        await self.coordinator.async_request_refresh()
