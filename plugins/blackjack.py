import itertools
import random
import requests

import discord
import asyncio

import metamodule

class BlackJack(metamodule.Meta):


    def __init__(self, client):
        # card deck
        self.deck = []
        # cards drawn by player
        self.player_cards = []

        # reset the game
        self._resetGame()

        # call super contructor
        super(BlackJack, self).__init__(client)

    # command to call the plugin
    def get_command(self):
        return 'blackjack'

    # help message
    async def help(self, message):
        helpstr = """ Play Backjack! Doesn't work yet...
                - `!%s card`: Draw a new card
                - `!%s reset`: Resets the game
        """ % tuple([self.get_command()]*2)
        await self.client.send_message(message.channel, helpstr)

    # maximum number of allowed parameters
    def get_max_parameters(self):
        return 1

    # functionality
    async def execute(self, command, message):
        # draw a new card
        if command[0] == 'card':
            self._drawCard()
            card_list_string = "\n".join([card.getFullVerbose() for card in  self.player_cards])
            await self.client.send_message(message.channel, card_list_string)
            # reset the game if the cards surpass 21 in value
            if(self._checkSurpassed21()):
                await self.client.send_message(message.channel, "You lost!")
                self._resetGame()
        # reset the game
        elif command[0] == 'reset':
            self._resetGame()
            await self.client.send_message(message.channel, "I resetted the game")
        # wrong argument
        else:
            await self.client.send_message(message.channel, "I don't understand `%s`..." % command[0])
            await self.help(message)



    # shuffles the deck (with all cards) and emptys the player_cards list
    def _resetGame(self):
        # shuffle a new deck of cards
        card_list = [Card(combination[0], combination[1]) for combination in itertools.product(range(2, 15),range(4))]
        self.deck = random.sample(card_list, len(card_list))
        # empty player cards
        self.player_cards = []



    # draws a card from the deck and adds it to the player_cards list
    #
    # @return the card
    def _drawCard(self):
        card = self.deck.pop()
        self.player_cards.append(card)
        return card



    # checks if the player has surpassed the value of 21
    # Aces are treated as 1s
    #
    # @return true if >21 else false
    def _checkSurpassed21(self):
        # choose 1 as the value for Aces
        return sum([1 if card.getVerboseValue() == 'Ace' else card.getGameValue() for card in self.player_cards]) > 21







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
        return "**%s** of **%s**" % (self.getVerboseValue(), self.getVerboseColor())



    # returns the game value for the card
    #   Number of Number
    #   10 for Jack, Queen and King
    #   11 for Ace
    def getGameValue(self):
        return (list(range(2,11)) + ([10]*3) + [11])[self.value-2]
