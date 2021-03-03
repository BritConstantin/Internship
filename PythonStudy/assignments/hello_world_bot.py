# required python-telegram-bot
import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from PythonStudy.bot_info import my_trib_bot

logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
        )

logger = logging.getLogger(__name__)
TOKEN = my_trib_bot


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text("Hello world")


def echo(update: Update, context: CallbackContext) -> None:
    """Always answer hello world."""
    update.message.reply_text("Hello world")


def main():
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
