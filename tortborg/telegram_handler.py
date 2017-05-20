#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from lib import pyborg
import pyborg_interface
import json

# Class designed to handle messages from/to Telegram
class TelegramBotHandler:

    def __init__(self, configData):
        # Storing the bot's configuration
        self.configData = configData
        
        # Connecting to a new pyborg interface
        # to communicate with the pyborg lib
        new_pyborg = pyborg.pyborg()
        try:
            self.pInterface = pyborg_interface.TelegramForPyborg(self, new_pyborg)
        except SystemExit:
            pass
        new_pyborg.save_all()

        self.bot = new_pyborg

    # Basic start method
    def start(self, bot, update):
        update.message.reply_text(self.configData["sentences"]["hi"])

    # Basic help method
    def help(self, bot, update):
        update.message.reply_text(self.configData["sentences"]["help"])

    # Error handler
    def error(self, bot, update, error):
        logger.warn('Update "%s" caused error "%s"' % (update, error))

    # Method called whenevr the bot receives a message,
    # whether from a private or group chat
    def handleReply(self, bot, update):
        # save last data from telegram inside the handler
        self.bot    = bot     # infos about the bot
        self.update = update  # infos about the last received message

        # verify owner
        owner = 0;
        if update.effective_user.username == self.configData["owner"]:
            owner = 1;

        print "Handling message : " + update.message.text

        # send input to pyborg
        self.pInterface.input(str(update.message.text), update.effective_user.username, self.configData["replyRate"], self.configData["learn"], owner)

    # Method called once the pyborg bot returns a newly generated sentence
    # May take a while to be called, depending on the input and the construction of the output
    def sendReply(self, message):
        print "Replying with : " + message
        self.bot.send_message(chat_id=self.update.message.chat_id, text=message)


    # Deploys the dispatcher which connects to this Telegram bot
    def deployTelegramDispatcher(self):

        print "Connecting to bot with token : " + self.configData["token"]

        # Create the EventHandler and pass it the bot's token.
        updater = Updater(self.configData["token"])

        # Get the dispatcher to register handlers
        dp = updater.dispatcher

        # on different commands - answer in Telegram
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(CommandHandler("help", self.help))

        # adding reply handler
        reply_handler = MessageHandler(Filters.text, self.handleReply)
        dp.add_handler(reply_handler)

        # log all errors
        dp.add_error_handler(self.error)

        # Start the Bot
        updater.start_polling()

        print "Now listening to the linked Telegram bot..."

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()
