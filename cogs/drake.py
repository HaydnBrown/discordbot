import discord
from discord.ext import commands
import os
import random


class Drake(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rngDrake(self, ctx):
        random_int = random.randrange(0, 501)
        userid = ctx.message.author.mention

        if (random_int >= 0) and (random_int < 300):
            print("The random int was: " + str(random_int) + ", common")
            file_name = random.choice(os.listdir("photos/commonDrake"))
            full_path = "photos/commonDrake/" + file_name
            print("full path: " + full_path)
            with open(full_path, 'rb') as f:
                picture = discord.File(f)
                await ctx.channel.send(content="Your common drake", file=picture)
        elif (random_int >= 300) and (random_int < 400):
            print("The random int was: " + str(random_int))
            file_name = random.choice(os.listdir("photos/uncommonDrake"))
            full_path = "photos/uncommonDrake/" + file_name
            with open(full_path, 'rb') as f:
                picture = discord.File(f)
                await ctx.channel.send(content="your uncommon drake", file=picture)
        elif (random_int >= 400) and (random_int < 475):
            print("The random int was: " + str(random_int))
            file_name = random.choice(os.listdir("photos/uniqueDrake"))
            full_path = "photos/uniqueDrake/" + file_name
            with open(full_path, 'rb') as f:
                picture = discord.File(f)
                await ctx.channel.send(content="your unique drake", file=picture)
        elif (random_int >= 475) and (random_int < 500):
            print("The random int was: " + str(random_int) + ", rare!")
            file_name = random.choice(os.listdir("photos/rareDrake"))
            full_path = "photos/rareDrake/" + file_name
            print("full path: " + full_path)
            msgtext = userid + " you pulled a rare drake!"
            with open(full_path, 'rb') as f:
                picture = discord.File(f)
                await ctx.channel.send(content=str(msgtext), file=picture)
        else:
            print("The random int was: " + str(random_int) + ", legendary!")
            file_name = random.choice(os.listdir("photos/legendaryDrake"))
            print("filename: " + file_name)
            full_path = "photos/legendaryDrake/" + file_name
            print("full path: " + full_path)
            msgtext = userid + " you pulled a legendary drake!"
            with open(full_path, 'rb') as f:
                picture = discord.File(f)
                await ctx.channel.send(content=str(msgtext), file=picture)

    @commands.command()
    async def rngDrakeOdds(self, ctx):
        common_size = len(os.listdir("photos/commonDrake"))
        uncommon_size = len(os.listdir("photos/uncommonDrake"))
        unique_size = len(os.listdir("photos/uniqueDrake"))
        rare_size = len(os.listdir("photos/rareDrake"))
        legendary_size = len(os.listdir("photos/legendaryDrake"))
        output = 'Odds of drake rarities: \nCommon ~60% with {} items \nUncommon ~20% with {} items \nUnique ~15% with {} items \nRare ~5% with {} items \nLegendary ~0.2% with {} items'.format(common_size, uncommon_size, unique_size, rare_size, legendary_size)
        await ctx.send(content=output)


def setup(client):
    client.add_cog(Drake(client))
