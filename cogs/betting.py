import discord
from discord.ext import commands
import os
import random
import motor
import motor.motor_asyncio
import time
import math

class Betting(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.mongo_client = motor.motor_asyncio.AsyncIOMotorClient(os.environ['mongoConnectionStr'])
        self.mongo_db = self.mongo_client.DrakeCollections
        self.mongo_collection = self.mongo_db.ServersCollections

    @commands.command()
    async def updatePoints(self, ctx):
        print("Updating users points")
        if (ctx.author.id == 136259896365678593):
            print("access granted...")
            user_list = await self.mongo_collection.find_one({'_id': 'users'})
        else:
            await ctx.send("You don't have permission for this command")



def setup(client):
    client.add_cog(Betting(client))