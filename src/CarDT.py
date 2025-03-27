import paho.mqtt.client as mqtt
import random
import time
import json

# Digital twin info
namespace = "example"
car_name = "mycar"
wheels_name = "mycar:wheel_"

# MQTT info
broker = "37.156.47.96"  # MQTT broker address
port = 30511  # MQTT port
topic = "telemetry/"  # Topic where data will be published


# MQTT connection
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successful connection")
    else:
        print(f"Connection failed with code {rc}")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
#client.username_pw_set(username, password)
#client.username_pw_set('')
client.connect(broker, port, 60)


# Data generator
def generate_wheel_data():
    velocity = random.uniform(0, 100)  # Generate random velocity (between 0 and 100 km/h)
    direction = random.uniform(-45, 45)  # Generate random direction (between -45 and 45 degrees)
    return velocity, direction


def generate_gps_data():
    latitude = random.uniform(-90.0, 90.0)
    longitude = random.uniform(-180.0, 180.0)
    return latitude, longitude


# Ditto Protocol
def get_ditto_protocol_value_car(time, latitude, longitude):
    return {
        "gps": {
            "properties": {
                "latitude": latitude,
                "longitude": longitude,
                "time": time
            }
        }
    }


def get_ditto_protocol_value_wheel(time, velocity, direction):
    return {
        "velocity": {
            "properties": {
                "value": velocity,
                "time": time
            }
        },
        "direction": {
            "properties": {
                "value": direction,
                "time": time
            }
        }
    }


def get_ditto_protocol_msg(name, value):
    return {
        "topic": "{}/{}/things/twin/commands/merge".format(namespace, name),
        "headers": {
            "content-type": "application/merge-patch+json"
        },
        "path": "/features",
        "value": value
    }


# Send data
try:
    while True:
        t = round(time.time() * 1000)  # Unix ms

        # Car twin
        latitude, longitude = generate_gps_data()
        test = get_ditto_protocol_value_car(t, latitude, longitude)
        msg = get_ditto_protocol_msg(car_name, get_ditto_protocol_value_car(t, latitude, longitude))
        client.publish(topic + namespace + "/" + car_name, json.dumps(msg))
        print(car_name + " data published")

        # Wheels twins
        for i in range(1, 5):
            name = wheels_name + str(i)
            velocity, direction = generate_wheel_data()
            msg = get_ditto_protocol_msg(name, get_ditto_protocol_value_wheel(t, velocity, direction))
            client.publish(topic + namespace + "/" + name, json.dumps(msg))
            print(name + " data published")

        time.sleep(60)

except KeyboardInterrupt:
    client.disconnect()