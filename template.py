import discord
import asyncio
import metamodule

# This is the template for generating new modules
# In order to work properly each module must inherit the Meta class
# and implement the abstract methods.
# This file shows example content for both functions and variables

class Template(metamodule.Meta):
    def __init__(self, client):
        self.client = client
        # the key word used in a discord message to address this module, e.g. "!samplecommand do_somehting"
        self.command = 'samplecommand'
        # This string is displayed when either !help is called or a wrong usage of parameters is detected
        self.helpstr = '''Supported Commands:
            
        - `command 1`: does something
        - `command 2`: does something else'''

    def command(self):
        return self.command


    async def execute(self, command, message):
        # this module would take one argument, e.g.: !samplecommand start
        if not len(command) == 1:
            await self.client.send_message(message.channel, 'Wrong number of arguments. {}'.format(self.helpstr))
            return
        elif command[0] == 'help':
            await self.help(message)
            return

        # sample commands start and stop
        if command[0] == 'start':
            pass
        elif command[0] == 'stop':
            pass
        else:
            await self.client.send_message(message.channel, 'Wrong usage of template.\n{}'.format(self.helpstr))


    async def help(self, message):
        await self.client.send_message(message.channel, '`template` - Default template.\n\n{}'.format(self.helpstr))
