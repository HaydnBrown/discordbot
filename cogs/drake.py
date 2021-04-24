import discord
from discord.ext import commands
import os
import random
import dircache

class Drake(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rngDrake(self, ctx):
        await ctx.send("not yet functional")



def setup(client):
    client.add_cog(Drake(client))