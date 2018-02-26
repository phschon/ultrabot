import discord
import asyncio
import testfuncrunner

class Testfunc:
    helpstr = '''Supported commands:

    - `start`: starts the test task
    - `stop`: stops the test task
    - `status`: shows the status of the test task'''

    def __init__(self, client):
        print('Test created')
        self.client = client
        self.running = False
        self.dic = {}


    async def execute(self, command, message):
        if not len(command) == 2:
            await self.client.send_message(message.channel, 'Wrong number of arguments. {}'.format(Testfunc.helpstr))
            return
        elif command[1] == 'help':
            await self.help(message)
            return

        if message.channel.id in self.dic:
            self.runner = self.dic[message.channel.id]
        else:
            self.runner = testfuncrunner.Testfuncrunner(self.client)
            self.dic[message.channel.id] = self.runner
            
        if command[1] == 'start':
            if self.runner.isrunning():
                await self.client.send_message(message.channel, 'Task already started.')
            else:
                self.runner.setrunning(True)
                self.client.loop.create_task(self.runner.run(message))
        elif command[1] == 'stop':
            if self.runner.isrunning():
                self.runner.setrunning(False)
                del self.dic[message.channel.id]
            else:
                await self.client.send_message(message.channel, 'Task not running.')
        elif command[1] == 'status':
            if self.runner.isrunning():
                await self.client.send_message(message.channel, 'Task running.')
            else:
                await self.client.send_message(message.channel, 'Task not running.')
        else:
            await self.client.send_message(message.channel, 'Wrong usage of test task. {}'.format(Testfunc.helpstr))


    async def help(self, message):
        await self.client.send_message(message.channel, '`test task` - Default bot testing and debugging.\n\n{}'.format(Testfunc.helpstr))
