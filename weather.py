# weather.py
import lvgl as lv
import urequests
import json
from secrets import OPENWEATHERMAP_API_KEY, OPENWEATHERMAP_CITY, OPENWEATHERMAP_COUNTRY
from timer import Timer


class WeatherScreen:
    """
    A screen to display weather information.
    """

    def __init__(self, mqtt):
        self.mqtt = mqtt
        self.screen = lv.obj()
        self.label = lv.label(self.screen)
        self.label.align(lv.ALIGN.CENTER, 0, -20)
        self.temperature_label = lv.label(self.screen)
        self.temperature_label.align(lv.ALIGN.CENTER, 0, 20)

        self.update_weather()
        self.timer = Timer(self.update_weather, 1800000)  # 30 minutes

    def get_screen(self):
        """
        Returns the screen object.
        """
        return self.screen

    def update_weather(self, timer=None):
        """
        Fetches and displays the current weather.
        """
        url = f"http://api.openweathermap.org/data/2.5/weather?q={OPENWEATHERMAP_CITY},{OPENWEATHERMAP_COUNTRY}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
        try:
            response = urequests.get(url)
            data = json.loads(response.text)
            response.close()

            if data and "main" in data and "weather" in data:
                weather_description = data["weather"][0]["description"]
                temperature = data["main"]["temp"]
                self.label.set_text(f"Weather: {weather_description}")
                self.temperature_label.set_text(f"Temperature: {temperature}°C")
            else:
                self.label.set_text("Weather: N/A")
                self.temperature_label.set_text("Temperature: N/A")

        except Exception as e:
            print(f"Error fetching weather: {e}")
            self.label.set_text("Weather: Error")
            self.temperature_label.set_text("Temperature: Error")
