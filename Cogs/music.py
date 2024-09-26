import discord
from discord.ext import commands
import os
import glob

import Cogs.downloader as dwn

import random

MUSIC_DIR = "music/"


def GetFFMPEGPath():
    with open("ffmpegpath", "r") as pathfile:
        path = pathfile.read()
    return path

FFMPEGPath = GetFFMPEGPath()
class MusicCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='Play',
        pass_context=True,
    )
    async def play(self, context, path):
        if not os.path.isfile(MUSIC_DIR+path):
            await context.send("No music file found!")
            return

        # grab the user who sent the command
        user=context.message.author
        voice_channel=user.voice.channel
        # only play music if user is in a voice channel
        if voice_channel!= None:
            # grab user's voice channel
            channel=voice_channel.name
            await context.send('User is in channel: '+ channel)
            # create StreamPlayer
            vc= await voice_channel.connect()
            await context.send(f"Playing {MUSIC_DIR+path}")
            vc.play(discord.FFmpegPCMAudio(MUSIC_DIR+path, executable=FFMPEGPath), after=lambda e: vc.stop())
            # disconnect after the player has finished
            #TODO: 
            
        else:
            await context.send('User is not in a channel.')

    @commands.command(name="AddSong", pass_context=True)
    async def add_song(self, context, url, name):
        log = dwn.DownloadAudioYT(url=url, save_dir=MUSIC_DIR, filename=name)
        await context.send(log)

    @commands.command(name="CreatePlaylist")
    async def CreatePlaylist(context,url, name):
        if os.path.isdir(MUSIC_DIR+name):
            files=glob.glob(MUSIC_DIR+name+"/*")
            msg = "Playlist already exists, contenets are \n"
            for file in files:
                msg = msg + file + "\n"
            await context.send(msg)
        else:
            os.mkdir(MUSIC_DIR+name)
        
        dwn.DownloadYTPlaylist(url, MUSIC_DIR+name)

        files = glob.glob(MUSIC_DIR+name+"/*")

        msg = "Finished downloading playlist, contents are\n"
        for file in files:
            msg = msg + file + "\n"
        
        await context.send(msg)

    def play_next(self, context, song_queue):
        vc = discord.utils.get(self.bot.voice_clients, guild=context.guild)
        if len(song_queue) > 1:
            del song_queue[0]
            vc.play(discord.FFmpegPCMAudio(song_queue[0], executable=FFMPEGPath), after=lambda e: self.play_next(self, context, song_queue))
        else:
            vc.disconnect(context)

    @commands.command(name="StartPlaylist")
    async def start_playlist(self, context, name):   
        if not os.path.isdir(MUSIC_DIR+name):
            await context.send("Playlist does not exist")
            return


        # grab the user who sent the command
        user=context.message.author
        voice_channel=user.voice.channel
        # only play music if user is in a voice channel
        if voice_channel!= None:
            # grab user's voice channel
            channel=voice_channel.name
            await context.send('User is in channel: '+ channel)
            # create StreamPlayer
            vc= await voice_channel.connect()

            files = glob.glob(MUSIC_DIR+name+"/*")
            song_queue = list(files)
            msg = ""
            for file in files:
                msg = msg + file + '\n'
            await context.send(msg)
            for file in files:
                vc.play(discord.FFmpegPCMAudio(file, executable=FFMPEGPath), after=lambda e: self.play_next(context, song_queue))
            # disconnect after the player has finished
            #TODO: 
            


        else:
            await context.send('User is not in a channel.')

    @commands.command(name="ShufflePlaylist")
    async def shuffle_playlist(self, context, name):  
        if not os.path.isdir(MUSIC_DIR+name):
            await context.send("Playlist does not exist")
            return


        # grab the user who sent the command
        user=context.message.author
        voice_channel=user.voice.channel
        # only play music if user is in a voice channel
        if voice_channel!= None:
            # grab user's voice channel
            channel=voice_channel.name
            await context.send('User is in channel: '+ channel)
            # create StreamPlayer
            vc= await voice_channel.connect()

            files = glob.glob(MUSIC_DIR+name+"/*")
            song_queue = list(files)
            random.shuffle(song_queue)
            print(f"Shuffled: {song_queue}")
            msg = ""
            for file in files:
                msg = msg + file + '\n'
            await context.send(msg)
            for file in files:
                vc.play(discord.FFmpegPCMAudio(file, executable=FFMPEGPath), after=lambda e: self.play_next(context, song_queue))
            # disconnect after the player has finished
            #TODO: 
            


        else:
            await context.send('User is not in a channel.')

    @commands.command(name="DisplayPlaylist")
    async def display_playlist(self, context, name):
        if not os.path.isdir(MUSIC_DIR+name):
            context.send("Playlist does not exist")
            return
        files = glob.glob(MUSIC_DIR+name+"/*")
        msg = ""
        for index, fname in enumerate(files):
            msg = msg + f"{index + 1} -> {fname}\n"

        await context.send(msg)

    @commands.command(name="SelectivePlay")
    async def selective_play(self, context, playlist_name, uid): #uid = glob.glob(<playlist-dir>)[uid - 1]

        if not os.path.isdir(MUSIC_DIR+playlist_name):
            await context.send("No playlist found!")
            return
        

        files = glob.glob(MUSIC_DIR+playlist_name+"/*")
        for i in range(len(files)):
            files[i] = files[i].replace("\\", "/")

        index = int(uid) - 1

        if index not in range(len(files)):
            await context.send("Invalid UID for playlist item")
            return

        # grab the user who sent the command
        user=context.message.author
        voice_channel=user.voice.channel
        # only play music if user is in a voice channel
        if voice_channel!= None:
            # grab user's voice channel
            channel=voice_channel.name
            await context.send('User is in channel: '+ channel)
            # create StreamPlayer
            vc= await voice_channel.connect()
            await context.send(files)
            vc.play(discord.FFmpegPCMAudio(files[index], executable=FFMPEGPath), after=lambda e: vc.stop())
            # disconnect after the player has finished
            #TODO: 
            
        else:
            await context.send('User is not in a channel.')

    @commands.command(name="Disconnect")
    async def disconnect(self, context):
        vc = discord.utils.get(self.bot.voice_clients, guild=context.guild)
        if vc == None:
            await context.send('User is not in a channel.')
        else:
            await vc.disconnect()


async def setup(bot):
    await bot.add_cog(MusicCog(bot))
