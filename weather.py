# weather.py
import lvgl as lv
import urequests
import json
import time
from secrets import OPENWEATHERMAP_API_KEY, OPENWEATHERMAP_CITY, OPENWEATHERMAP_COUNTRY
from timer import Timer


class WeatherScreen:
    """
    A screen to display weather information with time and date.
    """

    def __init__(self, mqtt):
        self.mqtt = mqtt
        self.screen = lv.obj()

        # Titel
        self.title_label = lv.label(self.screen)
        self.title_label.set_text("Wetter")
        self.title_label.align(lv.ALIGN.TOP_MID, 0, 10)

        # Uhrzeit & Datum (groß)
        self.time_label = lv.label(self.screen)
        self.time_label.set_text("--:--")
        self.time_label.align(lv.ALIGN.TOP_MID, 0, 35)

        self.date_label = lv.label(self.screen)
        self.date_label.set_text("-- --- ----")
        self.date_label.align(lv.ALIGN.TOP_MID, 0, 65)

        # Wetter-Beschreibung
        self.weather_label = lv.label(self.screen)
        self.weather_label.set_text("Wetter: ...")
        self.weather_label.align(lv.ALIGN.CENTER, 0, -40)

        # Temperatur (groß)
        self.temperature_label = lv.label(self.screen)
        self.temperature_label.set_text("-- °C")
        self.temperature_label.align(lv.ALIGN.CENTER, 0, -10)

        # Gefühlte Temperatur
        self.feels_like_label = lv.label(self.screen)
        self.feels_like_label.set_text("Gefuehlt: -- °C")
        self.feels_like_label.align(lv.ALIGN.CENTER, 0, 15)

        # Luftfeuchtigkeit
        self.humidity_label = lv.label(self.screen)
        self.humidity_label.set_text("Luftfeuchte: -- %")
        self.humidity_label.align(lv.ALIGN.CENTER, 0, 40)

        # Luftdruck
        self.pressure_label = lv.label(self.screen)
        self.pressure_label.set_text("Luftdruck: ---- hPa")
        self.pressure_label.align(lv.ALIGN.CENTER, 0, 65)

        # Wind
        self.wind_label = lv.label(self.screen)
        self.wind_label.set_text("Wind: -- km/h")
        self.wind_label.align(lv.ALIGN.CENTER, 0, 90)

        # Aktualisiere Zeit und Wetter
        self.update_time()
        self.update_weather()

        # Timer für Zeitaktualisierung (jede Sekunde)
        self.time_timer = Timer(self.update_time, 1000)

        # Timer für Wetteraktualisierung (alle 10 Minuten)
        self.weather_timer = Timer(self.update_weather, 600000)

    def get_screen(self):
        """
        Returns the screen object.
        """
        return self.screen

    def _replace_umlauts(self, text):
        """
        Replace German umlauts with ASCII equivalents.
        """
        replacements = {
            'ä': 'ae', 'Ä': 'Ae',
            'ö': 'oe', 'Ö': 'Oe',
            'ü': 'ue', 'Ü': 'Ue',
            'ß': 'ss'
        }
        for umlaut, replacement in replacements.items():
            text = text.replace(umlaut, replacement)
        return text

    def update_time(self, timer=None):
        """
        Updates the time and date display.
        """
        try:
            current_time = time.localtime()
            # Format: HH:MM:SS
            time_str = "{:02d}:{:02d}:{:02d}".format(
                current_time[3], current_time[4], current_time[5]
            )
            # Format: DD Mon YYYY
            months = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun",
                      "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]
            date_str = "{:02d} {} {}".format(
                current_time[2], months[current_time[1] - 1], current_time[0]
            )

            self.time_label.set_text(time_str)
            self.date_label.set_text(date_str)
        except Exception as e:
            print(f"Error updating time: {e}")

    def update_weather(self, timer=None):
        """
        Fetches and displays the current weather.
        """
        # Verwende 'lang=en' statt 'lang=de' für englische Texte (keine Umlaute)
        url = f"http://api.openweathermap.org/data/2.5/weather?q={OPENWEATHERMAP_CITY},{OPENWEATHERMAP_COUNTRY}&appid={OPENWEATHERMAP_API_KEY}&units=metric&lang=de"
        try:
            print("Fetching weather data...")
            response = urequests.get(url)
            data = json.loads(response.text)
            response.close()

            if data and "main" in data and "weather" in data:
                # Wetter-Beschreibung
                weather_desc = data["weather"][0]["description"]
                # Kapitalisiere den ersten Buchstaben
                if weather_desc:
                    weather_desc = weather_desc[0].upper() + weather_desc[1:]
                # Ersetze Umlaute für bessere Darstellung
                weather_desc = self._replace_umlauts(weather_desc)
                self.weather_label.set_text(f"{weather_desc}")

                # Temperatur
                temp = data["main"]["temp"]
                self.temperature_label.set_text(f"{temp:.1f} °C")

                # Gefühlte Temperatur
                feels_like = data["main"]["feels_like"]
                self.feels_like_label.set_text(f"Gefühlt: {feels_like:.1f} °C")

                # Luftfeuchtigkeit
                humidity = data["main"]["humidity"]
                self.humidity_label.set_text(f"Luftfeuchte: {humidity} %")

                # Luftdruck
                pressure = data["main"]["pressure"]
                self.pressure_label.set_text(f"Luftdruck: {pressure} hPa")

                # Wind
                wind_speed = data["wind"]["speed"] * 3.6  # m/s zu km/h
                self.wind_label.set_text(f"Wind: {wind_speed:.1f} km/h")

                print("Weather data updated successfully")
            else:
                self.weather_label.set_text("Wetter: N/A")
                print("Invalid weather data received")

        except Exception as e:
            print(f"Error fetching weather: {e}")
            self.weather_label.set_text("Wetter: Fehler")