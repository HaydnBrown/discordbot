import discord
from discord.ext import commands
import os
import random
import motor
import motor.motor_asyncio
import time
import math
import datetime


class Betting(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.mongo_client = motor.motor_asyncio.AsyncIOMotorClient(os.environ['mongoConnectionStr'])
        self.mongo_db = self.mongo_client.DrakeCollections
        self.mongo_collection = self.mongo_db.ServersCollections

    @commands.command()
    async def setPoints(self, ctx, points):
        print("setPoints function...\n")
        if ctx.author.id == 136259896365678593:
            print("access granted...")
            user_list = await self.mongo_collection.find_one({'_id': 'users'})
            member_list = user_list['members']
            for member in member_list:
                await self.mongo_collection.update_one({"members.name": member['name']},
                                                       {"$set": {"members.$.points": points}})
        else:
            await ctx.send("Nice try, jack")

    @commands.command()
    async def initializePoints(self, ctx):
        print("Initializing users points")
        if ctx.author.id == 136259896365678593:
            print("access granted...")
            user_list = await self.mongo_collection.find_one({'_id': 'users'})
            member_list = user_list['members']
            for member in member_list:
                if 'points' in member:
                    print("User's points were already initialized")
                else:
                    print("Initializing {}'s points to 5000".format(member['name']))
                    member['points'] = 5000
            await self.mongo_collection.update_one({'_id': 'users'}, {"$set": {"members": member_list}})
            print("Updated user points")
        else:
            await ctx.send("You don't have permission for this command")

    @commands.command()
    async def myPoints(self, ctx):
        print("myPoints function called")
        user_list = await self.mongo_collection.find_one({'_id': 'users'})
        member_list = user_list['members']
        for member in member_list:
            if ctx.author.name == member['name']:
                content_str = "{} you have {} points".format(ctx.author.name, member['points'])
                await ctx.send(content_str)
                break

    @commands.command()
    async def dailyPoints(self, ctx):
        print("{}'s daily points".format(ctx.author.name))
        user_list = await self.mongo_collection.find_one({'_id': 'users'})
        member_list = user_list['members']
        for member in member_list:
            if ctx.author.name == member['name']:
                if 'points' in member:
                    if 'lastdaily' in member:
                        print("check the time of the last daily")
                        if (int(time.time()) - member['lastdaily']) > 79200:
                            print("user can claim daily")
                            member['lastdaily'] = int(time.time())
                            member['points'] = member['points'] + 250
                            await ctx.send("{} you have claimed your 250 daily points".format(ctx.author.name))
                            await self.mongo_collection.update_one({"members.name": ctx.message.author.name},
                                                                   {"$set": {
                                                                       "members.$.lastdaily": member['lastdaily'],
                                                                       "members.$.points": member['points']}})
                        else:
                            print("hasnt been long enough to claim daily")
                            time_remaining = datetime.timedelta(seconds=(79200 - (int(time.time()) - member['lastdaily'])))
                            await ctx.send(
                                "{} you have {} remaining before you can claim your next daily".format(ctx.author.name,
                                                                                                       time_remaining))
                    else:
                        print("User hasnt claimed dailies before, initialize daily time")
                        member['lastdaily'] = int(time.time())
                        member['points'] = member['points'] + 250
                        await ctx.send("{} you have claimed your 250 daily points".format(ctx.author.name))
                        await self.mongo_collection.update_one({"members.name": ctx.message.author.name},
                                                               {"$set": {
                                                                   "members.$.lastdaily": member['lastdaily'],
                                                                   "members.$.points": member['points']}})
                else:
                    await ctx.send("Your points aren't initialized, msg @Frenchmyfry")


def setup(client):
    client.add_cog(Betting(client))
