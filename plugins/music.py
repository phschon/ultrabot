import discord
import asyncio
import metamodule
import copy
import re

class Music_wrapper:
    def __init__(self, player, message, url):
        self.player = player
        self.message = player.title
        self.channel = message.channel
        self.url = url

    def __str__(self):
        return self.message



class Music(metamodule.Meta):
    def __init__(self, client):
        self.client = client
        self.helpstr = '''Supported commands:
        - `join`: Bot joins your current voice channel
        - `join <channel>`: Bot joins voice <channel>
        - `add <url>`: Inserts <url> to queue
        - `pause`: Pauses the current song
        - `resume`: Resumes the current song
        - `play <url>`: Instantly plays <url>, resumes playing the queue if no url is given
        - `playing`: Shows the name of the current song
        - `stop`: Stops playing, but keeps queue
        - `list`: shows all songs in the queue
        - `skip`: skips the current song
        - `disconnect`: Bot disconnects from the voice channel and deletes the queue
        - `shut up` or `clear`: Stops playing and deletes the queue
        - `volume <vol>`: Sets volume to <vol>'''
        # check if bot is connected to a voice channel
        self.voice = None
        self.s_list = asyncio.Queue()
        self.current_song = None
        self.volume = 0.2
        self.wait_for_song = asyncio.Event()
        self.play_songs = self.client.loop.create_task(self.exec_playlist())
        self.command = 'music'

    def get_command(self):
        return self.command


    def is_url(self, url):
        regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return regex.match(url)
        pass


    
    async def play(self, message, url = None):
        if url:
            if not self.is_url(url):
                await self.client.send_message(message.channel, 'Not a valid URL.')
                return

            if self.voice == None:
                await self.summon_channel(message.author.voice_channel, message.channel)

            player = await self.voice.create_ytdl_player(url, after=self.play_next)
            player.volume = self.volume
            if self.current_song:
                self.current_song.player.pause()
                self.current_song = Music_wrapper(player, message, url)
                self.current_song.player.start()
                await self.client.send_message(self.current_song.channel, 'Now playing song: `{}`'.format(self.current_song.message))
                return
            else:
                await self.s_list.put(Music_wrapper(player, message, url))
                return

        if self.current_song == None:
            await self.client.send_message(message.channel, 'Nothing in the queue to play.')
            return

        try:
            self.current_song.player.start()
        except RuntimeError:
            self.current_song.player.resume()


    

    def play_next(self):
        self.client.loop.call_soon_threadsafe(self.wait_for_song.set)


    async def exec_playlist(self):
        while True:
            self.wait_for_song.clear()
            self.current_song = await self.s_list.get()
            await self.client.send_message(self.current_song.channel, 'Now playing song: `{}`'.format(self.current_song.message))
            self.current_song.player.volume = self.volume
            self.current_song.player.start()
            await self.wait_for_song.wait()
            self.current_song = None
            





    # join channel of user calling for bot
    async def summon_channel(self, v_channel, t_channel):
        if v_channel == None:
            await self.client.send_message(t_channel, 'You are not in a voice channel.')
            return False
        if self.voice == None:
            self.voice = await self.client.join_voice_channel(v_channel)
        else:
            await self.voice.move_to(v_channel)
            
        await self.client.send_message(t_channel, 'Joining channel `{}`. Ready to play some music'.format(v_channel))
        return True





    # join specific channel given by user
    async def join_channel(self, v_channel, t_channel):
        channels = t_channel.server.channels
        chan = None
        for x in channels:
            if x.name.startswith(v_channel) and x.type == discord.ChannelType.voice:
                chan = x
                break

        if chan == None:
            await self.client.send_message(t_channel, '`{}` is not a voice channel.'.format(v_channel))
            return False
        if self.voice == None:
            self.voice = await self.client.join_voice_channel(chan)
        else:
            await self.voice.move_to(chan)
        
        await self.client.send_message(t_channel, 'Joining channel `{}`. Ready to play some music'.format(chan.name))

        return True



    async def add(self, message, url):
        if not self.is_url(url):
            await self.client.send_message(message.channel, 'Not a valid URL.')
            return

        print(url)
        if self.voice == None:
            await self.summon_channel(message.author.voice_channel, message.channel)

        player = await self.voice.create_ytdl_player(url, after=self.play_next)
        player.volume = self.volume
        await self.s_list.put(Music_wrapper(player, message, url))
        print(self.s_list.qsize())




    async def list(self, t_channel):
        # TODO
        add = 0
        if not self.current_song == None:
            add = 1
        await self.client.send_message(t_channel, 'Currently {} song(s) in the queue'.format(self.s_list.qsize() + add))
        # await self.client.send_message(t_channel, '(Deprecated!) Songs in the queue:')
        # for i in self.s_list:
        #     await self.client.send_message(t_channel, i.message)






    async def pause(self, message):
        if self.current_song == None:
            await self.client.send_message(message.channel, 'Nothing playing.')
            return

        self.current_song.player.pause()



    async def clear(self, message):
        self.s_list = asyncio.Queue()
        self.current_song.player.stop()
        self.current_song = None




    async def stop(self, message):
        # TODO this is bad!!! do not download again, but copy object
        if self.current_song == None:
            await self.client.send_message(message.channel, 'Nothing playing.')
            return

        self.current_song.player.pause()
        player = await self.voice.create_ytdl_player(self.current_song.url, after=self.play_next)
        player.volume = self.volume
        self.current_song = Music_wrapper(player, message, self.current_song.url)
        # self.current_song = copy.deepcopy(self.current_song)








    async def resume(self, message):
        if self.current_song == None:
            await self.client.send_message(message.channel, 'Nothing playing.')
            return

        try:
            self.current_song.player.start()
        except:
            self.current_song.player.resume()



    async def set_volume(self, message, vol):
        if self.current_song == None:
            await self.client.send_message(message.channel, 'I am not playing anything, dude!.'.format(vol))
            return

        self.current_song.player.volume = int(vol) / 100
        self.volume = int(vol) / 100
        await self.client.send_message(message.channel, 'Volume set so {}%.'.format(vol))



    
    async def skip(self, message):
        if self.current_song == None:
            await self.client.send_message(message.channel, 'I am not playing anything, dude!.'.format(vol))
            return

        self.current_song.player.stop()


    async def playing(self, message):
        if self.current_song:
            await self.client.send_message(message.channel, 'Currently playing: `{}`'.format(self.current_song.message))
        else:
            await self.client.send_message(message.channel, 'Nothing playing.')






    async def execute(self, command, message):
        # handle wrong number of arguments
        if not len(command) > 0:
            await self.client.send_message(message.channel, 'Wrong number of arguments. {}'.format(self.helpstr))
            return
        # display help string
        elif command[0] == 'help':
            await self.help(message)
            return

        # summon bot to current voice channel (current = voice channel of message's author)
        if command[0] == 'join' and len(command) == 1:
            v_chan = message.author.voice_channel
            await self.summon_channel(v_chan, message.channel)
        # summon bot to specific voice channel
        elif command[0] == 'join' and len(command) == 2:
            v_chan = command[1]
            await self.join_channel(v_chan, message.channel)
        elif command[0] == 'add' and len(command) == 2:
            await self.add(message, command[1])
        elif command[0] == 'resume':
            await self.resume(message)
        elif command[0] == 'pause':
            await self.pause(message)
        elif command[0] == 'stop':
            await self.stop(message)
        elif command[0] == 'list':
            await self.list(message.channel)
        elif command[0] == 'play' and len(command) == 1:
            await self.play(message)
        elif command[0] == 'play' and len(command) == 2:
            await self.play(message, command[1])
        elif command[0] == 'skip':
            await self.skip(message)
        elif command[0] == 'shut' and command[1] == 'up':
            await self.clear(message)
        elif command[0] == 'clear':
            await self.clear(message)
        elif command[0] == 'playing':
            await self.playing(message)
        elif command[0] == 'disconnect':
            if not self.voice == None:
                self.s_list = asyncio.Queue
                self.current_song = None
                await self.voice.disconnect()
                # self.voice = None
            else:
                await self.client.send_message(message.channel, 'No connected to any voice channel.')
        elif command[0] == 'volume' and len(command) == 2:
            await self.set_volume(message, command[1])
        else:
            await self.client.send_message(message.channel, 'Wrong usage of music player. {}'.format(self.helpstr))


    async def help(self, message):
        await self.client.send_message(message.channel, '`Music player` - Play Music!.\n\n{}'.format(self.helpstr))
