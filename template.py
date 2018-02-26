import discord
import asyncio

# change all template occurrences
# change helpstr
# adapt start and stop commands and number of needed commands

class Template:
    def __init__(self, client):
        print('template created')
        self.client = client
        self.helpstr = '''Supported Commands:
            
        - `command 1`: does something
        - `command 2`: does something else'''


    async def execute(self, command, message):
        if not len(command) == 2:
            await self.client.send_message(message.channel, 'Wrong number of arguments. {}'.format(self.helpstr))
            return
        elif command[1] == 'help':
            await self.help(message)
            return

        if command[1] == 'start':
            pass
        elif command[1] == 'stop':
            pass
        else:
            await self.client.send_message(message.channel, 'Wrong usage of template.\n{}'.format(self.helpstr))


    async def help(self, message):
        await self.client.send_message(message.channel, '`template` - Default template.\n\n{}'.format(self.helpstr))
