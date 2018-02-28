import requests

from bs4 import BeautifulSoup
import discord
import asyncio

import metamodule

class Howlongtobeat(metamodule.Meta):

    def __init__(self, client):
        # call the super constructor to retain functionality
        super(Howlongtobeat, self).__init__(client)
        # self.client = client
        # header to send withe very HTTP request
        self.header = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*'
        }

    # defines the command to use this module
    def get_command(self):
        return 'howlong'

    # sends the help string to the channel
    async def help(self, message):
        helpstr = """ Gets the time required to beat a game from HowLongToBeat.com
                - `!%s <gametitle>`: Gets the info for the provided game
        """ % self.get_command()
        await self.client.send_message(message.channel, helpstr)

    # main functionality of the module
    async def execute(self, command, message):
        # check if a game title was provided
        if(len(command) > 0):
            # join the commands into one search string
            search_string = ' '.join(command)
            # POST request data object
            data = {
                'queryString': search_string,
                'sorthead': 'popular'
            }
            # make the resquest
            res = requests.post('https://howlongtobeat.com/search_main.php', data=data)
            # check for the response code
            if(res.status_code == 200):
                # parse the HTML with BeautifulSoup4
                html_soup = BeautifulSoup(res.text, 'html.parser')
                # check for the games
                games = html_soup.find_all('div', class_="search_list_details")
                # send info about the number of games found
                await self.client.send_message(message.channel, self._formatInfoMessage(len(games), search_string))
                # send a message for every game
                for game in games:
                    # parse the game inforamtion
                    game_info = self._getGameInfo(game)
                    # format the message
                    game_message = self._formatGameMessage(game_info)
                    # send the message back to the channel
                    await self.client.send_message(message.channel, game_message)
            # Not a 200 response code
            else:
                await self.client.send_message(message.channel, "Can't reach HowLongToBeat.com")
        # no game to search for provided
        else:
            await self.client.send_message(message.channel, "No game title provided")
            await self.help(message)


    # parses the html for a certain game and returns the information
    #
    # @param game_soup - retrieved HTML as a BS4 object
    #
    # @return game inforamtion object
    def _getGameInfo(self, game_soup):
        # parsing straight forward through HowLongToBeat's HTML
        game_title = game_soup.h3.a.text
        # parse the Playstyle Titles and hours
        titles = game_soup.select('.search_list_tidbit.shadow_text')
        hours  = game_soup.select('.search_list_tidbit.center')
        # return the game oject
        return {
            "title": game_title,
            "times": [
                {"playstyle": titles[i].text.strip(),
                 "hours": hours[i].text.strip()
                }
            for i in range(0, len(titles))]
        }

    # takes a game object and formats the message string for the chat
    #
    # @param game_object - a game object such as created by _getGameInfo
    #
    # @return formatted message string
    def _formatGameMessage(self, game_object):
        # create the message
        game_message = "**%s**\n" % game_object["title"]
        game_message += "```"
        for times in game_object["times"]:
            game_message += "%s: %s\n" % (times["playstyle"], times["hours"])
        game_message += "```"

        return game_message

    # formats the info message string to show how many games where found
    #
    # @param number_of_results - number of games found
    # @param search_string     - string used for searching
    #
    # @return formatted info message string
    def _formatInfoMessage(self, number_of_results, search_string):
        if(number_of_results == 0):
            return 'I couldn\'t find any games for **%s**' % search_string
        else:
            plural = "games" if number_of_results > 1 else "game"
            return 'I found %d %s for **%s**:' % (number_of_results, plural, search_string)
