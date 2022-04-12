import discord
from discord.ext import commands


class Utils(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events use @commands.Cog.listener()

    @commands.command()
    async def based(self, ctx):
        await ctx.send('thank u based god')

    @commands.command()
    async def clear(self, ctx, amount=1):
        if amount > 50:
            amount = 50
        await ctx.channel.purge(limit=amount)

    @commands.command()
    async def atme(self, ctx):
        myid = ctx.message.author.mention
        print("user mention: " + myid)
        await ctx.send(myid + " hello!")

    @commands.command()
    async def myname(self, ctx):
        await ctx.send(ctx.author.name)

    @commands.command()
    async def myid(self, ctx):
        await ctx.send(ctx.author.id)

def setup(client):
    client.add_cog(Utils(client))
