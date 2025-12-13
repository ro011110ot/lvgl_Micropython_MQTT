import lcd_bus
import machine


# SPI Bus Pins
SPI_HOST = 1
MOSI = 11
MISO = None
SCK = 12

# Display Control Pins
CS = 10
DC = 9
RST = 14

from micropython import const
import machine

_WIDTH = const(240)
_HEIGHT = const(320)

import lcd_bus

# Tried host 1 and 2; w/hard resets in between
_HOST = const(1)
_MOSI_PIN = const(11)
_MISO_PIN = const(-1)  # Not connected
_SCLK_PIN = const(12)

_DC_PIN = const(9)
_CS_PIN = const(10)
_RESET_PIN = const(14)
_POWER_PIN = const(None)
_BACKLIGHT_PIN = const(None)

_FREQ = const(40_000_000)

_WP_PIN = const(None)
_HD_PIN = const(None)

spi_bus = machine.SPI.Bus(
    host=_HOST,
    mosi=_MOSI_PIN,
    miso=_MISO_PIN,
    sck=_SCLK_PIN,
)

display_bus = lcd_bus.SPIBus(
    spi_bus=spi_bus,
    freq=_FREQ,
    dc=_DC_PIN,
    cs=_CS_PIN,
)

import st7789  # NOQA
import lvgl as lv  # NOQA

display = st7789.ST7789(
    data_bus=display_bus,
    display_width=_WIDTH,
    display_height=_HEIGHT,
    reset_pin=_RESET_PIN,
    reset_state=st7789.STATE_LOW,  # <-----
    backlight_pin=_BACKLIGHT_PIN,
    color_space=lv.COLOR_FORMAT.RGB565,
    color_byte_order=st7789.BYTE_ORDER_BGR,
    rgb565_byte_swap=True,
)

display.init()

display.set_backlight(100)

import task_handler

th = task_handler.TaskHandler()

scrn = lv.screen_active()

# Nehmen wir an, 'scrn' ist Ihr aktiver Bildschirm:
# scrn = lv.screen_active()

# 1. Tabelle erstellen
table = lv.table(scrn)
table.center()  # Tabelle in der Mitte des Bildschirms platzieren

# 2. Spaltenbreiten festlegen
# Spalte 0 (Name Sensor): 150 Pixel breit
# Spalte 1 (Wert des Sensors): 80 Pixel breit
table.set_column_width(0, 150)
table.set_column_width(1, 80)

# 3. Kopfzeile (Überschrift) festlegen
# Zeile 0: Überschrift
ROW_HEADER = 0
table.set_cell_value(ROW_HEADER, 0, "Sensor")
table.set_cell_value(ROW_HEADER, 1, "Wert")
ROW_TEMP = 1
ROW_HUMIDITY = 2
ROW_PRESSURE = 3
ROW_LIGHT = 4
# Styling für die Kopfzeile (Hervorhebung)
# Setzt den Stil für alle Zellen in Zeile 0 auf den HEADER-Modus
# Korrigierte Methode: Setzt das Header-Flag für jede Zelle in der Kopfzeile
ROW_HEADER = 0


# Testen Sie zuerst, ob die Konstante im lv-Objekt selbst liegt (häufig in v8-Bindings)
try:
    # Versucht, die Konstante zu finden (der korrekte Name kann variieren)
    HEADER_FLAG = lv.TABLE_CELL_CTRL_HEADER

except AttributeError:
    # Wenn der Name nicht gefunden wird, verwenden Sie den numerischen Wert (häufig 2)
    # Dies ist der sicherste Weg, wenn der Name nicht erkannt wird.
    HEADER_FLAG = 2

# Setzen der Header-Steuerung mit der gefundenen/definierten Konstante
table.set_cell_ctrl(ROW_HEADER, 0, HEADER_FLAG)
table.set_cell_ctrl(ROW_HEADER, 1, HEADER_FLAG)

# Weiterhin gültige Zeilen ab hier:
# ...
table.set_cell_value(ROW_TEMP, 0, "Temperatur")
# ...

# 4. Sensor-Daten hinzufügen
# Die Zählung beginnt ab Zeile 1


# Sensor-Namen (linke Spalte)
table.set_cell_value(ROW_TEMP, 0, "Temperatur")
table.set_cell_value(ROW_HUMIDITY, 0, "Luftfeuchte")
table.set_cell_value(ROW_PRESSURE, 0, "Luftdruck")
table.set_cell_value(ROW_LIGHT, 0, "Helligkeit")

# Sensor-Werte (rechte Spalte - Platzhalter)
table.set_cell_value(ROW_TEMP, 1, "23.5 °C")
table.set_cell_value(ROW_HUMIDITY, 1, "45 %")
table.set_cell_value(ROW_PRESSURE, 1, "1012 hPa")
table.set_cell_value(ROW_LIGHT, 1, "850 lux")

# Optional: Setzen Sie alle Zellen in der Wert-Spalte rechtsbündig
for row in range(ROW_TEMP, ROW_LIGHT + 1):
    # Setzt den Text der Zelle in Spalte 1 rechtsbündig aus
    table.set_cell_align(row, 1, lv.ALIGN.RIGHT)


# --- WICHTIG: Live-Update der Daten ---

# Um die Sensordaten dynamisch zu aktualisieren,
# müssen Sie diese Funktion z.B. alle 1000ms über einen LVGL-Timer aufrufen.


def update_sensor_data(timer):
    # Simulieren neuer Messwerte
    import random

    new_temp = random.uniform(20.0, 30.0)
    new_humidity = random.randint(30, 60)

    # Werte in die Tabelle schreiben
    table.set_cell_value(ROW_TEMP, 1, f"{new_temp:.1f} °C")
    table.set_cell_value(ROW_HUMIDITY, 1, f"{new_humidity} %")


# Beispiel, wie Sie den Timer starten würden (abhängig von Ihrer task_handler Implementierung):
# lv.timer_create(update_sensor_data, 1000, None)
