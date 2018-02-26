import discord
import asyncio
import testfunc
import helpfunc
import randomgen
import play_music
import swag

with open('token', 'r') as f:
    token = f.readline()[:-1]

client = discord.Client()
tasks = {'test' : testfunc.Testfunc(client), 'random' : randomgen.Randomgen(client), 'music' : play_music.Music(client), 'swag' : swag.Swag(client)}
tasks['help'] = helpfunc.Helpfunc(client, tasks)

tip = '''Available commands: `!music`,  `!swag`, `!test`, `!random`, `!help`

Use `!help <command>` for information about commands.'''


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    #for x in client.servers:
    #    print(x.id, x.name)


@client.event
async def on_message_delete(message):
    await tasks['archive'].notify(message)
#    await client.send_message(message.channel,
#                              '{} wrote: "{}" at {}'.format(message.author, message.content, message.timestamp))
#        print(message.channel, message.content)
#        print(message.author.id, client.user.id)
#        if (message.author.id != client.user.id):
#            await client.send_message(message.channel, message.content[1:])


async def background_task(channel):
    # for i in range(0,2):
    shotdown = False
    i = 0
    while not shotdown:
        await client.send_message(channel, 'Testmessage loop {}'.format(i))
        i = i+1
        await asyncio.sleep(1)
    await client.send_message(channel, 'Stopping.')


@client.event
async def on_message(message):
    print(message.channel, message.channel.id, message.content)
    if not message.content.startswith('!'):
        return
    command = str.split(message.content)
    command[0] = command[0][1:]

    if command[0] == 'list':
        await client.send_message(message.channel, tip)
        return

    if not command[0] in tasks:
         await client.send_message(message.channel, 'Command not supported. {}'.format(tip))
         return
    client.loop.create_task(tasks[command[0]].execute(command, message))


client.run(token)
