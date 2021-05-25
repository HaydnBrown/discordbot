import discord
from discord.ext import commands
import os
import random
from PIL import Image


class BasedImaging(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rarify(self, ctx):
        username = ctx.message.author.name
        filename = "tempfiles/" + username
        await ctx.message.attachments[0].save(filename)
        im1 = Image.open(filename)
        im2 = Image.open("photos/utility/RAREDRAKEOVERLAY.png")
        backup1 = im1.copy()
        backup2 = im2.copy()
        newsize = (470, 608)
        backup1 = backup1.resize(newsize)
        backup1.paste(backup2, (0, 0), backup2)
        rarified_filename = filename + "finalrare.png"
        backup1.save(rarified_filename)
        with open(rarified_filename, 'rb') as f:
            picture = discord.File(f)
            await ctx.channel.send(content="Your rarified image", file=picture)
        os.remove(filename)
        os.remove(rarified_filename)

    @commands.command()
    async def peterrip(self, ctx):
        username = ctx.message.author.name
        filename = "tempfiles/" + username
        await ctx.message.attachments[0].save(filename)
        im1 = Image.open(filename).convert('L')
        im2 = Image.open("photos/utility/peterrip.jpeg").convert('RGBA')
        backup1 = im1.copy()
        backup2 = im2.copy()
        newsize = (225, 276)
        backup1 = backup1.resize(newsize)
        backup2.paste(backup1, (113, 250))
        rip_filename = filename + "finalrip.png"
        backup2.save(rip_filename)
        with open(rip_filename, 'rb') as f:
            picture = discord.File(f)
            await ctx.channel.send(file=picture)
        os.remove(filename)
        os.remove(rip_filename)


def setup(client):
    client.add_cog(BasedImaging(client))
