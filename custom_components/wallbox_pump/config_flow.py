
from __future__ import annotations

from homeassistant import config_entries
import voluptuous as vol
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL, MIN_SCAN_INTERVAL, MAX_SCAN_INTERVAL, OPT_SCAN_INTERVAL

DATA_SCHEMA = vol.Schema({
    vol.Required("api_key"): str,
    vol.Required("device_id"): str,
})

class PumpConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Wallbox (PUMP)", data=user_input)
        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA)

    @staticmethod
    def async_get_options_flow(config_entry):
        return PumpOptionsFlow(config_entry)

class PumpOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        return await self.async_step_basic()

    async def async_step_basic(self, user_input=None):
        if user_input is not None:
            scan = int(user_input.get(OPT_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL))
            if scan < MIN_SCAN_INTERVAL:
                scan = MIN_SCAN_INTERVAL
            if scan > MAX_SCAN_INTERVAL:
                scan = MAX_SCAN_INTERVAL
            return self.async_create_entry(title="", data={OPT_SCAN_INTERVAL: scan})

        current = self.config_entry.options.get(OPT_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        schema = vol.Schema({
            vol.Required(OPT_SCAN_INTERVAL, default=current): vol.All(int, vol.Range(min=MIN_SCAN_INTERVAL, max=MAX_SCAN_INTERVAL))
        })
        return self.async_show_form(step_id="basic", data_schema=schema)
