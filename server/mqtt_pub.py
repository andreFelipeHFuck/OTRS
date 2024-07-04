import asyncio
import logging
import paho.mqtt.client as mqtt
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = mqtt.Client()


# Conectar ao broker MQTT
def connect_mqtt():
    if client.connect("localhost", 1883, 60) != 0:
        logger.error("Não pode se conectar ao broker MQTT")
        sys.exit(1)
    logger.info("Conectado ao broker MQTT")


# Publicar a mensagem MQTT
async def publish_message():
    logger.info("Mensagem enviada")
    client.publish("imagem/request_image", "Ligar!", 0)


# Executar tarefa periodicamente
async def scheduler(interval, task):
    while True:
        await task()
        await asyncio.sleep(interval)


async def main():
    connect_mqtt()
    interval = 3600  # Uma vez por hora
    # interval = 30  # Teste a cada 30 segundos
    logger.info("Iniciando o agendador...")
    await scheduler(interval, publish_message)


if __name__ == "__main__":
    asyncio.run(main())
    client.disconnect()
