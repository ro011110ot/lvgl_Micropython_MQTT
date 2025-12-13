from umqtt.simple import MQTTClient
from secrets import MQTT_BROKER, MQTT_USER, MQTT_PASSWORD, MQTT_PORT, MQTT_SSL
import machine
import ubinascii


class MQTT:
    """
    A wrapper class for the umqtt.simple.MQTTClient.
    Handles connection, subscription, and publishing.
    """

    def __init__(
        self,
        client_id=ubinascii.hexlify(machine.unique_id()),
        broker=MQTT_BROKER,
        port=MQTT_PORT,
        user=MQTT_USER,
        password=MQTT_PASSWORD,
        ssl=MQTT_SSL,
    ):
        """
        Initializes the MQTT client.
        """
        self.client_id = client_id
        self.broker = broker
        self.port = port
        self.user = user
        self.password = password
        self.ssl = ssl
        self.client = MQTTClient(
            self.client_id,
            self.broker,
            port=self.port,
            user=self.user,
            password=self.password,
            ssl=self.ssl,
        )
        self.is_connected = False
        self.subscriptions = {}

    def connect(self):
        """
        Connects to the MQTT broker.
        """
        if not self.is_connected:
            print(f"Connecting to MQTT broker at {self.broker}...")
            try:
                self.client.set_callback(self.on_message)
                self.client.connect()
                self.is_connected = True
                print("MQTT connected successfully.")
                for topic in self.subscriptions:
                    self.client.subscribe(topic)
            except OSError as e:
                print(f"Failed to connect to MQTT broker: {e}")
                self.is_connected = False

    def disconnect(self):
        """
        Disconnects from the MQTT broker.
        """
        if self.is_connected:
            print("Disconnecting from MQTT broker.")
            self.client.disconnect()
            self.is_connected = False

    def publish(self, topic, msg):
        """
        Publishes a message to a specific MQTT topic.
        """
        if self.is_connected:
            self.client.publish(topic, msg)

    def subscribe(self, topic, callback):
        """
        Subscribes to a topic and registers a callback.
        """
        self.subscriptions[topic] = callback
        if self.is_connected:
            self.client.subscribe(topic)

    def on_message(self, topic, msg):
        """
        Callback for incoming messages.
        """
        if topic in self.subscriptions:
            self.subscriptions[topic](topic, msg)

    def check_msg(self):
        """
        Checks for incoming messages.
        """
        if self.is_connected:
            self.client.check_msg()
