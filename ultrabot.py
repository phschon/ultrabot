import discord
import asyncio
import os
import re
import sys
import importlib
import metamodule

with open('token', 'r') as f:
    token = f.readline()[:-1]

client = discord.Client()
# dict with all available functions and objects of all supported functionality
# tasks = {'test' : testfunc.Testfunc(client), 'random' : randomgen.Randomgen(client), 'music' : play_music.Music(client)}
tasks = {}

tip = 'Available commands: `!list`,'

# load all valid modules from the modules subfolder
pysearchre = re.compile('.py$', re.IGNORECASE)
modfiles = filter(pysearchre.search,os.listdir(os.path.join(os.path.dirname(__file__),'modules')))
form_module = lambda fp: '.' + os.path.splitext(fp)[0]
mods = map(form_module, modfiles)
importlib.import_module('modules')
for mod in mods:
    if not mod.startswith('.__'):
        p = importlib.import_module(mod, package="modules")
        main_class = getattr(p, mod[1:].title())
        instance = main_class(client)
        if isinstance(instance, metamodule.Meta):
            name = instance.get_command()
            print(name + " created")
            tasks[name] = instance
            tip = tip + ' `!' + name + '`,'


# strip the trailing ','
tip = tip[:-1]

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

    if command[0] == 'help' and not len(command) == 2:
        await client.send_message(message.channel, 'Please specify one command. {}'.format(tip))
        return

    if command[0] == 'help':
        print(command)
        print(tasks)
        if command[1] in tasks:
            await tasks[command[1]].help(message)
            return
        else:
            await client.send_message(message.channel, 'Command not supported. {}'.format(tip))
            return

    # if command is not in dict, print help string and list of available commands
    if not command[0] in tasks:
         await client.send_message(message.channel, 'Command not supported. {}'.format(tip))
         return
    # command is in dict, forward command and parameters, as well as the entire message, to functionality object
    com = command.pop(0)
    client.loop.create_task(tasks[com].execute(command, message))


client.run(token)
