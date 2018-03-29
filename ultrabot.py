import discord
import asyncio
import os
import re
import sys
import importlib
import metamodule
from typing import Dict, List, Callable


def load_token() -> str:
    try:
        with open('token', 'r') as f:
            return f.readline().strip()
    except FileNotFoundError:
        print("Missing token file: ./token - see https://discordapp.com/developers/applications/me to register "
              "an application", file=sys.stderr)
        sys.exit(1)

class UltraClient(discord.Client):
    def __init__(self):
        super(UltraClient, self).__init__()
        self.tasks = {}  # type: Dict[str, metamodule.Meta]

        self.on_ready_listeners = []  # type: List[Callable]
        self.on_message_listeners = []  # type: List[Callable[discord.Message]]
        self.on_message_deleted_listeners = []  # type: List[Callable[discord.Message]]
        self.on_message_edited_listeners = []  # type: List[Callable[discord.Message, discord.Message]]
        self.on_reaction_added_listeners = []  # type: List[Callable[discord.Reaction, discord.User]]
        self.on_reaction_removed_listeners = []  # type: List[Callable[discord.Reaction, discord.User]]

        self.register_on_ready(self.print_ready_info)

    def load_plugins(self):
        """ load all valid plugins from the plugins subfolder """
        pysearchre = re.compile('.py$', re.IGNORECASE)
        plugin_path = os.listdir(os.path.join(os.path.dirname(__file__), 'plugins'))
        modfiles = filter(pysearchre.search, plugin_path)
        form_plugin = lambda fp: '.' + os.path.splitext(fp)[0]
        mods = map(form_plugin, modfiles)
        importlib.import_module('plugins')
        for mod in mods:
            if not mod.startswith('.__'):
                p = importlib.import_module(mod, package="plugins")
        for c in metamodule.Meta.__subclasses__():
            instance = c(self)
            print(f"Module loaded: {instance.get_command()}")
            self.tasks[instance.get_command()] = instance

    def get_help_msg(self) -> str:
        commands = ", ".join([f"`!{task}`" for task in self.tasks.keys()])
        return f"""Available commands: `!list`, `!aboutme`, {commands}

        Use `!help <command>` for information about commands.
        """

    async def print_ready_info(self):
        print(f'Logged in as {self.user.name} ({self.user.id})')
        print('------')

    async def log_messages(self, message: discord.Message):
        message_author = f'<{message.author.name}>'
        print(f'[{message.channel.name:>12}/{message.channel.id}] {message_author:<14} {message.content}')

    async def react_to_commands(self, message: discord.Message):
        # otherwise split message and get array with command and arguments
        command = str.split(message.content)
        # remove "!" prefix
        command[0] = command[0][1:]

        # if command is 'list', print avaibalbe commands
        if command[0] == 'list':
            await self.send_message(message.channel, self.get_help_msg())
            return

        if command[0] == 'aboutme':
            await self.send_message(message.channel, 'I am the UltraBot! You can download and support me here: https://github.com/phschon/ultrabot.')
            return

        if command[0] == 'help' and not len(command) == 2:
            await self.send_message(message.channel, f'Please specify one command. {self.get_help_msg()}')
            return

        if command[0] == 'help':
            if command[1] in self.tasks:
                await self.tasks[command[1]].help(message)
                return
            else:
                await self.send_message(message.channel, f'Command not supported. {self.get_help_msg()}')
                return

        # if command is not in dict, print help string and list of available commands
        if not command[0] in self.tasks:
            await self.send_message(message.channel, f'Command not supported. {self.get_help_msg()}')
            return

        # command is in dict, forward command and parameters, as well as the entire message, to functionality object
        com = command.pop(0)
        # check if the number of parameters exceed the ones allowed for the plugin
        max_para = self.tasks[com].get_max_parameters()
        # if the number of parameters exceed the maximum give an error message and send the plugin's help message
        if max_para and len(command) > max_para:
            await self.send_message(message.channel, f'Too many arguments for `!{com}`')
            await self.tasks[com].help(message)
        # run the plugin
        else:
            self.loop.create_task(self.tasks[com].execute(command, message))

    #
    # Event system starts here
    #

    def register_on_ready(self, callback: Callable):
        self.on_ready_listeners.append(callback)

    def unregister_on_ready(self, callback: Callable):
        self.on_ready_listeners.remove(callback)

    async def on_ready(self):
        tasks = [callback() for callback in self.on_ready_listeners]
        for task in tasks:
            await task

    def register_on_message(self, callback: Callable[[discord.Message], None]):
        self.on_message_listeners.append(callback)

    def unregister_on_message(self, callback: Callable[[discord.Message], None]):
        self.on_message_listeners.remove(callback)

    async def on_message(self, message: discord.Message):
        await self.log_messages(message)

        if message.author.id == self.user.id:
            return  # Do not handle echo messages

        if message.content.startswith('!'):
            await self.react_to_commands(message)
        else:
            tasks = [callback(message) for callback in self.on_message_listeners]
            for task in tasks:
                await task

    def register_on_message_deleted(self, callback: Callable[[discord.Message], None]):
        self.on_message_deleted_listeners.append(callback)

    def unregister_on_message_deleted(self, callback: Callable[[discord.Message], None]):
        self.on_message_deleted_listeners.remove(callback)

    async def on_message_delete(self, message: discord.Message):
        tasks = [callback(message) for callback in self.on_message_deleted_listeners]
        for task in tasks:
            await task

    def register_on_message_edited(self, callback: Callable[[discord.Message, discord.Message], None]):
        self.on_message_edited_listeners.append(callback)

    def unregister_on_message_edited(self, callback: Callable[[discord.Message, discord.Message], None]):
        self.on_message_edited_listeners.remove(callback)

    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        tasks = [callback(before, after) for callback in self.on_message_edited_listeners]
        for task in tasks:
            await task

    def register_on_reaction_added(self, callback: Callable[[discord.Reaction, discord.User], None]):
        self.on_reaction_added_listeners.append(callback)

    def unregister_on_reaction_added(self, callback: Callable[[discord.Reaction, discord.User], None]):
        self.on_reaction_added_listeners.remove(callback)

    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        tasks = [callback(reaction, user) for callback in self.on_reaction_added_listeners]
        for task in tasks:
            await task

    def register_on_reaction_removed(self, callback: Callable[[discord.Reaction, discord.User], None]):
        self.on_reaction_removed_listeners.append(callback)

    def unregister_on_reaction_removed(self, callback: Callable[[discord.Reaction, discord.User], None]):
        self.on_reaction_removed_listeners.remove(callback)

    async def on_message_remove(self, reaction: discord.Reaction, user: discord.User):
        tasks = [callback(reaction, user) for callback in self.on_reaction_removed_listeners]
        for task in tasks:
            await task


if __name__ == "__main__":
    client = UltraClient()
    client.load_plugins()
    client.run(load_token())
