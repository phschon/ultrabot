# UltraBot - yet another discord bot

A simple, extensible and lightweight discord bot written in Python. Control the bot using `!<command>` or `!help <command>` from any discord server's channel the bot is connected to or sending a private message.


## Plugins

The `plugin` folder contains all available plugins for the bot. Each plugin must consist of at least one class inheriting the `metamodule.py` class. This class is treaded as the plugin's "main" class, answering all function calls from the bot. Note that it is possible to provide more than one plugin in the same module.

At the moment the following functionalities are avaibalbe:
* `music`: a music player supporting queueing multiple songs from different users
* `random`: generate pseudo-random numbers in the form of pen&paper die throws
* `howlong`: get game info from [howlongtobeat.com](https://howlongtobeat.com)
* `pr0`: get a random image or video related to any number of tags specified
* `xkcd`: post random, latest or specific xkcd comic
* `reddit`: post a random picture from a subreddit
* `test`: debug and testing purpose only, showing debug output on console. Also works with multiple channels on multiple servers.

## TODO

* post pictures from specific sources in regular intervals
* moderation functionality for image posts
* allow multiple commands for the same plugin (e.g. !pr0 and !pro), maybe list only one in !list

Feel free to open issues for suggestions or contribute your own plugin :)


## Notes

* `metamodule.py` is the base class which all plugins must inherit. It specifies methods that are needed by the bot and must be implemented.
* `template.py` shows sample code for creating new functionalities. Adapt line 10, 14, 16-19, 44 and the execute function for the individual purpose
* In order to deploy the bot, you will need to register it using your discord account. More infos: https://discordapp.com/developers/docs/topics/oauth2. The token needed for the bot is stored in a file named `token` in its the root directory.


## Dependencies

* **Python3.4+**
* [discord.py](https://github.com/Rapptz/discord.py) library
* `asyncio` library
* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) library
* `requests` library


You can install the dependencies with pip using

```
pip install -r requirements.txt
```

## Known Bugs

* `music.py`: The class is not threadsafe. Combinations of parallel commands or function calls may trigger unintended/deprecated behaviour or even crash the bot. A potential fix is coming soon.
