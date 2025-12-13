# LVGL Micropython MQTT Project

This project is a MicroPython application for an ESP32 that uses LVGL for the display, connects to a WiFi network, synchronizes the time using NTP, and communicates with an MQTT broker to display sensor data and weather information.

## Features

- WiFi connection
- NTP time synchronization
- MQTT client for communication with a broker
- LVGL display with multiple screens:
  - Weather screen (data from OpenWeatherMap)
  - Sensor data screen

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

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    ```
2.  **Create a `secrets.py` file:**
    Create a `secrets.py` file in the root of the project and add your secrets for WiFi, MQTT and OpenWeatherMap.

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
3.  **Upload the files to your ESP32:**
    Use your favorite tool (e.g., `ampy`, `rshell`, `thonny`) to upload all the `.py` files to your ESP32.

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
    # Connect to WiFi
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
