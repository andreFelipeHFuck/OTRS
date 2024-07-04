import logging
import os

from telegram import Bot
from dotenv import load_dotenv

# Configuração do logging
logger = logging.getLogger(__name__)

load_dotenv()

contacts_list = os.getenv("CONTACTS_FILE")
token = os.getenv("TELEGRAM_BOT_TOKEN")

# message = "Aviso: O nível de gás supervisionado pelo ESP32 está baixo!"

# Inicializa o bot
telegram_bot = Bot(token=token)


async def send_to_contacts(message) -> None:
    if os.path.exists(contacts_list):
        with open(contacts_list, "r") as file:
            user_ids = file.readlines()

        for user_id in user_ids:
            try:
                await telegram_bot.send_message(
                    chat_id=int(user_id.strip()), text=message
                )
            except Exception as e:
                logger.error(f"Erro ao enviar notificação para {user_id}: {e}")

        logger.info("Notificações enviadas com sucesso.")
    else:
        logger.warning("Nenhum usuário registrado para notificações.")
