#!/usr/bin/env python
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import json.decoder
from pathlib import Path
from typing import Dict

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    )

from PythonStudy.Hints.db_worker import DbWorker
from PythonStudy.bot_info import my_trib_bot, h_bot

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [
    ['Age', 'Favourite colour'],
    ['Number of siblings', 'Something else...'],
    ['Done', 'Debug']
    ]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def facts_to_str(user_data: Dict[str, str]) -> str:
    facts = list()

    for key, value in user_data.items():
        facts.append(f'{key} - {value}')

    return "\n".join(facts).join(['\n', '\n'])


def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
            "Hi! My name is Doctor Botter. I will hold a more complex conversation with you. "
            "Why don't you tell me something about yourself?",
            reply_markup=markup,
            )
    # print('Context:')
    # print(context)
    # print('Update:')
    # print(update)
    #
    # print('User:')
    # print(update['message']['chat'])

    return CHOOSING


def regular_choice(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    context.user_data['choice'] = text

    update.message.reply_text(f'Your {text.lower()}? Yes, I would love to hear about that!')

    return TYPING_REPLY


def custom_choice(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
            'Alright, please send me the category first, ' 'for example "Most impressive skill"'
            )

    return TYPING_CHOICE


def received_information(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    update.message.reply_text(
            "Neat! Just so you know, this is what you already told me:"
            f"{facts_to_str(user_data)} You can tell me more, or change your opinion"
            " on something.",
            reply_markup=markup,
            )

    return CHOOSING


def done(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text(
            f"I learned these facts about you: {facts_to_str(user_data)} Until next time!"
            )
    update.message.reply_text(str(user_data))
    print(context)
    user_data.clear()
    return ConversationHandler.END


def save_message_to_db(update: Update, context: CallbackContext ):
    user = update.message.from_user
    print(f'-> catch message {update.message.message_id} '
          f'from user {user.id}({user.full_name}):')
    print(update.message)

    db_name = Path(__file__).name[:-3]
    db = DbWorker(db_name)  # db name created from the file name
    table_name = 'messages'
    users_hat = {
        'message_id': 'integer',
        'user_id': 'integer',
        'message': 'string'
        }

    db = DbWorker(db_name)
    db.create_table(table_name, users_hat)
    db.insert_row(table_name, users_hat.keys(),
                  (update.message.message_id,
                   user.id,
                   update.message.to_json()))


def get_db_messages(update: Update, context: CallbackContext):
    user = update.message.from_user
    print(f'Here is all messages from db.message :')

    db_name = Path(__file__).name[:-3]
    db = DbWorker(db_name)  # db name created from the file name
    table_name = 'messages'
    users_hat = {
        'message_id': 'integer',
        'user_id': 'integer',
        'message': 'string'
        }

    db = DbWorker(db_name)
    table_data = db.get_all_table_rows(table_name)

    for row in table_data:
        update.message.reply_text(row)
        print(row)


def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater(my_trib_bot)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    db_save_handler = MessageHandler(Filters.text | Filters.command, save_message_to_db)

    conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start)],
            states={
                CHOOSING: [
                    MessageHandler(Filters.regex('^(Age|Favourite colour|Number of siblings)$'),
                                   regular_choice),
                    MessageHandler(Filters.regex('^Something else...$'), custom_choice),
                    ],
                TYPING_CHOICE: [
                    MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Done$')), regular_choice)
                    ],
                TYPING_REPLY: [
                    MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                                   received_information, )
                    ],
                },
            fallbacks=[MessageHandler(Filters.regex('^Done$'), done)],
            )

    dispatcher.add_handler(CommandHandler("db_messages", get_db_messages))

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(db_save_handler)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
