import itertools
import random
import requests
import textwrap

import discord
import asyncio

import metamodule

# A Plugin to play Black Jack
# Supports only 1 player at a time, but multiplayer support is planned
class BlackJack(metamodule.Meta):


    def __init__(self, client):
        # card deck
        self.deck = Deck()
        # cards drawn by player
        self.player_cards = []
        # cards drawn by the dealer
        self.dealer_cards = []

        # flag if a game is running
        self.game = False

        # reset the game
        self._resetGame()

        # call super contructor
        super(BlackJack, self).__init__(client)

    # command to call the plugin
    def get_command(self):
        return 'blackjack'

    # help message
    async def help(self, message):
        helpstr = """ Play Backjack!
                - `!%s hit`: Draw a new card
                - `!%s new`: Start a new game
                - `!%s rules`: Show rules
                - `!%s stand`: Stop drawing new cards and take the score
        """ % tuple([self.get_command()]*4)
        await self.client.send_message(message.channel, helpstr)

    # maximum number of allowed parameters
    def get_max_parameters(self):
        return 1

    # functionality
    async def execute(self, command, message):
        # draw a new card
        if command[0] == 'hit':
            # game running
            if self.game:
                self._drawPlayerCard()
                response_message = self._playerCardsString()
                response_message += "\n\nYour current score is: **%d**\n" % self._calculateScore(self.player_cards, 21)
                # reset the game if the cards surpass 21 in value
                if(self._checkSurpassed21()):
                    response_message += "Too bad, you busted! Let's play another round!"
                    await self.client.send_message(message.channel, response_message)
                    self._resetGame()
                # continue otherwise
                else:
                    response_message += "You wanna **hit** or **stand**?"
                    await self.client.send_message(message.channel, response_message)
            # game not running
            else:
                await self.client.send_message(message.channel, "You have to start a game first. Use `!%s new` for that" % self.get_command())

        # start a new game
        elif command[0] == 'new':
            self.game = True
            response_message = "Sure thing, let's play a new game, here's the deal\n\n"
            # draw initial deal
            self._drawPlayerCard()
            self._drawDealerCard()
            self._drawPlayerCard()
            self._drawDealerCard()
            # show dealer cards
            response_message += "My cards: %s\n\n" % self._dealerCardsString()
            response_message += "Your cards: %s\n\n" % self._playerCardsString()
            # check for a Black Jack
            if(self._checkBlackJack()):
                response_message += "You hit a **Black Jack**, you won!, Let's play another round!"
                await self.client.send_message(message.channel, response_message)
            # continue the game if the player did not hit a Black Jack
            else:
                response_message += "Your current score is: **%d**\n" % self._calculateScore(self.player_cards, 21)
                response_message += "You wanna **hit** or **stand**?"
                await self.client.send_message(message.channel, response_message)

        # player stops the game and gets the score
        elif command[0] == 'stand':
            # game running
            if self.game:
                player_score = self._calculateScore(self.player_cards, 21)
                response_message = "Sure, your score is **%d**. I'll draw my cards!\n\n" % player_score
                # dealer has to draw cards until he has at least 17 points
                while self._calculateScore(self.dealer_cards, 17) < 17:
                    self._drawDealerCard()
                # check if the dealer has overpaid or not
                if self._calculateScore(self.dealer_cards, 21) > 21:
                    response_message += "Oh, damn it I busted. Your win!"
                # dealer has not overpaid
                else:
                    response_message += "My cards: %s\n\n" % self._dealerCardsString(hidden=False)
                    dealer_score = self._calculateScore(self.dealer_cards, 21)
                    response_message += "Score: **%s**\n" % dealer_score
                    if(dealer_score > player_score):
                        response_message += "Looks like I've won"
                    else:
                        response_message += "Look's like you've won"

                await self.client.send_message(message.channel, response_message)
                # reset the game
                self._resetGame()
            # game not running
            else:
                await self.client.send_message(message.channel, "You have to start a game first. Use `!%s new` for that" % self.get_command())

        # show the rules
        elif command[0] == 'rules':
            rules = textwrap.dedent("""
            Black Jack is a pretty simple game, on the **deal** we both draw two cards (my second one is *hidden* however). Your goal is to stay below **21** but as close as possible.

            You can either **hit** (`!%s hit`) to get a new card or **stand** (`!%s stand`) if you don't want to draw a new card.

            After that I will draw my cards until I reach at least **17** points. Whoever has the highest score wins.

            If you hit a **10** and an **Ace** on the deal that's a **Black Jack** and you win immediately.

            Card Values:
            **Numbers**: Their **number**
            **Jack**, **Queen** and **King**: **10**
            **Ace**: **1** or **11**

            The **ace** value is automatically chosen to best fit the situation

            Have fun playing!""" % tuple([self.get_command()]*2))
            await self.client.send_message(message.channel, rules)
        # wrong argument
        else:
            await self.client.send_message(message.channel, "I don't know `%s`..." % command[0])
            await self.help(message)



    # shuffles the deck (with all cards) and emptys the player_cards list
    def _resetGame(self):
        # shuffle a new deck of cards
        self.deck.reset()
        # empty player cards
        self.player_cards = []
        # empty dealer cards
        self.dealer_cards = []
        # game state
        self.game = False



    # draws a card from the deck and adds it to the player_cards list
    #
    # @return the card
    def _drawPlayerCard(self):
        card = self.deck.draw()
        self.player_cards.append(card)
        return card

    # draws a card from the deck and adds it to the dealer_cards list
    #
    # @return the card
    def _drawDealerCard(self):
        card = self.deck.draw()
        self.dealer_cards.append(card)
        return card



    # checks if the player has surpassed the value of 21
    # Aces are treated as 1s
    #
    # @return true if >21 else false
    def _checkSurpassed21(self):
        # choose 1 as the value for Aces
        return sum([1 if card.getVerboseValue() == 'Ace' else card.getGameValue() for card in self.player_cards]) > 21


    # checks for a Black Jack on the first 2 cards
    #
    # @return true if Black Jack false otherwise
    def _checkBlackJack(self):
        if(len(self.player_cards) > 2):
            return False
        else:
            num_aces = len([card for card in self.player_cards if card.getVerboseValue() == 'Ace'])
            num_10s  = len([card for card in self.player_cards if card.getVerboseValue() == '10'])
            return num_aces == 1 and num_10s == 1



    # calculates the maximal score that is at most 21 or the minimal score above 21 if there is no score
    # below or equal to 21
    def _calculateScore(self, card_list, limit):
        # points from non ace cards
        points_of_other_cards = sum([card.getGameValue() for card in card_list if not card.getVerboseValue() == 'Ace'])
        # list of aces
        number_of_aces = len([card for card in card_list if card.getVerboseValue() == 'Ace'])
        # permuations of aces set to on (11) and off (1)
        ace_perm = list(itertools.product([0,1], repeat=number_of_aces))
        # list of possibles scores
        scores = [sum([11 if flag else 1 for flag in perm])+points_of_other_cards for perm in ace_perm]
        print([card.getVerboseValue() for card in card_list])
        print(scores)
        # feasible score list
        feasible_scores = [score for score in scores if score <= limit]
        # infeasible scores
        infeasible_scores = [score for score in scores if score>limit]
        # return the maximum feasible score if possible, the minimal infeasible else
        if(len(feasible_scores) > 0):
            return max(feasible_scores)
        else:
            return min(infeasible_scores)


    def _dealerCardsString(self, hidden=True):
        # when the dealer has more than 2 cards show them all
        if len(self.dealer_cards) > 2 or not hidden:
            return "  ".join([card.getFullEmojiVerbose() for card in  self.dealer_cards])
        else:
            return "%s  :black_medium_square:" % self.dealer_cards[0].getFullEmojiVerbose()


    def _playerCardsString(self):
        return "  ".join([card.getFullEmojiVerbose() for card in  self.player_cards])

