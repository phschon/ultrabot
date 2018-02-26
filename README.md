# UltraBot - yet another discord bot

A simple, extensible and lightweight discord bot written in Python. Control the bot using `!<command>` or `!help <command>` from any server's channel the bot is connected to or sending a private message.


## Overwiew

Supports the following functionalities:
* `ultrabot.py`: basic bot, connects to server and handles agrument parsing
* `helpfunc.py`: handles `!help` command for each other functionality
* `randomgen.py`: generate pseudo-random numbers in the form of pen&paper die throws
* `testfunc.py`: debug and testing purpose only, showing debug output on console. Also works with multiple channels on multiple servers. To remove this from a running bot, delete the occurrences in lines 7, 13 and 16 in `ultrabot.py` 


## TODO

* (fix) music player - WIP
* post pictures from specific sources in regular intervals
* moderation functionality for image posts


## Notes

* `template.py` contains the base code for creating new functionalities. Adapt line 8, 12, 35 and the execute function for the individual purpose
* In order to deploy the bot, you will need to register it using your discord account. More infos: https://discordapp.com/developers/docs/topics/oauth2


## Dependencies

* [discord.py](https://github.com/Rapptz/discord.py) library
* Python3.4+
* `asyncio` library
