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
        await ctx.send(os.listdir("C:\Users\12893\PycharmProjects\discordbot\photos\Drake"))



def setup(client):
    client.add_cog(Drake(client))