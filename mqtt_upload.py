import paho.mqtt.client as mqtt
import time
# MQTT broker settings
broker_address = "broker.hivemq.com"
broker_port = 1883

def publish_to_mqtt(topic, data):
    # Create an MQTT client instance
    client = mqtt.Client()

    # Connect to the broker
    client.connect(broker_address, broker_port, 60)
    print(f"Connected to MQTT broker and send {data} ")
    # Publish the data to the specified topic
    client.publish(topic, data, qos=1)

    client.loop_start()

        # Allow time for the message to be published
    time.sleep(1)

        # Disconnect from the broker
    client.loop_stop()
    # Disconnect from the broker
    