# deck of cards
class Deck:

    # constructor
    def __init__(self):
        # list of cards
        self.cards = []
        # reset the deck
        self.reset()



    # shuffles the deck (with new cards)
    def reset(self):
        # shuffle a new deck of cards
        card_list = [Card(combination[0], combination[1]) for combination in itertools.product(range(2, 15),range(4))]
        self.cards = random.sample(card_list, len(card_list))



    # draws a card
    #
    # @return a Card
    def draw(self):
        return self.cards.pop()




# playing card
class Card:

    # constructor
    def __init__(self, value, color):
        # card's value
        self.value = value
        # card's color
        self.color = color



    # returns the cards color as a word
    def getVerboseColor(self):
        return ['Spades', 'Clubs', 'Hearts', 'Diamonds'][self.color]

    # returns the emoji for the card's color
    def getEmojiColor(self):
        return [':spades:', ':clubs:', ':hearts:', ':diamonds:'][self.color]

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



    # returns a string in the form of "<coloremoji>Value"
    def getFullEmojiVerbose(self):
        return "%s**%s**" % (self.getEmojiColor(), self.getVerboseValue())



    # returns the game value for the card
    #   Number of Number
    #   10 for Jack, Queen and King
    #   11 for Ace
    def getGameValue(self):
        return (list(range(2,11)) + ([10]*3) + [11])[self.value-2]
