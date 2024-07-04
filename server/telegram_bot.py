import logging
import os
from dotenv import load_dotenv

from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    CallbackContext,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

load_dotenv()

contacts_list = os.getenv("CONTACTS_FILE")
token = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Olá {user.mention_html()}! Se deseja ser notificado quando os níveis de gás armazenados no bloco G estiverem baixos, envie o comando /notificar para entrar na lista de usuários a serem notificados.",
    )


async def notificar(update: Update, _: CallbackContext) -> None:
    user_id = update.message.from_user.id

    # Checa se arquivo existe, caso não, o cria
    if not os.path.exists(contacts_list):
        open(contacts_list, "w").close()

    # Lê os IDs de usuário do arquivo
    with open(contacts_list, "r") as file:
        user_ids = file.read().splitlines()

    if str(user_id) not in user_ids:
        with open(contacts_list, "a") as file:
            file.write(f"{user_id}\n")
        await update.message.reply_text("Você será notificado!")
        logger.info(f"Usuário {user_id} registrado para notificações.")
    else:
        await update.message.reply_text("Você já está registrado para notificações.")


async def remover(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.message.from_user.id)

    not_reg = False

    # Lê os IDs de usuário do arquivo
    if os.path.exists(contacts_list):
        with open(contacts_list, "r") as file:
            user_ids = file.read().splitlines()

        # Verifica se o ID do usuário está no arquivo
        if user_id in user_ids:
            user_ids.remove(user_id)
            with open(contacts_list, "w") as file:
                file.write("".join(user_ids))
            await update.message.reply_text(
                "Você foi removido da lista e não será mais notificado!"
            )
            logger.info(f"Usuário {user_id} removido da lista de notificações.")
        else:
            not_reg = True
    else:
        not_reg = True

    if not_reg:
        await update.message.reply_text("Você não está registrado para notificações!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("notificar", notificar))
    application.add_handler(CommandHandler("remover", remover))
    application.add_handler(CommandHandler(["help", "ajuda"], help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            start,
        )
    )

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
