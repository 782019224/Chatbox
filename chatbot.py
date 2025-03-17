# import telegram
import os

from ChatGPT_HKBU import HKBU_ChatGPT
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackContext
import configparser
import logging
import redis
import requests
global redis1


def main():
    # Load your token and create an Updater for your Bot
    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(
        token=(config['TELEGRAM']['ACCESS_TOKEN']),
        use_context=True
    )
    dispatcher = updater.dispatcher

    global redis1
    redis1 = redis.Redis(
        host=(config['REDIS']['HOST']),
        password=(config['REDIS']['PASSWORD']),
        port=(config['REDIS']['REDISPORT']),
        decode_responses=(config['REDIS']['DECODE_RESPONSE']),
        username=(config['REDIS']['USER_NAME'])
    )
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    # register a dispatcher to handle message: here we register an echo dispatcher
    # echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    # dispatcher.add_handler(echo_handler)


    #dispatcher for chatgpt
    global chatgpt
    chatgpt = HKBU_ChatGPT()
    chatgpt_handler = MessageHandler(Filters.text & (~Filters.command), equiped_chatgpt)
    dispatcher.add_handler(chatgpt_handler)

    # on different commands
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("hello", hello_command))

    # To start the bot
    updater.start_polling()
    updater.idle()


def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update:  " + str(update))
    logging.info("Context:  " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Helping you helping you!')


def add(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try:
        global redis1
        logging.info(context.args[0])
        msg = context.args[0]
        # /add keyword <-- this should store the keyword
        redis1.incr(msg)
        update.message.reply_text(
            'You have said ' + msg + ' for ' +
            redis1.get(msg).decode('UTF-8') + ' times.'
        )
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <keyword>')

def equiped_chatgpt(update, context):
   user_message = update.message.text
   reply_message = chatgpt.submit(user_message)
   logging.info("Update: %s", update)
   logging.info("Context: %s", context)
   context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)


# hello_command
def hello_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /hello is issued."""
    try:
        name = ' '.join(context.args)
        if not name:
            update.message.reply_text("Please provide a name after /hello, e.g., /hello Kevin")
            return
        update.message.reply_text(f"Good day, {name}!")
    except Exception as e:
        logging.error(str(e))
        update.message.reply_text("Something went wrong. Please try again.")

if __name__ == '__main__':
    main()