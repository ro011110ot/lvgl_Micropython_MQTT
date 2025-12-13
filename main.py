# main.py
import time
import wifi
import ntp
from mqtt_client import MQTT
import display
import weather
import sensors


def main():
    """
    Main function to initialize and run the application.
    """
    # Connect to WiFi
    wifi.connect()

    # Synchronize time with NTP
    ntp.sync()

    # Start the MQTT client
    mqtt = MQTT()
    mqtt.connect()

    # Start the display
    disp = display.Display()
    disp.add_screen("Weather", weather.WeatherScreen(mqtt))
    disp.add_screen("Sensors", sensors.SensorScreen(mqtt))
    disp.show_screen("Weather")

    while True:
        mqtt.check_msg()
        time.sleep(1)


if __name__ == "__main__":
    main()
