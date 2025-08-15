
from __future__ import annotations

from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import device_registry as dr

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL, OPT_SCAN_INTERVAL
from .coordinator import PumpCoordinator

PLATFORMS: list[str] = ["sensor", "binary_sensor", "button"]

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})

    api_key = entry.data["api_key"]
    device_id = entry.data["device_id"]
    coordinator = PumpCoordinator(hass, api_key, device_id)

    scan = int(entry.options.get(OPT_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL))
    coordinator.update_interval = timedelta(seconds=scan)

    await coordinator.async_config_entry_first_refresh()
    hass.data[DOMAIN][entry.entry_id] = coordinator

    devreg = dr.async_get(hass)
    devreg.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, device_id)},
        manufacturer="PUMP",
        name="Wallbox",
        model="Generic Wallbox (via PUMP Connect)",
    )

    entry.async_on_unload(entry.add_update_listener(_async_options_updated))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def _async_options_updated(hass: HomeAssistant, entry: ConfigEntry) -> None:
    from datetime import timedelta
    from .const import DEFAULT_SCAN_INTERVAL, OPT_SCAN_INTERVAL
    coordinator: PumpCoordinator = hass.data[DOMAIN][entry.entry_id]
    scan = int(entry.options.get(OPT_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL))
    coordinator.update_interval = timedelta(seconds=scan)
    await coordinator.async_request_refresh()

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok
