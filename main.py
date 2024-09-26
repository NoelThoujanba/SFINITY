import discord
from discord.ext import commands
import requests

import asyncio

import Cogs.StableDiffusion as StableDiffusion

from sys import argv

command_prefix='.'

intents = discord.Intents().all()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix=command_prefix,intents=intents)

#Note to self: The codebase is getting out of hand. Need to seperate music and ai compontents

IMG_DWN_DIR = "img/dwn/"
IMG_GEN_DIR = "img/gen/"

#why?
@bot.command(pass_context=True)
async def SendImage(context):
    message = context.message
    if len(message.attachments) == 1:
        attachment = message.attachments[0]
        await context.send("Recieved Image")

    if (
        attachment.filename.endswith(".jpg")
        or attachment.filename.endswith(".jpeg")
        or attachment.filename.endswith(".png")
        or attachment.filename.endswith(".webp")
        or attachment.filename.endswith(".gif")
    ):
        img_data = requests.get(attachment.url).content
        with open(f"{IMG_DWN_DIR}/{attachment.filename}", "wb") as handler:
            handler.write(img_data)

    elif (
        "https://images-ext-1.discordapp.net" in message.content
        or "https://tenor.com/view/" in message.content
    ):
        await context.send("Unable to open image!")


@bot.event
async def on_command_error(context, error):
    if isinstance(error, commands.CommandNotFound):
        await context.send(f"Unknown command, type {command_prefix}mbot_help for assistance")

    if ("--debug") in argv:
        print(f'Error: {error}')
        await context.send(f"{error}")


async def main():
    token = input("TOKEN: ")
    async with bot:
        await bot.load_extension("Cogs.music")
        await bot.load_extension("Cogs.StableDiffusion")
        await bot.load_extension("Cogs.ChatBot")
        await bot.start(token)
    

if __name__ == "__main__":
    asyncio.run(main())
