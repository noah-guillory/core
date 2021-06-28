"""Constants for APCUPSD integration."""
from homeassistant.const import (
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

DOMAIN = "apcupsd"

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 3551

KEY_STATUS = "STATFLAG"
VALUE_ONLINE = 8

CONF_SENSORS = "sensors"

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
