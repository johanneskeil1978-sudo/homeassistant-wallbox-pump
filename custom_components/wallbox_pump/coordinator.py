
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any, Dict

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import API_BASE, DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)

def _pick(d: dict, keys: list, default=None):
    """Try multiple key names or nested paths and return the first hit."""
    for k in keys:
        if isinstance(k, (list, tuple)):
            cur = d
            ok = True
            for part in k:
                if isinstance(cur, dict) and part in cur:
                    cur = cur[part]
                else:
                    ok = False
                    break
            if ok:
                return cur
        else:
            if isinstance(d, dict) and k in d:
                return d[k]
    return default

class PumpCoordinator(DataUpdateCoordinator[Dict[str, Any]]):
    def __init__(self, hass: HomeAssistant, api_key: str, device_id: str) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name="Wallbox (PUMP)",
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.api_key = api_key
        self.device_id = device_id

    async def _async_update_data(self) -> Dict[str, Any]:
        headers = {"x-api-key": self.api_key, "Accept-Encoding": "gzip"}
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(f"{API_BASE}/devices") as r1:
                    r1.raise_for_status()
                    devices = await r1.json()

                async with session.get(f"{API_BASE}/sessions?status=ACTIVE") as r2:
                    r2.raise_for_status()
                    sessions = await r2.json()
        except Exception as err:  # noqa: BLE001
            raise UpdateFailed(err) from err

        device = next((d for d in devices if d.get("id") == self.device_id), None)

        active_session = None
        if isinstance(sessions, dict) and isinstance(sessions.get("sessions"), list):
            active_session = next((s for s in sessions["sessions"] if s.get("device_id") == self.device_id), None)

        power_w = 0
        if device and device.get("connectors") and isinstance(device["connectors"], list) and device["connectors"]:
            power_w = device["connectors"][0].get("current_power") or 0

        energy_kwh = 0.0
        duration_seconds = 0
        session_status = None
        session_id = None
        if active_session:
            session_id = active_session.get("id")
            session_status = active_session.get("status")
            energy_kwh = _pick(active_session, ["energy_kwh", "energy", "charged_energy_kwh", ["metrics", "energy_kwh"]], 0.0) or 0.0
            duration_seconds = _pick(active_session, ["duration_seconds", "duration", "elapsed_seconds", ["metrics", "duration_seconds"]], 0) or 0
            if isinstance(duration_seconds, (int, float)) and duration_seconds > 1_000_000:
                duration_seconds = int(duration_seconds / 1000)

        return {
            "raw_device": device,
            "raw_active_session": active_session,
            "power_w": power_w,
            "energy_kwh": energy_kwh,
            "duration_seconds": duration_seconds,
            "session_status": session_status,
            "session_id": session_id,
        }
