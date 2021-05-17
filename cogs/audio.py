import discord
from discord.ext import commands
import youtube_dl
import os
import random


class Audio(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def stop(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            voice.stop()
        else:
            await ctx.send("Music not playing, failed to stop")


def setup(client):
    client.add_cog(Audio(client))
