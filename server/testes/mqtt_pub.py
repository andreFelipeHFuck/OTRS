import sys
from time import sleep


import paho.mqtt.client as mqtt

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

if client.connect("localhost", 1883, 60) != 0:
    print("Couldn't connect to the mqtt broker")
    sys.exist(1)

print("Iniciando operação:")
#while True:
#    sleep(30)
print("Mensagem enviada")
client.publish("imagem/request_image", "Ligar!", 0)
client.disconnect()