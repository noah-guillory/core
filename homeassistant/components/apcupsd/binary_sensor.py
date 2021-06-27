"""Support for tracking the online status of a UPS."""
from __future__ import annotations

import voluptuous as vol

from homeassistant.components.binary_sensor import PLATFORM_SCHEMA, BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import APCUPSDEntity, APCUPSDUpdateCoordinator
from .const import DOMAIN, KEY_STATUS, VALUE_ONLINE

DEFAULT_NAME = "UPS Online Status"
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string}
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Create binary sensor for online status from config entry."""
    coordinator: APCUPSDUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    # config flow sets this to either UUID, serial number or None
    unique_id = entry.unique_id

    if unique_id is None:
        unique_id = entry.entry_id

    async_add_entities([OnlineStatus(entry.entry_id, unique_id, coordinator)], True)


class OnlineStatus(APCUPSDEntity, BinarySensorEntity):
    """Representation of an UPS online status."""

    def __init__(
        self,
        entry_id: str,
        unique_id: str,
        coordinator: APCUPSDUpdateCoordinator,
        enabled_default: bool = True,
    ) -> None:
        """Initialize APCUPSD sensor."""
        self._unique_id = None

        super().__init__(
            entry_id=entry_id,
            device_id=unique_id,
            coordinator=coordinator,
            name=f"{coordinator.data['MODEL']} Status",
            icon="mdi:power-plug",
            enabled_default=enabled_default,
        )

    @property
    def is_on(self):
        """Return true if the UPS is online, else false."""
        return int(self.coordinator.data[KEY_STATUS], 16) & VALUE_ONLINE > 0
