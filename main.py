import discord
from discord.ext import commands

import downloader as dwn

import random

import glob

from sys import argv

MUSIC_DIR = "music/"

command_prefix='.'

intents = discord.Intents().all()
intents.message_content = True
intents.voice_states = True
#client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix=command_prefix,intents=intents)

@bot.command(
    name='play',
    description='Plays music, duh....',
    pass_context=True,
)
async def play(context, path):
    # grab the user who sent the command
    user=context.message.author
    voice_channel=user.voice.channel
    channel=None
    # only play music if user is in a voice channel
    if voice_channel!= None:
        # grab user's voice channel
        channel=voice_channel.name
        await context.send('User is in channel: '+ channel)
        # create StreamPlayer
        vc= await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio(MUSIC_DIR+path, executable="ffmpeg/ffmpeg"), after=lambda e: vc.stop())
        # disconnect after the player has finished
        #TODO: 
        
    else:
        await context.send('User is not in a channel.')

@bot.command(name="playlist", pass_context=True)
async def play_playlist(context, dir):    
    # grab the user who sent the command
    user=context.message.author
    voice_channel=user.voice.channel
    channel=None
    # only play music if user is in a voice channel
    if voice_channel!= None:
        # grab user's voice channel
        channel=voice_channel.name
        await context.send('User is in channel: '+ channel)
        # create StreamPlayer
        vc= await voice_channel.connect()
        
        files = glob.glob(MUSIC_DIR+dir+"/*")
        await context.send(files)
        for file in files:
            vc.play(discord.FFmpegPCMAudio(file, executable="ffmpeg/ffmpeg"), after=lambda e: vc.stop())

        # disconnect after the player has finished
        #TODO: 
        
    else:
        await context.send('User is not in a channel.')

@bot.command(name="dc", pass_context=True)
async def disconnect(context):
    vc = discord.utils.get(bot.voice_clients, guild=context.guild)
    if vc == None:
        await context.send('User is not in a channel.')
    else:
        await vc.disconnect()


@bot.command(name="addsong", pass_context=True)
async def add_song(context, url, name):
    log = dwn.DownloadVidYT(url=url, save_dir=MUSIC_DIR, filename=name)
    await context.send(log)

@bot.command(name="addplaylist", pass_context=True)
async def add_playlist(context, url, name):
    dwn.DownloadMusicPlaylistSpotify(url, MUSIC_DIR+name)

@bot.command(name="fortune_cookie", pass_context=True)
async def fortune_cookie(context):
    sample_space = [
        "Your mom is a hoe",
        "Yo mama so fat she is blocking the transference signal",
        "Yo mama so fat, when she sits in the theater, she sits next to everyone",
        "You are nearing your end, read metamorphosis to live your life to the fullest",
        "You are about to have an NTR experience",
        "Einstein did not die so that you could discombobulate his theories with your stupidity",
        "Even Noah did not have to carry this many animals",
        "I'll frame your nuts on the wall(Wallframe deez nuts->warframe)",
        "Imagine being a Titan main, like those people dont exist. Wait a minute, gay people exist",
        "Habibi, stop playing",
        "Trust me lil bro, you aint getting a girlfriend or a girl friend ever. :sob:",
        "Habibi, its time to make your life useful and go to the towers again!",
        "Ye hmar, you so dumb you bring disgrace to the hmar"
    ]

    await context.send(random.choice(sample_space))

@bot.command(pass_contest=True)
async def mbot_help(context):
    await context.send(
        f"{command_prefix}help -> to display all commands\n"+
        f"{command_prefix}play <song-name> -> to play the song\n"+
        f"{command_prefix}dc -> to kick the bot out of voice channel\n"+
        f"{command_prefix}addsong <yt-url> <song-name-to-be-saved> -> adds the song to the library\n"+
        f"{command_prefix}addplaylist <spotify-url> <playlist-name> -> adds playlist to the library\n"+
        f"{command_prefix}playlist"+
        f"{command_prefix}fortune_cookie -> gives out fotune cookie\n"+
        "!!!Please be advised, the bot logs messages on the server for moderation purposes!!!\n"+
        "launch with --noglog to disable logging"
    )

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Unknown command, type {command_prefix}mbot_help for assistance")

@bot.event
async def on_member_join(member):
    await member.send('Please be advised, the bot logs mesages on the server for moderation purposes.')

@bot.event
async def on_message(message):
    no_log = "--nolog"
    if not no_log in argv:
        with open("msglog.txt", "a") as msglog:
            msglog.write(f"name = {message.author.name}, id = {message.author.id}, time = {message.created_at}, guild = {message.guild}: {message.content}\n")
    await bot.process_commands(message)



def main():
    token = input("TOKEN: ")
    bot.run(token)
    

if __name__ == "__main__":
    main()