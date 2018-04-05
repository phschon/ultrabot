import requests

import discord
import asyncio

import metamodule

class Jisho(metamodule.Meta):

    # command to call the plugin
    def get_command(self):
        return 'jisho'

    # help message
    async def help(self, message):
        helpstr = """ Look up japanese vocab and expressions from **jisho.org**
                - `!%s <word>`: Looks up that word on jisho.org
        """ % self.get_command()
        await self.client.send_message(message.channel, helpstr)

    # maximum number of allowed parameters
    def get_max_parameters(self):
        return 1

    # functionality
    async def execute(self, command, message):
        # this module needs a word it searches for
        if not command:
            await self.client.send_message(message.channel, 'You have to tell me what word to look for')
            await help(message)
        # command specified
        else:
            # command can only be one word so this should work
            response = requests.get('http://jisho.org/api/v1/search/words?keyword=%s' % command[0])
            if(response.status_code == 200):
                # get the response as JSON
                dict_info = response.json()
                await self.client.send_message(message.channel, 'There you go')
                # first 3 vocabs found
                for word in dict_info['data'][:3]:
                    # create the embed
                    em = self._createEmbedReponse(word)
                    await self.client.send_message(message.channel, embed=em)
                # see if not all results were shown
                if len(dict_info['data']) > 3:
                    # link to all search results
                    info_title = 'Showing **3** of **%d** results' % len(dict_info['data'])
                    info_desc  = 'You can find them all [here](http://jisho.org/search/%s)' % command[0]
                    info_embed = discord.Embed(title=info_title, description=info_desc, color=0x5CD738)
                    await self.client.send_message(message.channel, embed=info_embed)
            # no 200
            else:
                await self.client.send_message(message.channel, 'Can\'t reach jisho.org')



    # Creates the embed message for the vocabulary
    #
    # @param word - a word object extracted from the jisho API response
    #
    # @return message embed
    def _createEmbedReponse(self, word):

        # link to the vocabulary
        link = 'http://jisho.org/search/%s' % (word['japanese'][0]['reading'] if not 'word' in word['japanese'][0].keys() else word['japanese'][0]['word'])

        # embed message object
        em_mess = discord.Embed(description='[Further information](%s)' % link, color=0x5CD738)
        # japanese reading message
        em_mess.set_author(name='Jisho.org', url='http://jisho.org', icon_url='https://avatars1.githubusercontent.com/u/12574115?s=200&v=4')

        # format reading message
        reading_message = ""
        for reading_pair in self._extractJapanese(word):
            reading_message += '%s (%s)\n' % reading_pair if reading_pair[0] else '%s\n' % reading_pair[1]
        # add the reading field
        em_mess.add_field(name='Japanese', value=reading_message)

        # english definitions
        eng_def_message = '\n'.join(self._extractEnglish(word))
        em_mess.add_field(name='English', value=eng_def_message)

        return em_mess



    # extracts Kanji and reading
    #
    # @param vocab - vocabulary object returned by the Jisho API
    #
    # @return list of tuples of Kanjis and readings
    def _extractJapanese(self, vocab):
        # get the japanese part
        japanese_part = vocab['japanese']
        # result list
        result = []
        # iterate over all possible pairs
        for jap in japanese_part:
            # pair of Kanji and readings
            reading_pair = (None if not 'word' in jap.keys() else jap['word'], jap['reading'] if jap['reading'] else None)
            result.append(reading_pair)
        # return the readings
        return result



    # creates a list of all the english meanings
    #
    # @params vocab - vocabulary object returned by the Jisho API
    #
    # @return list of english definitions
    def _extractEnglish(self, vocab):
        # get the senses
        senses = vocab['senses']
        # result list
        result = []
        # iterate over all senses
        for sense in senses:
            for word in sense['english_definitions']:
                result.append(word)
        # return the english english definitions
        return result
