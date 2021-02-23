# required python-telegram-bot
import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
        )

logger = logging.getLogger(__name__)
TOKEN = '1259530619:AAE0o8QqvPCTze6O5PAq8e10MvwkcaCVuSo'


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
