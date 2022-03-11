import discord
from discord.ext import commands
import os
import random
from PIL import Image, ImageEnhance


class BasedImaging(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rarify(self, ctx):
        username = ctx.message.author.name
        filename = "tempfiles/" + username + "rarify"
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
        filename = "tempfiles/" + username + "peterrip"
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

    @commands.command()
    async def rip(self, ctx, user: discord.User):
        username = user.name
        filename = "tempfiles/" + username + "userrip"
        await user.avatar_url_as(format='png').save(filename)
        im1 = Image.open(filename).convert('L')
        im2 = Image.open("photos/utility/peterrip.jpeg").convert('RGBA')
        backup1 = im1.copy()
        backup2 = im2.copy()
        newsize = (225, 276)
        backup1 = backup1.resize(newsize)
        backup2.paste(backup1, (113, 250))
        rip_filename = filename + "finalripuser.png"
        backup2.save(rip_filename)
        with open(rip_filename, 'rb') as f:
            picture = discord.File(f)
            await ctx.channel.send(file=picture)
        os.remove(filename)
        os.remove(rip_filename)

    @commands.command()
    async def enhancesharpness(self, ctx, factor: int):
        username = ctx.message.author.name
        filename = "tempfiles/" + username + "sharpen"
        await ctx.message.attachments[0].save(filename)
        im1 = Image.open(filename)
        backup1 = im1.copy()
        enhancer = ImageEnhance.Sharpness(backup1)
        backup1 = enhancer.enhance((factor * 30.0))
        enhance_filename = filename + "enhancefinalsharpness.png"
        backup1.save(enhance_filename)
        with open(enhance_filename, 'rb') as f:
            picture = discord.File(f)
            await ctx.channel.send(file=picture)
        os.remove(filename)
        os.remove(enhance_filename)

    @commands.command()
    async def enhancecolor(self, ctx, factor: int):
        username = ctx.message.author.name
        filename = "tempfiles/" + username + "color"
        await ctx.message.attachments[0].save(filename)
        im1 = Image.open(filename)
        backup1 = im1.copy()
        enhancer = ImageEnhance.Color(backup1)
        backup1 = enhancer.enhance((factor * 3.0))
        enhance_filename = filename + "enhancefinalcolor.png"
        backup1.save(enhance_filename)
        with open(enhance_filename, 'rb') as f:
            picture = discord.File(f)
            await ctx.channel.send(file=picture)
        os.remove(filename)
        os.remove(enhance_filename)

    @commands.command()
    async def enhancecontrast(self, ctx, factor: int):
        username = ctx.message.author.name
        filename = "tempfiles/" + username + "contrast"
        await ctx.message.attachments[0].save(filename)
        im1 = Image.open(filename)
        backup1 = im1.copy()
        enhancer = ImageEnhance.Contrast(backup1)
        backup1 = enhancer.enhance((factor * 4.0))
        enhance_filename = filename + "enhancefinalcontrast.png"
        backup1.save(enhance_filename)
        with open(enhance_filename, 'rb') as f:
            picture = discord.File(f)
            await ctx.channel.send(file=picture)
        os.remove(filename)
        os.remove(enhance_filename)

    @commands.command()
    async def enhancebrightness(self, ctx, factor: int):
        username = ctx.message.author.name
        filename = "tempfiles/" + username + "brightness"
        await ctx.message.attachments[0].save(filename)
        im1 = Image.open(filename)
        backup1 = im1.copy()
        enhancer = ImageEnhance.Brightness(backup1)
        backup1 = enhancer.enhance((factor * 2.0))
        enhance_filename = filename + "enhancefinalbrightness.png"
        backup1.save(enhance_filename)
        with open(enhance_filename, 'rb') as f:
            picture = discord.File(f)
            await ctx.channel.send(file=picture)
        os.remove(filename)
        os.remove(enhance_filename)

    @commands.command()
    async def fallon(self, ctx):
        username = ctx.message.author.name
        filename = "tempfiles/" + username + "fallon"
        await ctx.message.attachments[0].save(filename)
        im1 = Image.open(filename)
        im2 = Image.open("photos/utility/fallon.jpg")
        backup1 = im1.copy()
        backup2 = im2.copy()
        newsize = (521, 461)
        backup1 = backup1.resize(newsize)
        backup2.paste(backup1, (119, 364))
        fallon_filename = filename + "finalfallon.png"
        backup2.save(fallon_filename)
        with open(fallon_filename, 'rb') as f:
            picture = discord.File(f)
            await ctx.channel.send(file=picture)
        os.remove(filename)
        os.remove(fallon_filename)

    @commands.command()
    async def zamn(self, ctx):
        username = ctx.message.author.name
        filename = "tempfiles/" + username + "zamn"
        await ctx.message.attachments[0].save(filename)
        im1 = Image.open(filename)
        im2 = Image.open("photos/utility/ZAMN.png")
        backup1 = im1.copy()
        backup2 = im2.copy()
        newsize = (319, 509)
        backup1 = backup1.resize(newsize)
        backup2.paste(backup1, (296, 1))
        fallon_filename = filename + "finalzamn.png"
        backup2.save(fallon_filename)
        with open(fallon_filename, 'rb') as f:
            picture = discord.File(f)
            await ctx.channel.send(file=picture)
        os.remove(filename)
        os.remove(fallon_filename)

    @commands.command()
    async def bidness(self, ctx):
        username = ctx.message.author.name
        filename = "tempfiles/" + username + "bidness"
        await ctx.message.attachments[0].save(filename)
        im1 = Image.open(filename)
        im2 = Image.open("photos/utility/blank_bidness.png")
        backup1 = im1.copy()
        backup2 = im2.copy()
        newsize = (262, 353)
        backup1 = backup1.resize(newsize)
        backup2.paste(backup1, (74, 268))
        fallon_filename = filename + "finalbidness.png"
        backup2.save(fallon_filename)
        with open(fallon_filename, 'rb') as f:
            picture = discord.File(f)
            await ctx.channel.send(file=picture)
        os.remove(filename)
        os.remove(fallon_filename)

    @commands.command()
    async def ericandre(self, ctx):
        username = ctx.message.author.name
        filename = "tempfiles/" + username + "ericandre"
        await ctx.message.attachments[0].save(filename)
        im1 = Image.open(filename)
        im2 = Image.open("photos/utility/blank_ericandre.png")
        backup1 = im1.copy()
        backup2 = im2.copy()
        newsize = (140, 165)
        backup1 = backup1.resize(newsize)
        backup2.paste(backup1, (360, 80))
        fallon_filename = filename + "finalericandre.png"
        backup2.save(fallon_filename)
        with open(fallon_filename, 'rb') as f:
            picture = discord.File(f)
            await ctx.channel.send(file=picture)
        os.remove(filename)
        os.remove(fallon_filename)

    @commands.command()
    async def pray(self, ctx):
        with open("photos/utility/angel-jerma.png", 'rb') as f:
            picture = discord.File(f)
            await ctx.channel.send(file=picture)
        print("sent angel-jerma")

    @commands.command()
    async def truegif(self, ctx):
        with open("photos/utility/thatstrue.gif", 'rb') as f:
            picture = discord.File(f)
            await ctx.channel.send(file=picture)
        print("sent thats-true gif")


def setup(client):
    client.add_cog(BasedImaging(client))
