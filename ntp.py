import ntptime
import time
from machine import RTC


def sync():
    """
    Synchronizes the device's real-time clock (RTC) with an NTP server (UTC).
    Retries a few times if it fails.
    """
    print("Synchronizing RTC with NTP server (UTC)...")
    rtc = RTC()
    max_retries = 3
    for attempt in range(max_retries):
        try:
            ntptime.settime()
            if rtc.datetime()[0] > 2021:
                print("Time synchronized successfully to UTC.")
                return
        except Exception as e:
            print(
                f"Error synchronizing time (attempt {attempt + 1}/{max_retries}): {e}"
            )
            time.sleep(5)
    raise RuntimeError("Failed to synchronize time.")
