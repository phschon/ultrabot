# UltraBot - yet another discord bot

A simple, extensible and lightweight discord bot written in Python. Control the bot using `!<command>` or `!help <command>` from any discord server's channel the bot is connected to or sending a private message.


## Modules

The `modules` folder contains all available modules for the bot. Each module must have the `ub-` prefix (for now, see TODO), as well as contain a class with the same name as the file (note the first letter being uppercase). The filename must only contain letters and digits. This class again, must contain the execute method, as can be seen in `template.py`.

At the moment the following functionalities are avaibalbe:
* `help`: handles `!help` command for each other functionality
* `random`: generate pseudo-random numbers in the form of pen&paper die throws
* `testfunc`: debug and testing purpose only, showing debug output on console. Also works with multiple channels on multiple servers. To remove this from a running bot, delete the occurrences in lines 7, 13 and 16 in `ultrabot.py`


## TODO

* (fix) music player - WIP
* post pictures from specific sources in regular intervals
* moderation functionality for image posts
* implement a better module recognition than the `ub-` prefix, to ensure that only proper modules are loaded and not helper classes (such as `testfuncrunner.py`)
* support arbitrary module names (not only digits and letters)


## Notes

* `template.py` contains the base code for creating new functionalities. Adapt line 8, 12, 35 and the execute function for the individual purpose
* In order to deploy the bot, you will need to register it using your discord account. More infos: https://discordapp.com/developers/docs/topics/oauth2


## Dependencies

* **Python3.4+**
* [discord.py](https://github.com/Rapptz/discord.py) library
* `asyncio` library


You can install the dependencies with pip doing

```
pip install -r requirements.txt
```
