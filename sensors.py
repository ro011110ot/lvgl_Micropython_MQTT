# sensors.py
import lvgl as lv
from secrets import MQTT_TOPIC_PREFIX


class SensorScreen:
    """
    A screen to display sensor data.
    """

    def __init__(self, mqtt):
        self.mqtt = mqtt
        self.screen = lv.obj()

        self.table = lv.table(self.screen)
        self.table.center()

        self.table.set_column_width(0, 150)
        self.table.set_column_width(1, 80)

        self.table.set_cell_value(0, 0, "Sensor")
        self.table.set_cell_value(0, 1, "Value")

        self.sensors = {
            "temperature": {"row": 1, "value": "N/A"},
            "humidity": {"row": 2, "value": "N/A"},
            "pressure": {"row": 3, "value": "N/A"},
            "light": {"row": 4, "value": "N/A"},
        }

        for name, data in self.sensors.items():
            self.table.set_cell_value(data["row"], 0, name.capitalize())
            self.table.set_cell_value(data["row"], 1, data["value"])

        self.subscribe_to_topics()

    def get_screen(self):
        """
        Returns the screen object.
        """
        return self.screen

    def subscribe_to_topics(self):
        """
        Subscribes to the MQTT topics for the sensors.
        """
        for sensor in self.sensors:
            topic = f"{MQTT_TOPIC_PREFIX}/sensor/{sensor}/state"
            self.mqtt.subscribe(topic, self.handle_sensor_data)

    def handle_sensor_data(self, topic, msg):
        """
        Handles the incoming sensor data from MQTT.
        """
        try:
            sensor = topic.decode().split("/")[-2]
            value = msg.decode()

            if sensor in self.sensors:
                self.sensors[sensor]["value"] = value
                self.table.set_cell_value(self.sensors[sensor]["row"], 1, value)
        except Exception as e:
            print(f"Error handling sensor data: {e}")
