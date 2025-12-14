# weather.py
import lvgl as lv
import urequests
import json
import time
from secrets import OPENWEATHERMAP_API_KEY, OPENWEATHERMAP_CITY, OPENWEATHERMAP_COUNTRY
from timer import Timer


class WeatherScreen:
    """
    A screen to display weather information with time, date and icons.
    """

    def __init__(self, mqtt):
        """
        Initializes the WeatherScreen.

        Args:
            mqtt: The MQTT client instance for communication.
        """
        self.mqtt = mqtt
        self.screen = lv.obj()

        # Title
        self.title_label = lv.label(self.screen)
        self.title_label.set_text("Wetter")
        self.title_label.align(lv.ALIGN.TOP_MID, 0, 5)

        # Time & Date
        self.time_label = lv.label(self.screen)
        self.time_label.set_text("--:--:--")
        self.time_label.align(lv.ALIGN.TOP_MID, 0, 25)

        self.date_label = lv.label(self.screen)
        self.date_label.set_text("-- --- ----")
        self.date_label.align(lv.ALIGN.TOP_MID, 0, 45)

        # Weather Icon (48x48 Pixel)
        self.weather_icon = lv.img(self.screen)
        # Weather Description
        self.weather_label = lv.label(self.screen)
        self.weather_label.set_text("...")
        self.weather_label.align(lv.ALIGN.CENTER, 0, 0)

        # Temperature (large)
        self.temperature_label = lv.label(self.screen)
        self.temperature_label.set_text("-- C")
        self.temperature_label.align(lv.ALIGN.CENTER, 0, 25)

        # Feels Like Temperature
        self.feels_like_label = lv.label(self.screen)
        self.feels_like_label.set_text("Feels like: -- C")
        self.feels_like_label.align(lv.ALIGN.CENTER, 0, 45)

        # Humidity & Pressure (side-by-side)
        self.humidity_label = lv.label(self.screen)
        self.humidity_label.set_text("-- %")
        self.humidity_label.align(lv.ALIGN.BOTTOM_LEFT, 10, -30)

        self.pressure_label = lv.label(self.screen)
        self.pressure_label.set_text("---- hPa")
        self.pressure_label.align(lv.ALIGN.BOTTOM_RIGHT, -10, -30)

        # Wind
        self.wind_label = lv.label(self.screen)
        self.wind_label.set_text("Wind: -- km/h")
        self.wind_label.align(lv.ALIGN.BOTTOM_MID, 0, -10)

        # Icon Cache
        self.icon_cache = {}
        self.current_icon_code = None

        # Update time and weather
        self.update_time()
        self.update_weather()

        # Timer for time update (every second)
        self.time_timer = Timer(self.update_time, 1000)

        # Timer for weather update (every 10 minutes)
        self.weather_timer = Timer(self.update_weather, 600000)

    def get_screen(self):
        """
        Returns the screen object.
        """
        return self.screen

    @staticmethod
    def _replace_umlauts(text):
        """
        Replace German umlauts with ASCII equivalents.
        """
        replacements = {
            'ä': 'ae', 'Ä': 'Ae',
            'ö': 'oe', 'Ö': 'Oe',
            'ü': 'ue', 'Ü': 'Ue',
            'ß': 'ss',
            '°': ''  # Grad-Zeichen entfernen
        }
        for umlaut, replacement in replacements.items():
            text = text.replace(umlaut, replacement)
        return text

    def _load_weather_icon(self, icon_code):
        """
        Load weather icon from file system.
        Icon codes: 01d, 01n, 02d, 02n, etc.
        Icons should be 48x48 RGB565 raw binary files.
        """
        if not icon_code:
            return None

        # Use cache
        if icon_code in self.icon_cache:
            return self.icon_cache[icon_code]

        icon_path = f"icons/{icon_code}.bin"
        try:
            # Load icon file as raw RGB565 data
            with open(icon_path, 'rb') as f:
                icon_data = f.read()



            # Create LVGL Image Descriptor for RGB565 Raw
            img_dsc = lv.img_dsc_t({
                'header': {
                    'always_zero': 0,
                    'w': 48,
                    'h': 48,
                    'cf': lv.img.CF.TRUE_COLOR,
                },
                'data': icon_data,
                'data_size': len(icon_data),
            })

            # Cache the icon
            self.icon_cache[icon_code] = img_dsc
            print(f"Loaded weather icon: {icon_code} ({len(icon_data)} bytes)")
            return img_dsc

        except Exception as e:
            print(f"Error loading icon {icon_code}: {e}")
            return None

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
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                      "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            date_str = "{:02d} {} {}".format(
                current_time[2], months[current_time[1] - 1], current_time[0]
            )

            self.time_label.set_text(time_str)
            self.date_label.set_text(date_str)
        except Exception as e:
            print(f"Error updating time: {e}")

    def update_weather(self, timer=None):
        """
        Fetches and displays the current weather with icon.
        """
        url = f"http://api.openweathermap.org/data/2.5/weather?q={OPENWEATHERMAP_CITY},{OPENWEATHERMAP_COUNTRY}&appid={OPENWEATHERMAP_API_KEY}&units=metric&lang=en"
        try:
            print("Fetching weather data...")
            response = urequests.get(url)
            data = json.loads(response.text)
            response.close()

            if data and "main" in data and "weather" in data:
                # Weather Icon
                icon_code = data["weather"][0]["icon"]
                if icon_code != self.current_icon_code:
                    icon_dsc = self._load_weather_icon(icon_code)
                    if icon_dsc:
                        self.weather_icon.set_src(icon_dsc)
                        self.current_icon_code = icon_code

                # Weather Description
                weather_desc = data["weather"][0]["description"]
                if weather_desc:
                    weather_desc = weather_desc[0].upper() + weather_desc[1:]
                weather_desc = self._replace_umlauts(weather_desc)
                self.weather_label.set_text(f"{weather_desc}")

                # Temperature
                temp = data["main"]["temp"]
                self.temperature_label.set_text(f"{temp:.1f} C")

                # Feels Like Temperature
                feels_like = data["main"]["feels_like"]
                self.feels_like_label.set_text(f"Feels like: {feels_like:.1f} C")

                # Humidity
                humidity = data["main"]["humidity"]
                self.humidity_label.set_text(f"{humidity}%")

                # Pressure
                pressure = data["main"]["pressure"]
                self.pressure_label.set_text(f"{pressure} hPa")

                # Wind
                wind_speed = data["wind"]["speed"] * 3.6  # m/s to km/h
                self.wind_label.set_text(f"Wind: {wind_speed:.1f} km/h")

                print("Weather data updated successfully")
            else:
                self.weather_label.set_text("N/A")
                print("Invalid weather data received")

        except Exception as e:
            print(f"Error fetching weather: {e}")
            self.weather_label.set_text("Error")