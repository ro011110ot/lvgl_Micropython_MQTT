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
    time.sleep(3)
    led.off()

    # Start the display
    # disp = display.Display()
    # disp.add_screen("Weather", weather.WeatherScreen(mqtt))
    # disp.add_screen("Sensors", sensors.SensorScreen(mqtt))
    # disp.show_screen("Weather")

    # Create a simple test screen directly on the active screen
    scrn = lv.screen_active()
    label = lv.label(scrn)
    label.set_text("Hello World!")
    label.center()

    while True:
        lv.tick_inc(5)
        lv.task_handler()
        mqtt.check_msg()
        time.sleep_ms(5)


if __name__ == "__main__":
    main()
