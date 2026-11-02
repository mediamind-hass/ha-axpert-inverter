import sys
import types


# Stub only the Home Assistant modules needed to import the custom component.
homeassistant = types.ModuleType("homeassistant")
config_entries = types.ModuleType("homeassistant.config_entries")
core = types.ModuleType("homeassistant.core")
exceptions = types.ModuleType("homeassistant.exceptions")
helpers = types.ModuleType("homeassistant.helpers")
helpers_typing = types.ModuleType("homeassistant.helpers.typing")
helpers_entity_platform = types.ModuleType("homeassistant.helpers.entity_platform")
helpers_update_coordinator = types.ModuleType("homeassistant.helpers.update_coordinator")
const = types.ModuleType("homeassistant.const")
components = types.ModuleType("homeassistant.components")
components_select = types.ModuleType("homeassistant.components.select")
components_sensor = types.ModuleType("homeassistant.components.sensor")
components_number = types.ModuleType("homeassistant.components.number")
util = types.ModuleType("homeassistant.util")
util_dt = types.ModuleType("homeassistant.util.dt")


class ConfigEntry:
    pass


class HomeAssistant:
    pass


class ServiceCall:
    pass


class ServiceValidationError(Exception):
    pass


class HomeAssistantError(Exception):
    pass


class SupportsResponse:
    OPTIONAL = "optional"


class DataUpdateCoordinator:
    def __init__(self, *args, **kwargs):
        pass


class CoordinatorEntity:
    def __init__(self, *args, **kwargs):
        pass


class RestoreEntity:
    pass


class SensorEntity:
    pass


class NumberEntity:
    pass


class SelectEntity:
    pass


class EntityCategory:
    CONFIG = "config"


class Entity:
    pass


config_entries.ConfigEntry = ConfigEntry
core.HomeAssistant = HomeAssistant
core.ServiceCall = ServiceCall
core.SupportsResponse = SupportsResponse
exceptions.ServiceValidationError = ServiceValidationError
exceptions.HomeAssistantError = HomeAssistantError
helpers_typing.ConfigType = dict
helpers_update_coordinator.DataUpdateCoordinator = DataUpdateCoordinator
helpers_update_coordinator.CoordinatorEntity = CoordinatorEntity
helpers_update_coordinator.UpdateFailed = Exception
helpers_entity_platform.AddEntitiesCallback = object
const.Platform = types.SimpleNamespace(
    SENSOR="sensor",
    SELECT="select",
    BINARY_SENSOR="binary_sensor",
    NUMBER="number",
)
const.EntityCategory = EntityCategory
const.UnitOfElectricPotential = types.SimpleNamespace(VOLT="V")
const.UnitOfElectricCurrent = types.SimpleNamespace(AMPERE="A")
const.UnitOfFrequency = types.SimpleNamespace(HERTZ="Hz")
const.UnitOfPower = types.SimpleNamespace(WATT="W")
const.UnitOfApparentPower = types.SimpleNamespace(VOLT_AMPERE="VA")
const.UnitOfEnergy = types.SimpleNamespace(KILO_WATT_HOUR="kWh")
const.UnitOfTemperature = types.SimpleNamespace(CELSIUS="°C")
const.PERCENTAGE = "%"
components_select.SelectEntity = SelectEntity
components_sensor.SensorEntity = SensorEntity
components_sensor.SensorDeviceClass = types.SimpleNamespace(
    VOLTAGE="voltage",
    FREQUENCY="frequency",
    POWER="power",
    APPARENT_POWER="apparent_power",
    BATTERY="battery",
    TEMPERATURE="temperature",
    CURRENT="current",
    ENERGY="energy",
)
components_sensor.SensorStateClass = types.SimpleNamespace(MEASUREMENT="measurement", TOTAL_INCREASING="total_increasing")
components_number.NumberEntity = NumberEntity
components_number.NumberDeviceClass = types.SimpleNamespace(CURRENT="current", VOLTAGE="voltage")
util_dt.utcnow = lambda: None

sys.modules["homeassistant"] = homeassistant
sys.modules["homeassistant.config_entries"] = config_entries
sys.modules["homeassistant.core"] = core
sys.modules["homeassistant.exceptions"] = exceptions
sys.modules["homeassistant.helpers"] = helpers
sys.modules["homeassistant.helpers.typing"] = helpers_typing
sys.modules["homeassistant.helpers.entity_platform"] = helpers_entity_platform
sys.modules["homeassistant.helpers.update_coordinator"] = helpers_update_coordinator
sys.modules["homeassistant.const"] = const
sys.modules["homeassistant.components"] = components
sys.modules["homeassistant.components.select"] = components_select
sys.modules["homeassistant.components.sensor"] = components_sensor
sys.modules["homeassistant.components.number"] = components_number
sys.modules["homeassistant.util"] = util
sys.modules["homeassistant.util.dt"] = util_dt

from custom_components.axpert_inverter import _is_allowed_command
from custom_components.axpert_inverter.axpert import AxpertInverter


def test_qpigs_too_short_returns_empty_dict(monkeypatch):
    inverter = AxpertInverter("/dev/ttyUSB0")
    monkeypatch.setattr(inverter, "send_command", lambda command: "bad")

    assert inverter.get_general_status() == {}


def test_allowed_command_whitelist():
    assert _is_allowed_command("QPIGS")
    assert _is_allowed_command("QPIWS")
    assert _is_allowed_command("PGR00")
    assert _is_allowed_command("MNCHGC060")
    assert not _is_allowed_command("rm -rf /")
    assert not _is_allowed_command("HELLO")


def test_qpigs_extended_fields_are_only_read_when_present(monkeypatch):
    inverter = AxpertInverter("/dev/ttyUSB0")
    monkeypatch.setattr(
        inverter,
        "send_command",
        lambda command: "230.0 50.0 230.0 50.0 0046 0002 000 371 53.20 001 080 0026 0001 089.9 53.13 00000 00110110 00000 00000 1234",
    )

    result = inverter.get_general_status()
    assert result["pv_charging_power"] == 1234
    assert result["status_binary"] == "00110110"
