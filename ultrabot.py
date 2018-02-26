import discord
import asyncio
import testfunc
import helpfunc
import randomgen
import play_music
import os

with open('token', 'r') as f:
    token = f.readline()[:-1]

client = discord.Client()
# dict with all available functions and objects of all supported functionality
tasks = {'test' : testfunc.Testfunc(client), 'random' : randomgen.Randomgen(client), 'music' : play_music.Music(client)}
tasks['help'] = helpfunc.Helpfunc(client, tasks)

tip = 'Available commands: `!music`,  `!test`, `!random`, `!help`'

# imports and configs if additional files/functionalities are found in folder
if "swag.py" in os.listdir("."):
    import swag
    tasks['swag'] = swag.Swag(client)
    tip = tip + ', `!swag`'

# add the rest of the help string
tip = tip + '''

Use `!help <command>` for information about commands.'''


# debug output on console during startup
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


# main function that is executed when a message is received, look up command in dict and forward parameters
@client.event
async def on_message(message):
    # print debug output
    print(message.channel, message.channel.id, message.content)
    # if message does not start with "!" control character, ignore
    if not message.content.startswith('!'):
        return
    # otherwise split message and get array with command and arguments
    command = str.split(message.content)
    # remove "!" prefix
    command[0] = command[0][1:]

    # if command is 'list', print avaibalbe commands
    if command[0] == 'list':
        await client.send_message(message.channel, tip)
        return

    # if command is not in dict, print help string and list of available commands
    if not command[0] in tasks:
         await client.send_message(message.channel, 'Command not supported. {}'.format(tip))
         return
    # command is in dict, forward command and parameters, as well as the entire message, to functionality object
    client.loop.create_task(tasks[command[0]].execute(command, message))


client.run(token)
