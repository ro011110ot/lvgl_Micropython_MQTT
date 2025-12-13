import network
import time
from status_led import StatusLed
from secrets import WIFI_CREDENTIALS


def connect():
    """
    Connects the device to the Wi-Fi network using credentials from secrets.py.
    It tries each network in the 'WIFI_CREDENTIALS' list until a connection is established.
    """
    led = StatusLed()
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    for creds in WIFI_CREDENTIALS:
        wlan.disconnect()
        time.sleep(1)  # Give time to disconnect

        ssid = creds.get("ssid")
        password = creds.get("password")

        print(f"Connecting to network {ssid}...")
        wlan.connect(ssid, password)

        max_wait = 10
        while max_wait > 0:
            led.wifi_connecting()
            if wlan.isconnected():
                break
            max_wait -= 1
            print("Waiting for connection...")
            time.sleep(1)

        if wlan.isconnected():
            print("Connected")
            status = wlan.ifconfig()
            print(f"ip = {status[0]}")
            led.set_color(0, 255, 0)  # Green for connected
            return

    if not wlan.isconnected():
        led.set_color(255, 0, 0)  # Red for error
        raise RuntimeError("Network connection failed")
