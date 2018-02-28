import discord
import asyncio

class Help:

    def __init__(self, client, dic):
        self.client = client
        self.dic = dic
        self.helpstr = 'Usage of `!help`: `!help <command>`'
        print('Help created')


    async def execute(self, command, message):
        if len(command) == 0:
            await self.help(message)
        elif not command[0] in self.dic:
            await self.client.send_message(message.channel, 'Error. `{}` is not a valid command.'.format(command[0]))
        else:
            await self.dic[command[0]].help(message)



    async def help(self, message):
        await self.client.send_message(message.channel, self.helpstr)
