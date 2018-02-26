import discord
import asyncio
import random
import math

class Swag:
    def __init__(self, client):
        print('swag created')
        self.client = client
        self.helpstr = '''Usage:

        - `!swag <name>`: transform your name into something.....'''
        self.UPPERCASE_CHANCE = 0.5
        self.LETTER_REPLACE_CHANCE = 0.8
        self.TRIPLE_CHANCE = 0.1
        self.MAX_TAGS = 4

        self.letter_replacements = {
            'S' : '$',
            'A' : '4',
            'a': '@',
            'l' : '1',
            'i' : '1',
            'I' : '1',
            'o' : '0',
            's' : 'z',
            'H' : "#",
            'z' : 'zzz',
            'Z' : 'ZZZ',
            'g': 'ggg',
            'G': 'GGG',
            'E' : '3',
            'e' : '3',
            's': '$',
            't' : '+',
            'D' : '|)'}

        self.decorations = [
            'x',
            'X',
            'xX',
            'xxx',
            '~',
            '.-~',
            'xXx',
            'XxX',
            'xxX_',
            '|',
            './|',
            '@@@',
            '$$$',
            '***',
            '+',
            '|420|',
            '.::',
            '.:',
            '.-.',
            '|||',
            '--',
            '*--']

        self.tags = [
            'SHOTS FIRED',
            '420',
            'LEGIT',
            '360',
            'Pr0',
            'NO$$$cop3z',
            '0SC0pe',
            'MLG',
            'h4xx0r',
            'M4X$W4G',
            'L3G1TZ',
            '3edgy5u',
            '2edgy4u',
            'nedgy(n+2)u',
            's0b4s3d',
            'SWEG',
            'LEGIT',
            'WUBWUBWUB',
            'BLAZEIT',
            'b14Z3d',
            '[le]G1t',
            '60x7',
            '24x7BLAZEIT',
            '4.2*10^2',
            'literally',
            '[le]terally',
            '1337',
            'l33t',
            '31337',
            'Tr1Ck$h0t',
            'SCRUBLORD',
            'DR0PTH3B4$$',
            'w33d',
            'ev REE DAI',
            'MTNDEW',
            'WATCH OUT',
            'EDGY',
            'ACE DETECTIVE',
            '90s KID',
            'NO REGRETS',
            'THANKS OBAMA',
            'SAMPLE TEXT',
            'FAZE',
            'U|_TR@',
            'ULTRA',
            '#nofilter']



    async def random_choice(self, l):
            return l[math.floor(random.random()*len(l))]



    async def decorate(self, s):
        decoration = await self.random_choice(self.decorations)
        return decoration + s + ''.join(list(decoration)[::-1])



    async def add_tags(self, s):
        # Between 0 and MAX_TAGS - 1 tags are added at the front.
        numtags = math.floor(random.random()*(self.MAX_TAGS)) 

        for i in range(0, numtags):
            s = '[' + await self.random_choice(self.tags) + ']' + s

        return s



    async def randomise_case(self, letter):
        if random.random() < self.UPPERCASE_CHANCE:
            return letter.upper()
        else:
            return letter.lower()



    async def transform(self, s):
        swag_array = list(s)

        replacement = None

        # wait what is this actually a for loop in js i don't get it needs more jQuery plugins
        for i in range(0, len(swag_array)):

            if random.random() < self.LETTER_REPLACE_CHANCE:
                if swag_array[i] in self.letter_replacements:
                    replacement = self.letter_replacements[swag_array[i]]

            # randomize the case EVEN AFTER WE REPLACED? SOMEBODY STOP ME
            swag_array[i] = await self.randomise_case(swag_array[i])

        #  At most once, replace a letter with that letter 3 times. Y'know, like they do ON THE STREETS.
        if random.random() < self.TRIPLE_CHANCE:

            triple_index = math.floor(random.random() * len(swag_array))
            letter = swag_array[triple_index]
            triple_letter = ""

            #  What even is this wacky code how do you multiply strings in js guido save me (reddit.com/r/basedguido)
            for i in range(0,3):
                triple_letter = triple_letter + letter

            swag_array[triple_index] = triple_letter


        # string status: [ ] mutable
        #                [x] not mutable
        s = ''.join(swag_array)

        s = await self.decorate(s)
        s = await self.add_tags(s)

        s = s.replace('le', '[le]') # GOTTA do this
        return s


    async def execute(self, command, message):
        if not len(command) == 2:
            await self.client.send_message(message.channel, 'Wrong number of arguments. {}'.format(self.helpstr))
            return
        elif command[1] == 'help':
            await self.help(message)
            return

        await self.client.send_message(message.channel, await self.transform(command[1]))



    async def help(self, message):
        await self.client.send_message(message.channel, '`Swagify your name` - powered by swagify.net.\n\n{}'.format(self.helpstr))
