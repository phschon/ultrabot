import discord
import asyncio

class Music_wrapper:
    def __init__(self, player, message):
        self.player = player
        self.message = message

    def __str__(self):
        return self.message



class Music:
    def __init__(self, client):
        print('music created')
        self.client = client
        self.helpstr = '''Supported commands:
        - `join`: Bot joins your current voice channel
        - `join <channel>`: Bot joins voice <channel>
        - `add <url>`: Inserts <url> to queue
        - `pause`: Pauses the current song
        - `resume`: Resumes the current song
        - `stop`: Stops playing
        - `disconnect`: Bot disconnects from the voice channel
        - `shut up`: Bot disconnects from the voice channel and deletes queue
        - `volume <vol>`: Sets volume to <vol>'''
        # check if bot is connected to a voice channel
        self.voice = None
        self.s_list = asyncio.Queue()
        self.current_song = None
        self.volume = 0.5
        self.wait_for_song = asyncio.Event()
        self.play_songs = self.client.loop.create_task(self.exec_playlist())


    
    def play(self):
        self.play_songs = self.client.loop.create_task(self.exec_playlist())


    

    def play_next(self):
        self.client.loop.call_soon_threadsafe(self.wait_for_song.set)


    async def exec_playlist(self):
        print('exec playlist entered')
        while True:
            print('next song')
            self.wait_for_song.clear()
            self.current_song = await self.s_list.get()
            # TODO: await self.client.send_message(t_channel, 'You are not in a voice channel.')
            self.current_song.player.volume = self.volume
            self.current_song.player.start()
            await self.wait_for_song.wait()
            print('end of loop')
            





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



    async def add(self, message, song):
        print(song)
        if self.voice == None:
            if not await self.summon_channel(message.author.voice_channel, message.channel):
                return

        player = await self.voice.create_ytdl_player(song, after=self.play_next())
        player.volume = self.volume
        # TODO: extract song name
        self.s_list.put(Music_wrapper(player, message))
        print(self.s_list.qsize())




        # self.voice.songs.put(song)
        # self.player.start()
        # TODO: adjust volume at the beginning of each song



    async def list(self, t_channel):
        await self.client.send_message(t_channel, self.s_list.qsize())
        # await self.client.send_message(t_channel, '(Deprecated!) Songs in the queue:')
        # for i in self.s_list:
        #     await self.client.send_message(t_channel, i.message)






    async def pause(self, message):
        if self.current_song == None:
            await self.client.send_message(message.channel, 'Nothing playing.')
            return

        self.current_song.player.pause()






    async def stop(self, message):
        if self.current_song == None:
            await self.client.send_message(message.channel, 'Nothing playing.')
            return

        self.current_song.player.stop()








    async def resume(self, message):
        if self.current_song == None:
            await self.client.send_message(message.channel, 'Nothing playing.')
            return

        self.current_song.player.resume()



    async def volume(self, message, vol):
        if self.current_song == None:
            await self.client.send_message(message.channel, 'I am not playing anything, dude!.'.format(vol))
            return

        self.current_song.player.volume = int(vol) / 100
        self.volume = int(vol) / 100
        await self.client.send_message(message.channel, 'Volume set so {}%.'.format(vol))



    
    async def skip(self):
        if self.current_song == None:
            await self.client.send_message(message.channel, 'I am not playing anything, dude!.'.format(vol))
            return

        self.current_song.player.stop()







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
        elif command[0] == 'play':
            # await self.play()
            pass
        elif command[0] == 'skip':
            # await self.skip(self)
            pass
        elif command[0] == 'disconnect':
            if not self.voice == None:
                await self.voice.disconnect()
                self.voice = None
            else:
                await self.client.send_message(message.channel, 'No connected to any voice channel.')
        elif command[0] == 'shut' and command[1] == 'up':
            if not self.voice == None:
                await self.voice.disconnect()
                self.voice = None
        elif command[0] == 'volume' and len(command) == 2:
            await self.volume(message, command[1])
        else:
            await self.client.send_message(message.channel, 'Wrong usage of music player. {}'.format(self.helpstr))


    async def help(self, message):
        await self.client.send_message(message.channel, '`Music player` - Play Music!.\n\n{}'.format(self.helpstr))
