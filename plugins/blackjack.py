import itertools
import random
import requests

import discord
import asyncio

import metamodule

# A Plugin to play Black Jack
# Supports only 1 player at a time, but multiplayer support is planned
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
                - `!%s new`: Resets the game
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
            card_list_string += "\n\nYour current score is: **%d**" % self._calculateScore()
            await self.client.send_message(message.channel, card_list_string)
            # check for blackjack
            if(self._checkBlackJack()):
                await self.client.send_message(message.channel, "You hit a **Black Jack**, nice!, Lets play another round!")
                self._resetGame()
            # reset the game if the cards surpass 21 in value
            if(self._checkSurpassed21()):
                await self.client.send_message(message.channel, "Too bad, you lost! Let's play another round!")
                self._resetGame()
        # reset the game
        elif command[0] == 'new':
            self._resetGame()
            await self.client.send_message(message.channel, "Sure thing, let's play a new game")
        # player stops the game and gets the score
        elif command[0] == 'stop':
            score = self._calculateScore()
            await self.client.send_message(message.channel, "Sure, your score is **%d**. Let's play another round!" % score)
            # reset the game
            self._resetGame()
        # wrong argument
        else:
            await self.client.send_message(message.channel, "I don't know `%s`..." % command[0])
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


    def _checkBlackJack(self):
        if(len(self.player_cards) > 2):
            return False
        else:
            num_aces = len([card for card in self.player_cards if card.getVerboseValue() == 'Ace'])
            num_10s  = len([card for card in self.player_cards if card.getVerboseValue() == '10'])
            return num_aces == 1 and num_10s == 1


    # calculates the maximal score that is at most 21 or the minimal score above 21 if there is no score
    # below or equal to 21
    def _calculateScore(self):
        # points from non ace cards
        points_of_other_cards = sum([card.getGameValue() for card in self.player_cards if not card.getVerboseValue() == 'Ace'])
        # list of aces
        number_of_aces = len([card for card in self.player_cards if card.getVerboseValue() == 'Ace'])
        # permuations of aces set to on (11) and off (1)
        ace_perm = list(itertools.product([0,1], repeat=number_of_aces))
        # list of possibles scores
        scores = [sum([11 if flag else 1 for flag in perm])+points_of_other_cards for perm in ace_perm]
        print([card.getVerboseValue() for card in self.player_cards])
        print(scores)
        # feasible score list
        feasible_scores = [score for score in scores if score <= 21]
        # infeasible scores
        infeasible_scores = [score for score in scores if score>21]
        # return the maximum feasible score if possible, the minimal infeasible else
        if(len(feasible_scores) > 0):
            return max(feasible_scores)
        else:
            return min(infeasible_scores)






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
