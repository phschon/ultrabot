import random
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
                - `!%s`: random xkcd comic
                - `!%s <no>`: xkcd comic number <no>
                - `!%s latest`:latest xkcd comic
        """ % tuple([self.get_command()]*3)
        await self.client.send_message(message.channel, helpstr)

    # maximum number of allowed parameters
    def get_max_parameters(self):
        return 1

    # functionality
    async def execute(self, command, message):
        # no further parameters provided
        # ===============
        # random xkcd
        # ===============
        if not command:
            # get the latest comic to check for the number of available comics
            response = requests.get('http://xkcd.com/info.0.json')
            if(response.status_code == 200):
                max_number = response.json()['num']
                await self.client.send_message(message.channel, 'There are currently **%d** comics on **xkcd.com**, here\'s a random one:' % max_number)
                # get a random comic
                response = requests.get('http://xkcd.com/%d/info.0.json' % random.randint(1, max_number+1))
                if(response.status_code == 200):
                    # parse the information
                    comic_information = response.json()
                    # XKCD embed
                    comic_embed = self._createComicEmbed(comic_information)
                    await self.client.send_message(message.channel, embed=comic_embed)
                # something went wrong
                else:
                    await self.client.send_message(message.channel, 'Sorry I coudn\'t reach **xkcd.com**')
            # something went wrong
            else:
                await self.client.send_message(message.channel, 'Sorry I coudn\'t reach **xkcd.com**')
        # further parameters provied
        # exactly one command (because more are restricted by get_max_parameters())
        else:
            # =================================
            # get xkcd with the number provided
            # =================================
            if command[0].isdigit():
                # get the comic with the number provided
                response = requests.get('http://xkcd.com/%s/info.0.json' % command[0])
                if(response.status_code == 200):
                    # parse the information
                    comic_information = response.json()
                    await self.client.send_message(message.channel, 'Here\'s the **xkcd** comic number **%s**:' % comic_information['num'])
                    # XKCD embed
                    comic_embed = self._createComicEmbed(comic_information)
                    await self.client.send_message(message.channel, embed=comic_embed)
                # not 200, might be a 404 for a non existant comic
                else:
                    await self.client.send_message(message.channel, 'Sorry but it seems that **xkcd** number **%s** has not been created yet...' % command[0])
            # provied parameter was not a number
            # =================================
            # latest xkcd
            # =================================
            elif(command[0] == 'latest'):
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
            # unsupported parameter
            else:
                await self.client.send_message(message.channel, 'Sorry but **%s** is not supported...' % command[0])
                await self.help(message)




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
