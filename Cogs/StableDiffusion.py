import discord
from discord.ext import commands

from typing import Final

from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler

import functools
import typing
import asyncio

def to_thread(func: typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)
    return wrapper


class StableDiffusionCog(commands.Cog):

    #will add getters and setters for these attributes when I understand what the fuck they do
    __imgGenModel: str = "dreamlike-art/dreamlike-photoreal-2.0"
    __imgWidth: str = 1280
    __imgHeight: str = 720
    __betaStart: str = 0.00085
    __betaEnd: str = 0.012
    __betaScheduled: str = "scaled_linear"
    __numInferenceSteps: int = 30
    __guidanceScale = 7.5
    __imgGenCount: int = 0

    __pipe = None
    __scheduler = None

    SAVE_PAtH: Final[str] = "img/gen/"

    def __init__(self, bot) -> None:
        self.bot = bot

        self.__pipe = StableDiffusionPipeline.from_pretrained(self.__imgGenModel)
        self.__pipe.to("cuda")
        self.__scheduler = EulerDiscreteScheduler(beta_start=self.__betaStart, beta_end=self.__betaEnd, beta_schedule=self.__betaScheduled)
    
    @commands.command(pass_context=True)
    async def GenerateImage(self, context, prompt: str):
        
        image = self.__pipe(
            prompt,
            width=self.__imgWidth,
            height=self.__imgHeight,
            scheduler=self.__scheduler,
            num_inference_steps=self.__numInferenceSteps,
            guidance_scale=self.__guidanceScale,
        ).images[0]
        image.save(f"{self.SAVE_PAtH}{self.__imgGenCount}.png")
        await context.send(file=discord.File(f"{self.SAVE_PAtH}{self.__imgGenCount}.png")) #need to delete the image afterwards
        self.__imgGenCount += 1


async def setup(bot):
    await bot.add_cog(StableDiffusionCog(bot))