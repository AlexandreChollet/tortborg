#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Class designed to communicate with a newly instancied pyborg
class TelegramForPyborg:
    def __init__(self, context, my_pyborg):
    	self.context			= context
        self.pyborg 			= my_pyborg
        self.generatedMessage   = ""

    # Sends a new message to pyborg
    # self 			: the instancied TelegramForPyborg
	# message 		: the body of the message sent to pyborg
	# replyrate     : the chance for pyborg to reply with a sentence (%)
	# name 			: the name of the person who sent the message
	# owner			: whether or not this is the bot's owner
    def input(self, message, name, replyrate = 100, learn = 1, owner = 0):
        self.pyborg.process_msg(self, message, replyrate, 1, (name), owner)

    # When pyborg returns a new sentence
    def output(self, message, args):
        self.generatedMessage = message
        self.context.sendReply(self.generatedMessage)