import itertools
import random
import requests

import discord
import asyncio

import metamodule

class BlackJack(metamodule.Meta):


    def __init__(self, client):
        # shuffeled card deck
        self.deck = []
        self._resetDeck()

        # call super contructor
        super(BlackJack, self).__init__(client)

    # command to call the plugin
    def get_command(self):
        return 'blackjack'

    # help message
    async def help(self, message):
        helpstr = """ Play Backjack! Doesn't work yet..."""
        await self.client.send_message(message.channel, helpstr)

    # maximum number of allowed parameters
    def get_max_parameters(self):
        return 0

    # functionality
    async def execute(self, command, message):
        pass

    def _resetDeck(self):
        card_list = [Card(combination[0], combination[1]) for combination in itertools.product(range(2, 15),range(4))]
        self.deck = random.sample(card_list, len(card_list))

# playing card
class Card:

    # constructor
    def __init__(self, value, color):
        self.value = value
        self.color = color

    # returns the cards color as a word
    def getVerboseColor(self):
        return ['Spades', 'Clubs', 'Hearts', 'Diamonds'][self.color]

    # returns the verbose value of a card
    def getVerboseValue(self):
        return ([str(x) for x in range(2, 11)] + ['Jack', 'Queen', 'King', 'Ace'])[self.value-2]

    # returns a string in the form of "card of color"
    # Examples:
    #   Ace of Spades
    #   Jack of Diamonds
    #   5 of Clubs
    def getFullVerbose(self):
        return "%s of %s" % (self.getVerboseValue(), self.getVerboseColor())

    # returns the game value for the card
    #   Number of Number
    #   10 for Jack, Queen and King
    #   11 for Ace
    def getGameValue(self):
        return (list(range(2,11)) + ([10]*3) + [11])[self.value-2]
