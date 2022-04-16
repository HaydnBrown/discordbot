import discord
from discord.ext import commands


class Utils(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events use @commands.Cog.listener()

    @commands.command()
    async def patchNotes(self, ctx):
        """
        What's new
        """
        print("\n\n---Patch Notes---")
        try:
            await ctx.send(content="Whats new:\n"
                                   "Added points system and betting. Get more info on betting by using `$help Betting`"
                                   " and then `$help <cmd name>`.\n"
                                   "Everybody starts with 5000 points and can gain more points through `$dailyPoints`, "
                                   "pulling duplicate drakes, or by winning bets.")
        except Exception as e:
            print("Exception : {}".format(e))

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
