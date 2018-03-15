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
        helpstr = """ Gets comics from **xkcd.com**
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
                # create the embed
                em = self._createEmbedReponse(dict_info['data'], command[0])
                await self.client.send_message(message.channel, 'There you go')
                await self.client.send_message(message.channel, embed=em)
            # no 200
            else:
                await self.client.send_message(message.channel, 'Can\'t reach jisho.org')



    # Creates the embed message for the vocabulary
    #
    # @param jisho_response_data - data object as returned by the jisho API
    # @param search_tag - the tag searched for
    #
    # @return message embed
    def _createEmbedReponse(self, jisho_response_data, search_tag):

        # only get the very first entry
        word = jisho_response_data[0]

        em_mess = discord.Embed(description='[Further information](http://jisho.org/search/%s)' % search_tag, color=0x5CD738)
        # japanese reading message
        em_mess.set_author(name='Jisho.org', url='http://jisho.org/search/%s' % search_tag,  icon_url='https://avatars1.githubusercontent.com/u/12574115?s=200&v=4')

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
