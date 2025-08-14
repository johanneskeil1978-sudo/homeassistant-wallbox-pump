
from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN

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
