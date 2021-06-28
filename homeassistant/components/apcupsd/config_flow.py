"""Config flow to configure the APCUPSD integration."""
from __future__ import annotations

import logging
from typing import Any, OrderedDict

from apcaccess import status as apc
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .const import CONF_SENSORS, DEFAULT_HOST, DEFAULT_PORT, DOMAIN, SENSOR_TYPES

_LOGGER = logging.getLogger(__name__)


def get_sensors(data: dict) -> OrderedDict[str, str]:
    """Retrieve sensor data from APCUPSD."""
    return apc.parse(apc.get(host=data[CONF_HOST], port=data[CONF_PORT]))


class APCUPSDConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """APCUPSD config flow."""

    def __init__(self) -> None:
        """Initialize config flow."""
        self.data: dict[str, Any] = {}
        self.sensors: OrderedDict[str, str] = OrderedDict()

    async def async_step_user(self, user_input: ConfigType | None = None) -> FlowResult:
        """Handle user configuration flow."""
        if user_input is None:
            return self._show_setup_form()

        try:
            self.sensors = get_sensors(user_input)
        except Exception:
            _LOGGER.debug("NIS connection error", exc_info=True)
            return self._show_setup_form({"base": "cannot_connect"})

        self.data[CONF_HOST] = user_input[CONF_HOST]
        self.data[CONF_PORT] = user_input[CONF_PORT]

        return await self.async_step_sensor_select()

    async def async_step_sensor_select(
        self, user_input: ConfigType | None = None
    ) -> FlowResult:
        """Handle selecting sensors to use."""

        valid_sensors = {}

        for sensor in self.sensors.keys():
            if sensor.lower() in SENSOR_TYPES:
                valid_sensors[sensor.lower()] = SENSOR_TYPES[sensor.lower()][0]

        if user_input is None:
            return self._show_sensor_select_form(valid_sensors)

        self.data[CONF_SENSORS] = user_input[CONF_SENSORS]
        await self.async_set_unique_id(self.sensors["SERIALNO"])

        self._abort_if_unique_id_configured(
            updates={
                CONF_HOST: self.data[CONF_HOST],
                CONF_PORT: self.data[CONF_PORT],
                CONF_SENSORS: self.data[CONF_SENSORS],
            }
        )

        return self.async_create_entry(title=self.data[CONF_HOST], data=self.data)

    def _show_sensor_select_form(
        self, sensors: dict[str, str], errors: dict | None = None
    ) -> FlowResult:
        """Show the sensor select form to the user."""
        return self.async_show_form(
            step_id="sensor_select",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_SENSORS,
                    ): cv.multi_select(sensors),
                }
            ),
        )

    def _show_setup_form(self, errors: dict | None = None) -> FlowResult:
        """Show the setup form to the user."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST, default=DEFAULT_HOST): str,
                    vol.Required(CONF_PORT, default=DEFAULT_PORT): int,
                }
            ),
            errors=errors or {},
        )
