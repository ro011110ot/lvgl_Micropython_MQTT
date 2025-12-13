import network
import time
from secrets import WIFI_SSID, WIFI_PASSWORD


def connect():
    """
    Connects the device to the Wi-Fi network using credentials from secrets.py.
    """
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print(f"Connecting to network {WIFI_SSID}...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        max_wait = 10
        while max_wait > 0:
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            max_wait -= 1
            print("Waiting for connection...")
            time.sleep(1)

    if wlan.status() != 3:
        raise RuntimeError("Network connection failed")
    else:
        print("Connected")
        status = wlan.ifconfig()
        print(f"ip = {status[0]}")
