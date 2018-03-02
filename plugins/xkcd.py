import requests

import discord
import asyncio

import metamodule

class Xkcd(metamodule.Meta):

    # command to call the plugin
    def get_command(self):
        return 'xkcd'

    # help message
    async def help(self, message):
        helpstr = """ Gets comics from **xkcd.com**
                - `!%s`: Get the latest xkcd comic
        """ % self.get_command()
        await self.client.send_message(message.channel, helpstr)

    # functionality
    async def execute(self, command, message):
        # no further parameters provided
        # get latest xkcd
        if not command:
            # get the latest comic
            response = requests.get('http://xkcd.com/info.0.json')
            if(response.status_code == 200):
                # parse the information
                comic_information = response.json()
                await self.client.send_message(message.channel, 'Here\'s the latest **xkcd** comic:')
                # XKCD embed
                comic_embed = self._createComicEmbed(comic_information)
                await self.client.send_message(message.channel, embed=comic_embed)
            # 404 or anything else not 200
            else:
                await self.client.send_message(message.channel, 'Sorry I coudn\'t reach **xkcd.com**')

    # creates an Embed object containing all the information about the comic
    # image, date published, number, title and description
    #
    # @param comic_info - json object as retunred by xkcd.com
    #
    # @return the embed object
    def _createComicEmbed(self, comic_info):
        # title
        title =  "#%s: %s" % (comic_info['num'], comic_info['title'])
        # create the embed object
        em_mess = discord.Embed(title=title, description=comic_info['alt'], color=0x97A9C7)
        # add the comic image
        em_mess.set_image(url=comic_info['img'])
        # date for the footer
        date = "Published on %s.%s.%s" % (comic_info['day'], comic_info['month'], comic_info['year'])
        em_mess.set_footer(text=date)
        # return the embed
        return em_mess
