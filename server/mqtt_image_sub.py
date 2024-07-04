import sys
import os
import datetime
import base64
import paho.mqtt.client as paho
import numpy as np
import cv2
import logging

from image_process import process_image_manometro, process_image_digital
from telegram_notify import send_to_contacts

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Defina a mensagem a ser enviada
default_msg = "Aviso: O nível de gás supervisionado pelo ESP32 está baixo!"

client = paho.Client(paho.CallbackAPIVersion.VERSION2)

modo = 'manometro'


def message_handling(client, userdata, msg):
    timestamp = datetime.datetime.now()
    image_path = f'./images/esp32cam-{timestamp.strftime('%Y-%m-%d_%H-%M-%S')}.jpeg'
    with open(image_path, "wb") as f:
        logger.info(bytes(msg.payload))
        f.write(base64.decodebytes(msg.payload))

    logger.info("Image received")
    client.publish("imagem/response_send_image", "Imagem recebida")

    logger.info("Sending image to process_image...")

    if modo == 'manometro':
        # percs_quads = process_image_manometro(image_path)
        percs_quads = process_image_manometro('./images/teste_alg/teste_manometro.jpg')

        if percs_quads[1] > 30:
            logger.info(
                "Nível de gás baixo detectado pelo manômetro. Enviando notificação..."
            )
            send_to_contacts(default_msg)
            logger.info("Notificação enviada com sucesso.")
        else:
            logger.info("Nível de gás normal. Aguardar próxima verificação.")

    else:
        # percs = process_image_manometro(image_path)
        perc = process_image_digital("./images/teste_alg/teste_digital.png")

        if perc > 20:
            logger.info(
                "Nível de gás baixo detectado pelo manômetro. Enviando notificação..."
            )
            send_to_contacts(default_msg)
            logger.info("Notificação enviada com sucesso.")
        else:
            logger.info("Nível de gás normal. Aguardar próxima verificação.")


# Tons de cinza
def on_message(client, userdata, msg):
    try:
        timestamp = datetime.datetime.now()

        filename = os.path.basename(f'./images/teste/esp32cam-{timestamp.strftime('%Y-%m-%d_%H-%M-%S')}.jpg')

        img_array = np.frombuffer(msg.payload, dtype=np.uint8)

        img = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)

        cv2.imwrite(os.path.join("images", filename), img)

        logger.info("Image received")
    except Exception as e:
        logger.error(f"Error receiving image: {e}")


client.on_message = message_handling

if client.connect("localhost", 1883, 60) != 0:
    logger.error("Couldn't connect to the mqtt broker")
    sys.exit(1)

client.subscribe("imagem/send_image")

try:
    logger.info("Press CTRL+C to exit...")
    client.loop_forever()
except Exception:
    logger.info("Caught an Exception, something went wrong...")
finally:
    logger.info("Disconnecting from the MQTT broker")
    client.disconnect()

