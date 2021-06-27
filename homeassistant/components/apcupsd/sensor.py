"""Support for APCUPSd sensors."""
import logging

from apcaccess.status import ALL_UNITS

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_RESOURCES,
    CONF_SENSORS,
    ELECTRICAL_CURRENT_AMPERE,
    ELECTRICAL_VOLT_AMPERE,
    FREQUENCY_HERTZ,
    PERCENTAGE,
    POWER_WATT,
    TEMP_CELSIUS,
    TIME_MINUTES,
    TIME_SECONDS,
    VOLT,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DOMAIN, APCUPSDEntity, APCUPSDUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

SENSOR_PREFIX = "UPS "
SENSOR_TYPES = {
    "alarmdel": ["Alarm Delay", "", "mdi:alarm"],
    "ambtemp": ["Ambient Temperature", "", "mdi:thermometer"],
    "apc": ["Status Data", "", "mdi:information-outline"],
    "apcmodel": ["Model", "", "mdi:information-outline"],
    "badbatts": ["Bad Batteries", "", "mdi:information-outline"],
    "battdate": ["Battery Replaced", "", "mdi:calendar-clock"],
    "battstat": ["Battery Status", "", "mdi:information-outline"],
    "battv": ["Battery Voltage", VOLT, "mdi:flash"],
    "bcharge": ["Battery", PERCENTAGE, "mdi:battery"],
    "cable": ["Cable Type", "", "mdi:ethernet-cable"],
    "cumonbatt": ["Total Time on Battery", "", "mdi:timer-outline"],
    "date": ["Status Date", "", "mdi:calendar-clock"],
    "dipsw": ["Dip Switch Settings", "", "mdi:information-outline"],
    "dlowbatt": ["Low Battery Signal", "", "mdi:clock-alert"],
    "driver": ["Driver", "", "mdi:information-outline"],
    "dshutd": ["Shutdown Delay", "", "mdi:timer-outline"],
    "dwake": ["Wake Delay", "", "mdi:timer-outline"],
    "endapc": ["Date and Time", "", "mdi:calendar-clock"],
    "extbatts": ["External Batteries", "", "mdi:information-outline"],
    "firmware": ["Firmware Version", "", "mdi:information-outline"],
    "hitrans": ["Transfer High", VOLT, "mdi:flash"],
    "hostname": ["Hostname", "", "mdi:information-outline"],
    "humidity": ["Ambient Humidity", PERCENTAGE, "mdi:water-percent"],
    "itemp": ["Internal Temperature", TEMP_CELSIUS, "mdi:thermometer"],
    "lastxfer": ["Last Transfer", "", "mdi:transfer"],
    "linefail": ["Input Voltage Status", "", "mdi:information-outline"],
    "linefreq": ["Line Frequency", FREQUENCY_HERTZ, "mdi:information-outline"],
    "linev": ["Input Voltage", VOLT, "mdi:flash"],
    "loadpct": ["Load", PERCENTAGE, "mdi:gauge"],
    "loadapnt": ["Load Apparent Power", PERCENTAGE, "mdi:gauge"],
    "lotrans": ["Transfer Low", VOLT, "mdi:flash"],
    "mandate": ["Manufacture Date", "", "mdi:calendar"],
    "masterupd": ["Master Update", "", "mdi:information-outline"],
    "maxlinev": ["Input Voltage High", VOLT, "mdi:flash"],
    "maxtime": ["Battery Timeout", "", "mdi:timer-off-outline"],
    "mbattchg": ["Battery Shutdown", PERCENTAGE, "mdi:battery-alert"],
    "minlinev": ["Input Voltage Low", VOLT, "mdi:flash"],
    "mintimel": ["Shutdown Time", "", "mdi:timer-outline"],
    "model": ["Model", "", "mdi:information-outline"],
    "nombattv": ["Battery Nominal Voltage", VOLT, "mdi:flash"],
    "nominv": ["Nominal Input Voltage", VOLT, "mdi:flash"],
    "nomoutv": ["Nominal Output Voltage", VOLT, "mdi:flash"],
    "nompower": ["Nominal Output Power", POWER_WATT, "mdi:flash"],
    "nomapnt": ["Nominal Apparent Power", ELECTRICAL_VOLT_AMPERE, "mdi:flash"],
    "numxfers": ["Transfer Count", "", "mdi:counter"],
    "outcurnt": ["Output Current", ELECTRICAL_CURRENT_AMPERE, "mdi:flash"],
    "outputv": ["Output Voltage", VOLT, "mdi:flash"],
    "reg1": ["Register 1 Fault", "", "mdi:information-outline"],
    "reg2": ["Register 2 Fault", "", "mdi:information-outline"],
    "reg3": ["Register 3 Fault", "", "mdi:information-outline"],
    "retpct": ["Restore Requirement", PERCENTAGE, "mdi:battery-alert"],
    "selftest": ["Last Self Test", "", "mdi:calendar-clock"],
    "sense": ["Sensitivity", "", "mdi:information-outline"],
    "serialno": ["Serial Number", "", "mdi:information-outline"],
    "starttime": ["Startup Time", "", "mdi:calendar-clock"],
    "statflag": ["Status Flag", "", "mdi:information-outline"],
    "status": ["Status", "", "mdi:information-outline"],
    "stesti": ["Self Test Interval", "", "mdi:information-outline"],
    "timeleft": ["Time Left", "", "mdi:clock-alert"],
    "tonbatt": ["Time on Battery", "", "mdi:timer-outline"],
    "upsmode": ["Mode", "", "mdi:information-outline"],
    "upsname": ["Name", "", "mdi:information-outline"],
    "version": ["Daemon Info", "", "mdi:information-outline"],
    "xoffbat": ["Transfer from Battery", "", "mdi:transfer"],
    "xoffbatt": ["Transfer from Battery", "", "mdi:transfer"],
    "xonbatt": ["Transfer to Battery", "", "mdi:transfer"],
}

SPECIFIC_UNITS = {"ITEMP": TEMP_CELSIUS}
INFERRED_UNITS = {
    " Minutes": TIME_MINUTES,
    " Seconds": TIME_SECONDS,
    " Percent": PERCENTAGE,
    " Volts": VOLT,
    " Ampere": ELECTRICAL_CURRENT_AMPERE,
    " Volt-Ampere": ELECTRICAL_VOLT_AMPERE,
    " Watts": POWER_WATT,
    " Hz": FREQUENCY_HERTZ,
    " C": TEMP_CELSIUS,
    " Percent Load Capacity": PERCENTAGE,
}


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


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the APCUPSd sensors."""
    apcups_data = hass.data[DOMAIN]
    entities = []

    for resource in config[CONF_RESOURCES]:
        sensor_type = resource.lower()

        if sensor_type not in SENSOR_TYPES:
            SENSOR_TYPES[sensor_type] = [
                sensor_type.title(),
                "",
                "mdi:information-outline",
            ]

        if sensor_type.upper() not in apcups_data.status:
            _LOGGER.warning(
                "Sensor type: %s does not appear in the APCUPSd status output",
                sensor_type,
            )

        entities.append(APCUPSdSensor(apcups_data, sensor_type))

    add_entities(entities, True)


def infer_unit(value):
    """If the value ends with any of the units from ALL_UNITS.

    Split the unit off the end of the value and return the value, unit tuple
    pair. Else return the original value and None as the unit.
    """

    for unit in ALL_UNITS:
        if value.endswith(unit):
            return value[: -len(unit)], INFERRED_UNITS.get(unit, unit.strip())
    return value, None


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
