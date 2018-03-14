import random

import requests
import discord
import asyncio

import metamodule

import urllib.request, json

# pr0gramm Plugin
#
# Searches for random images on pro0gramm form the popupar section
# An arbitrary amount of search tags can be provided
#
class pr0gramm(metamodule.Meta):

    # command to call the plugin
    def get_command(self):
        return 'pr0'

    # sends help message
    async def help(self, message):
        help_str = """ Gets a random image or video from **pr0gramm.com**
                - `!%s <tag1> ... <tagn>`: Random image or video with the provided tags attached
                - `!%s`: Random image or video
        """ % tuple([self.get_command()]*2)
        await self.client.send_message(message.channel, help_str)

    # main functionality of the plugin
    async def execute(self, command, message):
        # no command provided get some random pr0gramm image
        random_item = self._getRandomItem(command)
        # if we got something back from pr0gramm send it to the channel
        if(random_item):
            # info message
            await self.client.send_message(message.channel, self._formatInfoMessage(command))
            # send the url to the channel
            await self.client.send_message(message.channel, self._generateUrl(random_item))
        # if we couldn't get anything send an error message
        else:
            await self.client.send_message(message.channel, 'I couldn\'t find anything for %s' % self._formatTags(command))



    # gets a random item from pr0gramm with the given tags attached
    #
    # @param tags - list of tags
    #
    # @return image object from the pr0gramm API or None if nothing was found
    def _getRandomItem(self, tags=[]):
        res = requests.get('http://pr0gramm.com/api/items/get', {
            # SFW
            'flags': 1,
            'promoted': 1,
            'tags': tags
        })
        # check if the request was ok
        if res.status_code == 200:
            # parse the items
            items = res.json()["items"]
            if items:
                # get a random item
                return items[random.randrange(0, len(items))]
            else:
                return None

        # if the response code was not 200 something went wrong
        else:
            return None



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


    # formats the list of tags into a natural sounding sentence
    # Example: tag1, tag2 and tag3
    # Example: tag1 and tag2
    #
    # @param tags - the search tags
    #
    # @return formatted info string
    def _formatTags(self, tags):
        # no search tags provided
        if not tags:
            return ""
        # search tags provied
        else:
            # more than 2
            if len(tags) > 2:
                tag_message = ""
                tag_message += "".join(["**%s**, " % tag for tag in  tags[:len(tags)-2]])
                tag_message += "**%s** and **%s**" % (tags[len(tags)-2], tags[len(tags)-1])
                return tag_message
            # exactly 2
            elif len(tags) == 2:
                return "**%s** and **%s**" % (tags[0], tags[1])
            # exactly 1
            else:
                return "**%s**" % tags[0]


    # generates the info message for the bot response for the tags provided
    # for the search
    #
    # @param tags - the search tags
    #
    # @return info message string
    def _formatInfoMessage(self, tags):
        # no search tags provided
        if not tags:
            return 'Here\'s what I found:'
        # search tags provided
        else:
            return 'Here\'s what I found for %s:' % self._formatTags(tags)



class reddit(metamodule.Meta):
    def __init__(self, client):
        self.client = client
        self.command = 'reddit'
        self.redlist = ['shitty_car_mods',
                       'programmerhumor',
                       'earthporn',
                       'funny',
                       'crappydesign',
                       'punny',
                       'justrolledintotheshop']
        self.helpstr = '''Supported Commands:

        - without further parameters, get a random post from a secret list
        - `<subreddit>`: get a random post from the `subreddit` sorted by `new`
        - `<subreddit>` `<new/hot>`: get a random post from the `subreddit` either sorted by `new` or `hot`'''


    def get_command(self):
        return self.command

    async def execute(self, command, message):
        if (len(command) == 1 and command[0] == 'help') or len(command) > 2:
            await self.help(message)
            return


        subred = self.redlist[random.randrange(len(self.redlist))]

        # TODO new/hot might not work
        if len(command) == 1:
            if command[0] == 'new' or command[0] == 'hot':
                sort = command[0]
            else:
                subred = command[0]
                sort = 'new'


        if len(command) == 2:
            if command[1] == 'new' or command[1] == 'hot':
                subred = command[0]
                sort = command[1]
            else:
                await self.client.send_message(message.channel, command[1] + ' is not a valid argument.')
                return


        try:
            with urllib.request.urlopen("https://www.reddit.com/r/" + subred + "/new.json?sort=new") as url:
                j = json.loads(url.read().decode())
        except urllib.error.HTTPError:
            await self.client.send_message(message.channel, 'Error: Too many requests. I will soon be authenticating via OAuth...for sure...')
            return


        # TODO this may crash because not all posts have an image
        try:
            index = random.randrange(len(j['data']['children']))
        except ValueError:
            await self.client.send_message(message.channel, 'I did not find anything for subreddit ' + subred + '.')

        img = j['data']['children'][index]['data']['url']
        await self.client.send_message(message.channel, 'Look at this post from ' + subred + ':\n{}'.format(img))



    async def help(self, message):
        await self.client.send_message(message.channel, '`reddit` - Get reddit posts either from a subreddit of your choice or one of our secret list.\n\n{}'.format(self.helpstr))
