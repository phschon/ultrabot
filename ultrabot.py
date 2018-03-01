import discord
import asyncio
import os
import re
import sys
import importlib
import metamodule
from typing import Dict

TASKS = {}  # type: Dict[str, metamodule.Meta]


def load_token() -> str:
    try:
        with open('token', 'r') as f:
            return f.readline().strip()
    except FileNotFoundError:
        print("Missing token file: ./token - see https://discordapp.com/developers/applications/me to register "
              "an application", file=sys.stderr)
        sys.exit(1)


def get_help_msg() -> str:
    commands = ", ".join([f"`!{task}`" for task in TASKS.keys()])
    return f"""Available commands: `!list`, {commands}
    
    Use `!help <command>` for information about commands.
    """


def load_modules(client: discord.Client):
    """ load all valid modules from the modules subfolder """
    pysearchre = re.compile('.py$', re.IGNORECASE)
    module_path = os.listdir(os.path.join(os.path.dirname(__file__), 'modules'))
    modfiles = filter(pysearchre.search, module_path)
    form_module = lambda fp: '.' + os.path.splitext(fp)[0]
    mods = map(form_module, modfiles)
    importlib.import_module('modules')
    for mod in mods:
        # TODO use dir() to iterate over all classes and check if class inherts Meta
        # -> one module for multiple commands
        if not mod.startswith('.__'):
            p = importlib.import_module(mod, package="modules")
            main_class = getattr(p, mod[1:].title())
            instance = main_class(client)
            if isinstance(instance, metamodule.Meta):
                name = instance.get_command()
                print("Module loaded: " + name)
                TASKS[name] = instance


def run_client():
    client = discord.Client()
    load_modules(client)

    @client.event
    async def on_ready():
        print(f'Logged in as {client.user.name} ({client.user.id})')
        print('------')

    # main function that is executed when a message is received, look up command in dict and forward parameters
    @client.event
    async def on_message(message: discord.Message):
        print(f'[{message.channel.name:>12}/{message.channel.id}] {message.content}')

        # if message does not start with "!" control character, ignore
        if not message.content.startswith('!'):
            return
        # otherwise split message and get array with command and arguments
        command = str.split(message.content)
        # remove "!" prefix
        command[0] = command[0][1:]

        # if command is 'list', print avaibalbe commands
        if command[0] == 'list':
            await client.send_message(message.channel, get_help_msg())
            return

        if command[0] == 'help' and not len(command) == 2:
            await client.send_message(message.channel, f'Please specify one command. {get_help_msg()}')
            return

        if command[0] == 'help':
            print(command)
            print(TASKS)
            if command[1] in TASKS:
                await TASKS[command[1]].help(message)
                return
            else:
                await client.send_message(message.channel, f'Command not supported. {get_help_msg()}')
                return

        # if command is not in dict, print help string and list of available commands
        if not command[0] in TASKS:
            await client.send_message(message.channel, f'Command not supported. {get_help_msg()}')
            return

        # command is in dict, forward command and parameters, as well as the entire message, to functionality object
        com = command.pop(0)
        client.loop.create_task(TASKS[com].execute(command, message))

    client.run(load_token())

if __name__ == "__main__":
    run_client()
