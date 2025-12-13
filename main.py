# main.py
import time
import wifi
import ntp
from mqtt_client import MQTT
import display
import weather
import sensors
from status_led import StatusLed
import lvgl as lv


def main():
    """
    Main function to initialize and run the application.
    """
    led = StatusLed()

    # Connect to WiFi
    wifi.connect()

    # Synchronize time with NTP
    ntp.sync()

    # Start the MQTT client
    led.mqtt_connecting()
    mqtt = MQTT()
    mqtt.connect()
    led.set_color(255, 255, 0)  # Yellow for connected
    time.sleep(1)
    led.off()

    print("=== Initializing Display Screens ===")
    # Start the display manager
    disp = display.Display()
    disp.add_screen("Weather", weather.WeatherScreen(mqtt))
    disp.add_screen("Sensors", sensors.SensorScreen(mqtt))
    disp.show_screen("Weather")

    print("Display initialized and running!")
    print("Hardware timer handles LVGL updates automatically.")
    print("Press Ctrl+C to stop\n")

    # Main loop - Timer läuft automatisch!
    while True:
        mqtt.check_msg()
        time.sleep_ms(100)


if __name__ == "__main__":
    main()