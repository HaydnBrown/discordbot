import discord
from discord.ext import commands
import os
import random
import dircache

class peterClips(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def peterclip(self, ctx, clip):
        await ctx.send('clip to play: ' + clip)


def setup(client):
    client.add_cog(peterClips(client))