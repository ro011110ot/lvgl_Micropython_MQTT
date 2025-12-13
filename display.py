# display.py
import lvgl as lv
import st7789
import lcd_bus
import machine
from micropython import const

_WIDTH = const(240)
_HEIGHT = const(320)

# SPI Bus Pins
SPI_HOST = 1
MOSI = 11
MISO = None
SCK = 12

# Display Control Pins
CS = 10
DC = 9
RST = 14

_FREQ = const(40_000_000)


class Display:
    """
    Manages the display and screens.
    """

    def __init__(self):
        self.spi_bus = machine.SPI(
            SPI_HOST,
            mosi=machine.Pin(MOSI),
            miso=machine.Pin(MISO) if MISO is not None else None,
            sck=machine.Pin(SCK),
        )

        self.display_bus = lcd_bus.SPIBus(
            spi_bus=self.spi_bus,
            freq=_FREQ,
            dc=machine.Pin(DC),
            cs=machine.Pin(CS),
        )
        self.display = st7789.ST7789(
            data_bus=self.display_bus,
            display_width=_WIDTH,
            display_height=_HEIGHT,
            reset_pin=machine.Pin(RST, machine.Pin.OUT),
            reset_state=st7789.STATE_LOW,
            backlight_pin=None,
            color_space=lv.COLOR_FORMAT.RGB565,
            color_byte_order=st7789.BYTE_ORDER_BGR,
            rgb565_byte_swap=True,
        )
        self.display.init()
        self.display.set_backlight(100)

        self.screens = {}
        self.current_screen = None

    def add_screen(self, name, screen_instance):
        """
        Adds a screen to the manager.
        """
        self.screens[name] = screen_instance

    def show_screen(self, name):
        """
        Shows the specified screen.
        """
        if name in self.screens:
            screen = self.screens[name].get_screen()
            lv.screen_load(screen)
            self.current_screen = screen
