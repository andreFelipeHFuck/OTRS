import logging
import os
import asyncio
import schedule
from telegram import Bot

# Configuração do logging
logger = logging.getLogger(__name__)

CONTACTS_FILE = "./python-env/contatos.txt"
TOKEN = "7264200561:AAGX-DV5oo7TO2X7Y4NLzIvVcXngDeJJtWU"

message = "Aviso: O nível de gás supervisionado pelo ESP32 está baixo!"

# Inicializa o bot
telegram_bot = Bot(token=TOKEN)


async def enviar_notificacao() -> None:
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "r") as file:
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


# Envia notificação
asyncio.run(enviar_notificacao())
