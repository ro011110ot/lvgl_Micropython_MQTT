# sensors.py
import lvgl as lv
import ujson


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

        self.sensors = {}
        self.next_row = 1

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
        self.mqtt.subscribe("Sensor/#", self.handle_sensor_data)

    def handle_sensor_data(self, topic, msg):
        """
        Handles the incoming sensor data from MQTT.
        """
        try:
            sensor_name = topic.decode().split("/")[-1]
            data = ujson.loads(msg)
            value = data.get("value")
            unit = data.get("unit", "")

            if sensor_name not in self.sensors:
                self.sensors[sensor_name] = {"row": self.next_row}
                self.table.set_cell_value(self.next_row, 0, sensor_name)
                self.next_row += 1

            row = self.sensors[sensor_name]["row"]
            self.table.set_cell_value(row, 1, f"{value} {unit}")

        except Exception as e:
            print(f"Error handling sensor data: {e}")
