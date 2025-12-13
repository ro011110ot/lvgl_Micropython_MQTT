# status_led.py
from machine import Pin
from neopixel import NeoPixel
import time


class StatusLed:
    """
    A class to control a NeoPixel status LED.
    """

    def __init__(self, pin_number=48, num_pixels=1):
        self.pin = Pin(pin_number, Pin.OUT)
        self.np = NeoPixel(self.pin, num_pixels)
        self.off()

    def set_color(self, r, g, b):
        """
        Sets the color of the LED.
        """
        self.np[0] = (r, g, b)
        self.np.write()

    def off(self):
        """
        Turns the LED off.
        """
        self.set_color(0, 0, 0)

    def blink(self, color, duration=0.5, num_blinks=1):
        """
        Blinks the LED with a given color.
        """
        for _ in range(num_blinks):
            self.set_color(*color)
            time.sleep(duration)
            self.off()
            time.sleep(duration)

    def wifi_connecting(self):
        """
        Blinks green to indicate WiFi is connecting.
        """
        self.blink((0, 255, 0))

    def mqtt_connecting(self):
        """
        Blinks yellow to indicate MQTT is connecting.
        """
        self.blink((255, 255, 0))
