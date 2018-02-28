import discord
import asyncio
import modules.testfuncrunner
import metamodule

class Testfunc(metamodule.Meta):

    def __init__(self, client):
        self.client = client
        self.running = False
        self.dic = {}
        self.helpstr = '''Supported commands:

    - `start`: starts the test task
    - `stop`: stops the test task
    - `status`: shows the status of the test task'''
        self.command = 'test'

    def get_command(self):
        return self.command


    async def execute(self, command, message):
        if not len(command) == 1:
            await self.client.send_message(message.channel, 'Wrong number of arguments. {}'.format(self.helpstr))
            return
        elif command[0] == 'help':
            await self.help(message)
            return

        if message.channel.id in self.dic:
            self.runner = self.dic[message.channel.id]
        else:
            self.runner = modules.testfuncrunner.Testfuncrunner(self.client)
            self.dic[message.channel.id] = self.runner
            
        if command[0] == 'start':
            if self.runner.isrunning():
                await self.client.send_message(message.channel, 'Task already started.')
            else:
                self.runner.setrunning(True)
                self.client.loop.create_task(self.runner.run(message))
        elif command[0] == 'stop':
            if self.runner.isrunning():
                self.runner.setrunning(False)
                del self.dic[message.channel.id]
            else:
                await self.client.send_message(message.channel, 'Task not running.')
        elif command[0] == 'status':
            if self.runner.isrunning():
                await self.client.send_message(message.channel, 'Task running.')
            else:
                await self.client.send_message(message.channel, 'Task not running.')
        else:
            await self.client.send_message(message.channel, 'Wrong usage of test task. {}'.format(self.helpstr))


    async def help(self, message):
        await self.client.send_message(message.channel, '`test task` - Default bot testing and debugging.\n\n{}'.format(self.helpstr))
