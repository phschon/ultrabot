# UltraBot - yet another discord bot

A simple, extensible and lightweight discord bot written in Python. Control the bot using `!<command>` or `!help <command>` from any discord server's channel the bot is connected to or sending a private message.


## Modules

The `modules` folder contains all available modules for the bot. Each module must contain a class with the exact name as the file name (except the first letter in a class' name, which is still uppercase) and inherit the `metamodule.py`. The file name must only contain digits and characters (see TODO).

At the moment the following functionalities are avaibalbe:
* `random`: generate pseudo-random numbers in the form of pen&paper die throws
* `test`: debug and testing purpose only, showing debug output on console. Also works with multiple channels on multiple servers. To remove this from a running bot, delete the occurrences in lines 7, 13 and 16 in `ultrabot.py`

## TODO

* (fix) music player - WIP
* post pictures from specific sources in regular intervals
* moderation functionality for image posts
* support arbitrary module names (not only digits and letters)


## Notes

* `metamodule.py` is the base class which all modules must inherit. It specifies methods that are needed by the bot and must be implemented.
* `template.py` shows sample code for creating new functionalities. Adapt line 10, 14, 16-19, 44, the execute function and the file name for the individual purpose
* In order to deploy the bot, you will need to register it using your discord account. More infos: https://discordapp.com/developers/docs/topics/oauth2


## Dependencies

* **Python3.4+**
* [discord.py](https://github.com/Rapptz/discord.py) library
* `asyncio` library


You can install the dependencies with pip using

```
pip install -r requirements.txt
```
