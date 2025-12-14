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

    # Connect to Wi-Fi
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
    print("Screens will switch automatically every 10 seconds.")
    print("Press Ctrl+C to stop\n")

    # Liste der Screens für automatischen Wechsel
    screen_names = ["Weather", "Sensors"]
    current_screen_index = 0
    screen_switch_counter = 0
    SWITCH_INTERVAL = 100  # 100 * 100ms = 10 Sekunden

    # Main loop - Timer läuft automatisch!
    while True:
        mqtt.check_msg()
        time.sleep_ms(100)

        # Automatischer Screen-Wechsel
        screen_switch_counter += 1
        if screen_switch_counter >= SWITCH_INTERVAL:
            screen_switch_counter = 0
            current_screen_index = (current_screen_index + 1) % len(screen_names)
            next_screen = screen_names[current_screen_index]
            print(f"Switching to {next_screen} screen...")
            disp.show_screen(next_screen)


if __name__ == "__main__":
    main()