import discord
import asyncio
import random

class Randomgen:
    def __init__(self, client):
        print('random created')
        self.client = client
        self.helpstr = '''Supported commands:
        - `<number>d<die>`: Roll <die> <number> of times
        - `<number>w<die>`: Roll <die> <number> of times'''


    async def execute(self, command, message):
        if not len(command) == 2:
            await self.client.send_message(message.channel, 'Wrong number of arguments.{}'.format(self.helpstr))
            return
        elif command[1] == 'help':
            await self.help(message)
            return


        random.seed()
        res = 0
        out = ""
        if "d" in command[1]:
            num, die = command[1].split("d")
        elif "w" in command[1]:
            num, die = command[1].split("w")
        else:
            await self.client.send_message(message.channel, 'Wrong usage of random. {}'.format(self.helpstr))
            return

        if num == "":
            num = 1
        if die == "":
            die = 1

        if int(num) > 1000:
            await self.client.send_message(message.channel, "Nope, that's too much dude...")
            return

        if int(num) > 100:
            await self.client.send_message(message.channel, 'Dude... srsly? Hmpf...')


        for i in range(0,int(num)):
            rand = random.randrange(int(die)) + 1
            res = res + rand
            out = out + ", " +str(rand)
            print(rand, res, out)

        await self.client.send_message(message.channel, '{} ({})'.format(str(res), out[2:]))




    async def help(self, message):
        await self.client.send_message(message.channel, '`random` - Generate random die rolls.\n\n{}'.format(self.helpstr))
