import discord
import asyncio

class Testfuncrunner:

    def __init__(self, client):
        print('Testrunner created')
        self.client = client
        self.running = False


    def setrunning(self, val):
        self.running = val

    def isrunning(self):
        self.msg = None
        return self.running

    async def run(self, message):
        print('entering run')
        i = 0
        self.msg = await self.client.send_message(message.channel, 'Testmessage loop {}'.format(i))
        while self.running:
            i = i+1
            if self.msg == None:
                self.msg = await self.client.send_message(message.channel, 'Testmessage loop {}'.format(i))
            else:
                self.msg = await self.client.edit_message(self.msg, 'Testmessage loop {}'.format(i))
            await asyncio.sleep(1)
        await self.client.send_message(message.channel, 'Stopping.')

