import random

import requests
import discord
import asyncio

import metamodule

class pr0gramm(metamodule.Meta):

    # command to call the plugin
    def get_command(self):
        return 'pr0'

    # sends help message
    async def help(self, message):
        help_str = """ Gets a random image or video from **pr0gramm.com**
                - `!%s`: Random image or video
        """ % self.get_command()
        await self.client.send_message(message.channel, help_str)

    # main functionality of the plugin
    async def execute(self, command, message):
        # no command provided get some random pr0gramm image
        if not command:
            res = requests.get('http://pr0gramm.com/api/items/get', {
                # SFW
                'flags': 1,
                'promoted': 1,
            })
            # check if the request was ok
            if res.status_code == 200:
                # parse the items
                items = res.json()["items"]
                # get a random item
                random_item = items[random.randint(0, len(items))]
                # info message
                await self.client.send_message(message.channel, 'Here\'s what I found:')
                # send the url to the channel
                await self.client.send_message(message.channel, self._generateUrl(random_item))
            else:
                await self.client.send_message(message.channel, 'I couldn\'t reach **pro0gramm.com**')


    # gererates the URL to the resource. It differs for videos and images
    #
    # @param item - the item object as returned by the pr0gramm API
    #
    # @return URL string
    def _generateUrl(self, item):
        # get the items extension
        _, ext = item["image"].split('.')
        if(ext == 'mp4'):
            return 'http://vid.pr0gramm.com/%s' % item["image"]
        else:
            return 'http://img.pr0gramm.com/%s' % item["image"]
