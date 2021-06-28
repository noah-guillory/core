"""Support for APCUPSd sensors."""
import logging

from apcaccess.status import ALL_UNITS

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_SENSORS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import APCUPSDEntity, APCUPSDUpdateCoordinator
from .const import DOMAIN, INFERRED_UNITS, SENSOR_TYPES

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the APCUPSd sensors."""

    coordinator: APCUPSDUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    # config flow sets this to either UUID, serial number or None
    unique_id = entry.unique_id

    if unique_id is None:
        unique_id = entry.entry_id

    entities = []

    for sensor in entry.data[CONF_SENSORS]:
        if sensor not in SENSOR_TYPES:
            SENSOR_TYPES[sensor] = [
                sensor.title(),
                "",
                "mdi:information-outline",
            ]
        if sensor.upper() not in coordinator.data:
            _LOGGER.warning(
                "Sensor type: %s does not appear in the APCUPSd status output",
                sensor,
            )

        entities.append(APCUPSdSensor(entry.entry_id, unique_id, coordinator, sensor))

    async_add_entities(entities, True)


class APCUPSdSensor(APCUPSDEntity, SensorEntity):
    """Representation of a sensor entity for APCUPSd status values."""

    def __init__(
        self,
        entry_id: str,
        unique_id: str,
        coordinator: APCUPSDUpdateCoordinator,
        sensor_type,
        enabled_default: bool = True,
    ):
        """Initialize the sensor."""

        self.type = sensor_type
        self._unit = SENSOR_TYPES[sensor_type][1]
        self._inferred_unit = None

        super().__init__(
            entry_id=entry_id,
            device_id=unique_id,
            coordinator=coordinator,
            name=f"{coordinator.data['MODEL']} {SENSOR_TYPES[sensor_type][0]}",
            icon=SENSOR_TYPES[self.type][2],
            enabled_default=enabled_default,
        )

    @property
    def name(self):
        """Return the name of the UPS sensor."""
        return self._name

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return SENSOR_TYPES[self.type][2]

    @property
    def state(self):
        """Return sensor data."""
        return self.coordinator.data[self.type.upper()]

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        if not self._unit:
            if not self._inferred_unit:
                for unit in ALL_UNITS:
                    if self.state.endswith(unit):
                        self._inferred_unit = INFERRED_UNITS.get(unit, unit.strip())
                    self._inferred_unit = None
            return self._inferred_unit
        return self._unit
