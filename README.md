# Axpert Inverter Home Assistant Integration

This custom component integrates Axpert Inverters directly into Home Assistant over a **USB serial** port (`pyserial`), replacing the need for external tools like `mppsolar` or MQTT bridges. It communicates with the inverter using the QPIGS protocol at **2400 baud, 8N1**.

This repository is a **fork** of the original project by Arnau Mora:

- Upstream: https://github.com/ArnyminerZ/ha-axpert-inverter.git

The original integration talks to the inverter as a USB HID device (`/dev/hidrawX`). This fork uses a serial device instead (default **`/dev/ttyUSB0`**) so setups that expose the inverter as a TTY can connect without HID.

> [!WARNING]
> **Disclaimer:** This integration interacts directly with your hardware. Incorrect configuration or usage could potentially cause damage to your inverter or connected devices. The creators and contributors of this integration take **no responsibility** for any damage, data loss, or other issues that may arise from using this software. Use at your own risk.

> [!IMPORTANT]
> This integration is not affiliated with or endorsed by Axpert.
> It is a completely independent project, backed up by the community, and based on official documentation, commands, and reverse engineering.

> [!NOTE]
> **Disclaimer:** this project has been generated mainly by AI. Even though it has been reviewed and tested by a professional programmer, I feel like it's important to disclose this fact.

## Fork changes

Compared to [ArnyminerZ/ha-axpert-inverter](https://github.com/ArnyminerZ/ha-axpert-inverter):

| | Original (upstream) | This fork |
| --- | --- | --- |
| Transport | USB HID (`pyusb`, `/dev/hidraw0`) | Serial (`pyserial`, `/dev/ttyUSB0`) |
| Port default | `/dev/hidraw0` | `/dev/ttyUSB0` |
| Serial settings | n/a | `2400` baud, 8 data bits, no parity, 1 stop bit, 5 s timeout |
| Device path | Ignored at runtime (VID:PID `0665:5161`) | The configured path is opened with `serial.Serial` |

Home Assistant will install the `pyserial` requirement from `manifest.json` when the integration is loaded.

If your host exposes a different TTY (for example `/dev/ttyUSB0` or `/dev/ttyACM0`), set that path in the integration options. Keep using `/dev/usbtty0` when that is the node created on your system.

## Features

- **Direct Communication**: Reads data from the serial device (default `/dev/usbtty0`), no separate MQTT broker required.
- **Real-time Sensors**:
    - Grid Voltage & Frequency
    - AC Output Voltage, Frequency, Active Power (W), Apparent Power (VA)
    - Battery Voltage, Charging Current, Capacity (%)
    - PV Input Voltage, Current, and Power
- **Energy Metering**:
    - Built-in kWh accumulation for **PV Energy** (Solar Generation) and **Load Energy** (Consumption).
    - Fully compatible with the **Home Assistant Energy Dashboard**.
- **Control**:
    - **AC Input Range Selection**: Switch between "Appliance" (Generator friendly) and "UPS" (Grid) modes directly from HA.
- **Diagnostics**:
    - Reports Inverter Firmware Version.

## Prerequisites
### Prepare the Device
Ensure your Home Assistant host has access to the inverter's USB serial device.

- Default path in this fork: `/dev/ttyUSB0`.
- If using Docker / Home Assistant OS add-ons, map the device, for example:
  `--device /dev/ttyUSB0:/dev/ttyUSB0`
- Stop any other services using the same port (e.g. `mppsolar` container).
- Home Assistant needs read/write permission on the TTY.

## Installation

### Option 1: HACS (Recommended)
1.  Open **HACS** in Home Assistant.
2.  Go to **Integrations** > **Three dots (top right)** > **Custom repositories**.
3.  Add the URL of **this** repository (the fork) and select **Integration** as the category.
4.  Click **ADD**.
5.  Find **Axpert Inverter** in the list and click **Download**.
6.  Restart Home Assistant.

To use the original HID-based integration instead, add [ArnyminerZ/ha-axpert-inverter](https://github.com/ArnyminerZ/ha-axpert-inverter).

### Option 2: Manual Installation
1.  Copy the `custom_components/axpert_inverter` directory into your Home Assistant's `config/custom_components/` folder.
    ```bash
    cp -r custom_components/axpert_inverter /config/custom_components/
    ```
2.  Restart Home Assistant.

## Configuration

1.  In Home Assistant, go to **Settings** > **Devices & Services**.
2.  Click **+ ADD INTEGRATION**.
3.  Search for **Axpert Inverter**.
4.  Enter the **Device Path** (default: `/dev/ttyUSB0`).
5.  Optionally set the **scan interval** (default: 60 seconds).
6.  Click **Submit**.

If connection is successful, the integration will load and entities will become available.

You can change the serial path later from the integration options.

## Usage

### Energy Dashboard Setup
To track your solar production and home usage:
1.  Go to **Energy** section in Settings.
2.  Under **Solar Panels**, add the entity `sensor.axpert_pv_energy`.
3.  Under **Home Usage**, add the entity `sensor.axpert_load_energy`.

### Configuring AC Input (Grid vs Generator)
Use the **AC Input Range** select entity (`select.axpert_ac_input_range`) to configure the input voltage sensitivity:
-   **Appliance (Generator)**: Sets wide input range (90-280V). Use this when running on a generator to prevent rejection of dirty power.
-   **UPS (Grid)**: Sets narrow input range (170-280V). Use this for stable grid power for better protection of sensitive electronics.

## Troubleshooting

-   **Connection Failed**: Verify the serial path exists (`/dev/ttyUSB0` or the path you configured) and Home Assistant has read/write permissions.
-   **Wrong device node**: If `/dev/ttyUSB0` is missing, check `dmesg` / `ls /dev/tty*` and set the actual TTY in the integration options.
-   **Port busy**: Another process (WatchPower, `mppsolar`, a second HA integration) may already hold the serial port.
-   **Entities Unavailable**: Check the logs. If the inverter is off (only battery/solar), USB communication might be down depending on the model.

## Credits

Original project: [ArnyminerZ/ha-axpert-inverter](https://github.com/ArnyminerZ/ha-axpert-inverter) by [Arnau Mora](https://github.com/ArnyminerZ).

This fork keeps that protocol and Home Assistant integration, and changes the transport from USB HID to `pyserial` on `/dev/usbtty0`.
