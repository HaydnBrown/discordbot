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
        await ctx.channel.purge(limit=amount)


def setup(client):
    client.add_cog(Utils(client))
