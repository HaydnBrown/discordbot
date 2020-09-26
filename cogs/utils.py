import discord
from discord.ext import commands


class Utils(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events use @commands.Cog.listener()

    @commands.command()
    async def based(self, ctx):
        await ctx.send('thank u based god')


def setup(client):
    client.add_cog(Utils(client))
