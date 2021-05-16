import discord
from discord.ext import commands
import os
import random


class Drake(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rngDrake(self, ctx):
        with open(random.choice(os.listdir("photos/Drake")), 'rb') as f:
            picture = discord.File(f)
            await ctx.send(file=picture)


def setup(client):
    client.add_cog(Drake(client))