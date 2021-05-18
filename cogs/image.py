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
        print("username: " + username)
        filename = "tempfiles/" + username
        print("filename: " + filename)
        await ctx.message.attachments[0].save(filename)
        print("saved file!")
        im1 = Image.open(filename)
        im2 = Image.open("photos/utility/RAREDRAKEOVERLAY.png")
        print("images opened")
        backup1 = im1.copy()
        backup2 = im2.copy()
        newsize = (470, 608)
        backup1 = backup1.resize(newsize)
        print("resizing")
        backup1.paste(backup2, (0, 0), backup2)
        rarified_filename = filename + "final.png"
        backup1.save(rarified_filename)
        with open(rarified_filename, 'rb') as f:
            picture = discord.File(f)
            await ctx.channel.send(content="Your rarified image", file=picture)
        os.remove(filename)
        os.remove(rarified_filename)
        print("removing the temp files")


def setup(client):
    client.add_cog(BasedImaging(client))
