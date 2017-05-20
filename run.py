#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tortborg import telegram_handler
import json
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
        
def main():
    print "-----------------------"
    print "- Welcome to tortborg -"
    print "-----------------------"

    with open('config.json') as config_data:
        jsonData = json.load(config_data)

    if len(jsonData["bots"]) == 0:
        print "No bot configured at this time. Please add a new one in your configuration file."
        return

    # Creates a new handler for every configured bot
    for bot in jsonData["bots"]:
        telegramBotHandler = telegram_handler.TelegramBotHandler(bot)

if __name__ == '__main__':
    main()