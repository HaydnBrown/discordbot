import discord
from discord.ext import commands
import os
import random


class Drake(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rngDrake(self, ctx):
        randomInt = random.randrange(0, 1000)
        if (randomInt == 1):
            fileNameRare = random.choice(os.listdir("photos/rareDrake"))
            fullPathRare = "photos/Drake/" + fileNameRare
            with open(fullPathRare, 'rb') as f:
                picture = discord.File(f)
                await ctx.channel.send(content="YOUR RARE DRAKE PHOTOGRAPH", file=picture)
        else:
            fileName = random.choice(os.listdir("photos/Drake"))
            fullPath = "photos/Drake/" + fileName
            print(fullPath)
            with open(fullPath, 'rb') as f:
                picture = discord.File(f)
                await ctx.channel.send(content="your random drake pic", file=picture)


def setup(client):
    client.add_cog(Drake(client))