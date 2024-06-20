import sys
import os
import datetime
import base64

import paho.mqtt.client as paho

import numpy as np
import cv2

client = paho.Client(paho.CallbackAPIVersion.VERSION2)


def message_handling(client, userdata, msg):
    timestamp = datetime.datetime.now()
    image_name = f'./images/esp32cam-{timestamp.strftime('%Y-%m-%d_%H-%M-%S')}.jpeg'
    with open(image_name, "wb") as f:
        print(bytes(msg.payload))
        f.write(base64.decodebytes(msg.payload))

    print("Image received")
    client.publish("imagem/response_send_image", "Imagem recebida")

# Tons de cinza
def on_message(client, userdata, msg):
    try:
        timestamp = datetime.datetime.now()

        filename = os.path.basename(f'./images/teste/esp32cam-{timestamp.strftime('%Y-%m-%d_%H-%M-%S')}.jpg')

        img_array = np.frombuffer(msg.payload, dtype=np.uint8)

        img = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)

        cv2.imwrite(os.path.join("images", filename), img)

        print("Image received")
    except Exception as e:
        print(f"Error receiving image: {e}")


client.on_message = message_handling

if client.connect("localhost", 1883, 60) != 0:
    print("Couldn't connect to the mqtt broker")
    sys.exit(1)

client.subscribe("imagem/send_image")

try:
    print("Press CTRL+C to exit...")
    client.loop_forever()
except Exception:
    print("Caught an Exception, something went wrong...")
finally:
    print("Disconnecting from the MQTT broker")
    client.disconnect()

