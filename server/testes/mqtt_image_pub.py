import sys

import paho.mqtt.client as mqtt

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

#client.username_pw_set("esp32cam", "$7$101$ETJ0TXYN5KloG92j$uFPozzTWOJa2WkGJOB5zn7eHsLIs1XQ1ilnC442iRVzF6+DbuKSRNzHf5/uf7mKS1ZBYz5tKlx49PraiIKzFmQ==")

if client.connect("localhost", 1883, 60) != 0:
    print("Couldn't connect to the mqtt broker")
    sys.exist(1)


with open("./image_test.png", "rb") as file:
    filecontent = file.read()
    byteArray = bytearray(filecontent)
    print(bytes(byteArray))
    client.publish("imagem/send_image", bytes(byteArray), 0)
    
    client.disconnect()