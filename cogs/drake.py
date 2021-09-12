import discord
from discord.ext import commands
import os
import random
import motor
import motor.motor_asyncio
import time
import math
from tabulate import tabulate

# mongo "mongodb+srv://cluster0.pkpoc.mongodb.net/DrakeCollections" --username haydnbrown

drake_cooldowns = {}


class Drake(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.mongo_client = motor.motor_asyncio.AsyncIOMotorClient(
            "mongodb+srv://haydnbrown:Ds572284@cluster0.pkpoc.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        self.mongo_db = self.mongo_client.DrakeCollections
        self.mongo_collection = self.mongo_db.ServersCollections

    async def addServerToDB(self, ctx):
        guild_members = ctx.guild.members
        human_members = guild_members.copy()
        for member in guild_members:
            if member.bot:
                human_members.remove(member)
        for m in human_members:
            print(m.name)
        await self.mongo_collection.insert_one({'_id': ctx.guild.id, 'members': []})
        for member in human_members:
            await self.mongo_collection.update_one({'_id': ctx.guild.id},
                                                   {'$addToSet': {'members':
                                                                      {'name': member.name,
                                                                       'common': [],
                                                                       'uncommon': [],
                                                                       'unique': [],
                                                                       'rare': [],
                                                                       'legendary': []}}})

    def progressstring(self, percentage):
        output_str = ""
        p = math.floor(percentage / 10)
        for x in range(0, 10):
            if x < p:
                output_str = output_str + "█"
            else:
                output_str = output_str + "░"
        return output_str

    @commands.command()
    async def rngDrake(self, ctx):
        current_guild = ctx.guild
        if current_guild is None:
            await ctx.channel.send("rngDrake functionality is only available from within a server")
        else:
            global drake_cooldowns
            if ctx.message.author.name in drake_cooldowns:
                new_time = time.time()
                if new_time - drake_cooldowns[ctx.message.author.name] > 600:
                    drake_cooldowns[ctx.message.author.name] = new_time
                else:
                    await ctx.channel.send("You need to wait", (new_time - drake_cooldowns[ctx.message.author.name]), "more seconds before your next pull")
                    return
            else:
                drake_cooldowns[ctx.message.author.name] = time.time()
            # pull drake functionality
            random_int = random.randrange(0, 501)
            userid = ctx.message.author.mention
            picture = None
            file_name = ""
            rarity = ""
            full_path = ""
            msg_text = ""
            if (random_int >= 0) and (random_int < 300):
                file_name = random.choice(os.listdir("photos/commonDrake"))
                full_path = "photos/commonDrake/" + file_name
                rarity = "common"
                msg_text = "Your common drake."
            elif (random_int >= 300) and (random_int < 400):
                file_name = random.choice(os.listdir("photos/uncommonDrake"))
                full_path = "photos/uncommonDrake/" + file_name
                rarity = "uncommon"
                msg_text = "Your uncommon drake."
            elif (random_int >= 400) and (random_int < 475):
                file_name = random.choice(os.listdir("photos/uniqueDrake"))
                full_path = "photos/uniqueDrake/" + file_name
                rarity = "unique"
                msg_text = "Your unique drake."
            elif (random_int >= 475) and (random_int < 500):
                file_name = random.choice(os.listdir("photos/rareDrake"))
                full_path = "photos/rareDrake/" + file_name
                rarity = "rare"
                msg_text = userid + " you pulled a rare drake!"
            else:
                file_name = random.choice(os.listdir("photos/legendaryDrake"))
                full_path = "photos/legendaryDrake/" + file_name
                rarity = "legendary"
                msg_text = userid + " you pulled a legendary drake!"

            guild_document = await self.mongo_collection.find_one({'_id': current_guild.id})
            # check to make sure the server is in the database
            if guild_document is None:
                # the server isn't yet tracked in the database, initialize it with addServerToDB
                print("the server isn't in the db, adding it now")
                await self.addServerToDB(ctx)
                await self.mongo_collection.update_one({"members.name": ctx.message.author.name},
                                                       {"$addToSet": {"members.$.{}".format(rarity): file_name}})
            else:
                # find the member document
                result = await self.mongo_collection.find_one({"members.name": ctx.message.author.name})
                members = result['members']
                for member in members:
                    if member['name'] == ctx.message.author.name:
                        rarity_list = member[rarity]
                        if file_name in rarity_list:
                            # player already found this drake
                            with open(full_path, 'rb') as f:
                                picture = discord.File(f)
                                msg_text = msg_text + " You already own this drake"
                                await ctx.channel.send(content=msg_text, file=picture)
                        else:
                            # new drake pull, add to players collection
                            await self.mongo_collection.update_one({"members.name": ctx.message.author.name},
                                                                   {"$addToSet": {
                                                                       "members.$.{}".format(rarity): file_name}})
                            with open(full_path, 'rb') as f:
                                picture = discord.File(f)
                                msg_text = msg_text + " Added to your collection!"
                                await ctx.channel.send(content=msg_text, file=picture)

    @commands.command()
    async def rngDrakeOdds(self, ctx):
        common_size = len(os.listdir("photos/commonDrake"))
        uncommon_size = len(os.listdir("photos/uncommonDrake"))
        unique_size = len(os.listdir("photos/uniqueDrake"))
        rare_size = len(os.listdir("photos/rareDrake"))
        legendary_size = len(os.listdir("photos/legendaryDrake"))
        output = 'Odds of drake rarities: \nCommon ~60% with {} items \nUncommon ~20% with {} items \nUnique ~15% with {} items \nRare ~5% with {} items \nLegendary ~0.2% with {} items'.format(
            common_size, uncommon_size, unique_size, rare_size, legendary_size)
        await ctx.send(content=output)

    @commands.command()
    async def myCollection(self, ctx):
        result = await self.mongo_collection.find_one({"members.name": ctx.message.author.name})
        members = result['members']
        for member in members:
            if member['name'] == ctx.message.author.name:
                common_progress = (len(member['common']) / len(os.listdir("photos/commonDrake"))) * 100
                common_bar = self.progressstring(common_progress)
                common_str = "Commons: \t{} \t{:.2f}%".format(common_bar, common_progress)
                uncommon_progress = (len(member['uncommon']) / len(os.listdir("photos/uncommonDrake"))) * 100
                uncommon_bar = self.progressstring(uncommon_progress)
                uncommon_str = "Uncommons: \t{} \t{:.2f}%".format(uncommon_bar, uncommon_progress)
                unique_progress = (len(member['unique']) / len(os.listdir("photos/uniqueDrake"))) * 100
                unique_bar = self.progressstring(unique_progress)
                unique_str = "Uniques: \t{} \t{:.2f}%".format(unique_bar, unique_progress)
                rare_progress = (len(member['rare']) / len(os.listdir("photos/rareDrake"))) * 100
                rare_bar = self.progressstring(rare_progress)
                rare_str = "Rares: \t{} \t{:.2f}%".format(rare_bar, rare_progress)
                legendary_progress = (len(member['legendary']) / len(os.listdir("photos/legendaryDrake"))) * 100
                legendary_bar = self.progressstring(legendary_progress)
                legendary_str = "Legendaries: \t{} \t{:.2f}%".format(legendary_bar, legendary_progress)
                data = [["Commons:", common_bar, "{:.2f}%".format(common_progress)],
                        ["Uncommons:", uncommon_bar, "{:.2f}%".format(uncommon_progress)],
                        ["Uniques:", unique_bar, "{:.2f}%".format(unique_progress)],
                        ["Rares:", rare_bar, "{:.2f}%".format(rare_progress)],
                        ["Legendary:", legendary_bar, "{:.2f}%".format(legendary_progress)]]
                output_str = "Your collection progress: \n" + tabulate(data)
                await ctx.channel.send("```\n{}\n```".format(output_str))

    @commands.command()
    async def globalLeaderBoard(self, ctx):
        totalDrakes = len(os.listdir("photos/commonDrake")) + len(os.listdir("photos/uncommonDrake")) + \
                      len(os.listdir("photos/uniqueDrake")) + len(os.listdir("photos/rareDrake")) + \
                      len(os.listdir("photos/legendaryDrake"))
        users = {} # dict containing every user and their total % of collection completed
        result = self.mongo_collection.find()
        docs = await result.to_list(100)
        print("success")
        print(len(docs))
        print(docs[0]['members'][0]['name'])
        for document in docs:
            # print(document['members'])
            # members = document['members']
            for user in document['members']:
                userDrakes = len(user['common']) + len(user['uncommon']) + len(user['unique']) + len(user['rare']) + \
                             len(user['legendary'])
                print(user['name'], ", drakes: ", userDrakes)
                percentage = (userDrakes / totalDrakes) * 100
                users[user['name']] = percentage
        print(users)
        finalUsers = {k: v for k, v in sorted(users.items(), key=lambda item: item[1], reverse=True)}
        print(finalUsers)


def setup(client):
    client.add_cog(Drake(client))
