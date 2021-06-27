"""Support for APCUPSd via its Network Information Server (NIS)."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import OrderedDict

from apcaccess import status as apc

from homeassistant.components.binary_sensor import DOMAIN as BINARY_SENSOR_DOMAIN
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

_LOGGER = logging.getLogger(__name__)

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 3551
SCAN_INTERVAL = timedelta(seconds=60)
DOMAIN = "apcupsd"

PLATFORMS = [BINARY_SENSOR_DOMAIN, SENSOR_DOMAIN]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up APCUPSD from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    coordinator = hass.data[DOMAIN].get(entry.entry_id)
    if not coordinator:
        coordinator = APCUPSDUpdateCoordinator(
            hass,
            host=entry.data[CONF_HOST],
            port=entry.data[CONF_PORT],
        )
        hass.data[DOMAIN][entry.entry_id] = coordinator

    await coordinator.async_config_entry_first_refresh()

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True


class APCUPSDUpdateCoordinator(DataUpdateCoordinator[OrderedDict]):
    """Class to manage fetching APCUPSD data from NIS."""

    def __init__(self, hass: HomeAssistant, host: str, port: str) -> None:
        """Initialize coordinator."""
        self._host = host
        self._port = port
        self._get = apc.get
        self._parse = apc.parse

        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL)

    async def _async_update_data(self) -> OrderedDict:
        """Fetch data from APCUPSD."""
        return self._parse(self._get(host=self._host, port=self._port))


class APCUPSDEntity(CoordinatorEntity):
    """Defines a base APCUPSD entity."""

    def __init__(
        self,
        *,
        entry_id: str,
        device_id: str,
        coordinator: APCUPSDUpdateCoordinator,
        name: str,
        icon: str,
        enabled_default: bool = True,
    ) -> None:
        """Initialize the APCUPSD entity."""
        super().__init__(coordinator)
        self._device_id = device_id
        self._enabled_default = enabled_default
        self._entry_id = entry_id
        self._icon = icon
        self._name = name

    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return self._name

    @property
    def icon(self) -> str:
        """Return the mdi icon of the entity."""
        return self._icon

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Return if the entity should be enabled when first added to the entity registry."""
        return self._enabled_default
