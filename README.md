# LVGL Micropython MQTT Project

This project is a MicroPython application for an ESP32 that uses LVGL for the display, connects to a Wi-Fi network, synchronizes the time using NTP, and communicates with an MQTT broker to display sensor data and weather information.

Used Hardware:
  -ESP32-S3 N16R8-DevKitC-1

  -Build & Flash Command for lvgl_micropython (https://github.com/lvgl-micropython/lvgl_micropython)

    python3 make.py esp32 clean BOARD=ESP32_GENERIC_S3 BOARD_VARIANT=SPIRAM_OCT DISPLAY=st7789 --flash-size=16 --partition-size=4194304 --optimize-size CONFIG_SPIRAM_MODE_OCT=y CONFIG_SPIRAM_SPEED_40M=y CONFIG_BOOTLOADER_WDT_TIME_MS=12000 deploy PORT=/dev/ttyACM0
    
    
    
    python3 -m esptool --chip esp32s3 -b 460800 --before default_reset --after hard_reset write_flash --flash_mode dio --flash_size 16MB --flash_freq 80m --erase-all 0x0 /home/ro011110ot/lvgl_micropython/build/lvgl_micropy_ESP32_GENERIC_S3-SPIRAM_OCT-16.bin

## Features

- Wi-Fi connection
- NTP time synchronization
- MQTT client for communication with a broker
- LVGL display with multiple screens:
  - Weather screen (data from OpenWeatherMap)
  - Sensor data screen
  - Last 10 Move Detections

## File Structure

```
.
├── display.py
├── main.py
├── mqtt_client.py
├── ntp.py
├── secrets.py
├── weather.py
└── wifi.py
```

## Setup

1. Create your lvgl Firmware for your ESP32 (https://github.com/lvgl-micropython/lvgl_micropython)

2. **Clone the repository:**
   
   ```bash
   git clone https://github.com/ro011110ot/lvgl_Micropython_MQTT
   ```

3. **Create a `secrets.py` file:**
   
    Create a `secrets.py` file in the root of the project and add your secrets for Wi-Fi, MQTT and OpenWeatherMap.
   
    **Example `secrets.py`:**
   
   ```python
   # This file is not tracked by git.
   # Create a copy of this file and name it secrets.py
   
    # WiFi credentials
    WIFI_SSID = "your_wifi_ssid"
    WIFI_PASSWORD = "your_wifi_password"
   
    # MQTT broker credentials
    MQTT_BROKER = "your_mqtt_broker_ip"
    MQTT_USER = "your_mqtt_user"
    MQTT_PASSWORD = "your_mqtt_password"
    MQTT_CLIENT_ID = "esp32"
    MQTT_TOPIC_PREFIX = "home/livingroom"
   

    # OpenWeatherMap API key
    OPENWEATHERMAP_API_KEY = "your_openweathermap_api_key"
    OPENWEATHERMAP_CITY = "your_city"
    OPENWEATHERMAP_COUNTRY = "your_country_code"

	```
4.  **Upload the files to your ESP32:**
 Use your favorite tool (e.g., `ampy`, `rshell`, `mpremote` `thonny`) to upload all the `.py` files to your ESP32.

## Icon Generation

The project uses 48x48 pixel icons in RGB565 raw binary format (`.bin`) for LVGL. These icons are generated from PNG images using scripts located in the `scripts/` directory.

**Steps to generate icons:**

1.  **Download and Resize PNG Icons:**
 Use `scripts/OpenWeatherMap_Icon_Downloader.py` to fetch OpenWeatherMap icons and resize them to 48x48 pixels. This script will place the resized PNGs in `icons_png/48x48/`.
 ```bash
 python3 scripts/OpenWeatherMap_Icon_Downloader.py
 ```
 *Note: For `wifi_on.png` and `wifi_off.png`, you might need to provide your own PNG files in the `icons_png/original/` directory if the script creates dummy placeholders.*

2.  **Convert PNGs to LVGL Binary Format:**
 Once you have the 48x48 PNG icons, use `scripts/convert_icons.py` to convert them into LVGL-compatible `.bin` files. This script reads from `icons_png/` (specifically `icons_png/48x48/` if the downloader was run) and outputs the `.bin` files to the `icons/` directory.
 ```bash
 python3 scripts/convert_icons.py
 ```

3.  **Upload to ESP32:**
 Copy the generated `.bin` files from the local `icons/` directory to the `/icons` directory on your ESP32.

## Usage

The `main.py` file is the entry point of the application. It will automatically run when the ESP32 boots up.

```python
# main.py
import time
import wifi
import ntp
import mqtt_client
import display

def main():
 """
 Main function to initialize and run the application.
 """
 # Connect to Wi-Fi
 wifi.connect()

 # Synchronize time with NTP
 ntp.sync()

 # Start the MQTT client
 mqtt = mqtt_client.MQTT()
 mqtt.connect()

 # Start the display
 disp = display.Display()
 disp.add_screen("Weather", weather.WeatherScreen)
 disp.add_screen("Sensors", sensors.SensorScreen)
 disp.show_screen("Weather")


 while True:
     mqtt.check_msg()
     time.sleep(1)

if __name__ == "__main__":
 main()
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
