#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from lib import pyborg
import pyborg_interface

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
        del new_pyborg

        # Deploying dispatcher to handle messages through the Telegram API
        self.deployTelegramDispatcher()

    # Define a few command handlers. These usually take the two arguments bot and
    # update. Error handlers also receive the raised TelegramError object in error.
    def start(self, bot, update):
        update.message.reply_text(self.configData["sentences"]["hi"])


    def help(self, bot, update):
        update.message.reply_text(self.configData["sentences"]["help"])


    def handleReply(self, bot, update):
        # save last data from telegram inside the handler
        self.bot    = bot     # infos about the bot
        self.update = update  # infos about the last received message

        # verify owner
        owner = 0;
        if update.effective_user.username == self.configData["owner"]:
            owner = 1;

        print update.message.from_user

        # send input to pyborg
        self.pInterface.input(str(update.message.text), update.effective_user.username, self.configData["replyRate"], self.configData["learn"], owner)

    def sendReply(self, message):
        self.bot.send_message(chat_id=self.update.message.chat_id, text=message)

    def error(self, bot, update, error):
        logger.warn('Update "%s" caused error "%s"' % (update, error))


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