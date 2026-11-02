"""Constants for the Axpert Inverter integration."""

DOMAIN = "axpert_inverter"

# Configuration
CONF_DEVICE_PATH = "device_path"
CONF_SCAN_INTERVAL = "scan_interval"
# Default device path for a standard USB serial adapter exposed as ttyUSB0.
DEFAULT_PORT = "/dev/ttyUSB0"
DEFAULT_DEVICE_PATH = DEFAULT_PORT

# Default poll interval (seconds)
DEFAULT_SCAN_INTERVAL = 60

# Commands
CMD_QPIGS = "QPIGS"
CMD_QMOD = "QMOD"
CMD_QID = "QID"
CMD_PGR00 = "PGR00"  # Appliance range (Generator)
CMD_PGR01 = "PGR01"  # UPS range (Grid)

# Device Info
MANUFACTURER = "Voltronic/Axpert"
MODEL = "Axpert Inverter"
