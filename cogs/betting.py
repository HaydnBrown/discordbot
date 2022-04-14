import discord
from discord.ext import commands
import os
import random
import motor
import motor.motor_asyncio
import time
import math
import datetime
from urllib.error import HTTPError


def generate_code():
    chars = "1234567890abcdefghijklmnopqrstuvwxyz"
    list_str = ""
    for i in range(0, 6):
        list_str += random.choice(chars)
    return list_str


class Betting(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.mongo_client = motor.motor_asyncio.AsyncIOMotorClient(os.environ['mongoConnectionStr'])
        self.mongo_db = self.mongo_client.DrakeCollections
        self.mongo_collection = self.mongo_db.ServersCollections

    @commands.command()
    async def initBetting(self, ctx):
        """
        Initializes the betting doc in the database. Admin only.
        """
        print("\nInitializing betting in the db")
        if ctx.author.id == 136259896365678593:
            print("access granted...")
            betting_doc = await self.mongo_collection.find_one({'_id': 'betting'})
            if betting_doc is None:
                await self.mongo_collection.insert_one({'_id': 'betting', 'bets': []})
            else:
                print("Betting in the db is already initialized")
        else:
            await ctx.send(content="not an admin")

    @commands.command()
    async def createBet(self, ctx, *args):
        """
        Creates a new bet with a unique 6-digit code to access it. Requires two result options to be specified.
        Usage: Specify the options by typing two phrases separated by ";;;"
        Format: <Option 1> ;;; <Option 2>
        Example: Over 2.5 attempts ;;; under 2.5 attempts
        """
        arg_list = list(args)
        bet_id = generate_code()
        print("\nCreating a new bet with id: {}".format(bet_id))
        index_of_seperator = -1  # after the loop, represents the start of second option
        if ";;;" in arg_list:
            print("Format for bet was correct")
            index_of_seperator = arg_list.index(";;;")
            print("removing sep from arg_list")
            arg_list.remove(";;;")
        else:
            print("format was wrong, checking for typo")
            for i in range(0, len(arg_list)):
                if ";;;" in arg_list[i]:
                    print("found the typo word")
                    if arg_list[i].endswith(";;;"):
                        print("this is the end of option 1")
                        arg_list[i].strip(";")
                        index_of_seperator = i + 1
                    else:
                        # the word starts with ;;;
                        print("this is the start of option 2")
                        arg_list[i].strip(";")
                        index_of_seperator = i
        print("done checking for separator, index is: {}".format(index_of_seperator))
        if index_of_seperator == -1:
            print("Could not find ;;; in input")
            await ctx.send(content="{}, bad input, please try again. Use #help createBet for help on how to create a "
                                   "bet".format(ctx.author.name))
            return None
        else:
            # we have the index, can create the bet.
            print("separator found")
            option_one = ""
            for i in range(0, index_of_seperator):
                option_one = option_one + arg_list[i] + " "
            print("option 1: {}".format(option_one))
            option_two = ""
            for i in range(index_of_seperator, len(arg_list)):
                option_two = option_two + arg_list[i] + " "
            print("option 2: {}".format(option_two))
            print("adding bet to db")
            await self.mongo_collection.update_one({'_id': 'betting'},
                                                   {'$addToSet': {'bets': {'code': bet_id,
                                                                           'guild': ctx.guild.id,
                                                                           'creator': ctx.author.name,
                                                                           'option_one': option_one,
                                                                           'option_two': option_two,
                                                                           'users': []}}})
            print("bet added to db, sending msg to user")
            await ctx.send(content="Created bet with unique code: {} and options: \n1: {} \n2: {} \n{} will be "
                                   "responsible for determining "
                                   "the outcome and closing the bet".format(bet_id, option_one, option_two,
                                                                            ctx.author.name))
            print("msg sent to user. createBet done")

    @commands.command()
    async def placeBet(self, ctx, code, option, amount):
        """
         This command is used to place points on an existing bet.
         Format: $placeBet <bet code> <option #> <amount to bet>
         Example: $placeBet abc123 2 2500

        :param code: The unique 6-digit bet code
        :param option: option to bet on (1 or 2)
        :param amount: Amount to bet
        """
        print("\nplaceBet command")
        # the process for updating a user's existing bet is super inefficient. can definitely improve it
        # by going through the document and if the user doesnt exist, update it then, and if they do, update it
        # then and there instead of going through the for loops a second time
        print("Getting userlist ")
        user_list = await self.mongo_collection.find_one({'_id': 'users'})
        user = next((user for user in user_list['members'] if user['name'] == ctx.author.name), None)
        print("got user")
        option = int(option)
        amount = int(amount)
        if amount > user['points']:
            await ctx.send(
                content="{}, you have {} points, please enter a value less than or equal to this amount".format(
                    ctx.author.name, user['points']))
            return None
        betting_doc = await self.mongo_collection.find_one({'_id': 'betting'})  # returns all bets
        bet = next((bet for bet in betting_doc['bets'] if bet['code'] == str(code)), None)
        print("bet returned: {}".format(bet))

        # check if user already placed a bet
        existing_user = next((u for u in bet['users'] if u['name'] == ctx.author.name), None)
        print("checked if user exists")
        if existing_user is None:
            # add user to users array in bet
            print("initializing user in bet")
            await self.mongo_collection.update_one({'bets.code': code},
                                                   {'$addToSet': {'bets.$.users': {'name': ctx.author.name,
                                                                                   'option': option,
                                                                                   'amount': amount}}})
        else:
            # update user array
            for user in bet['users']:
                if user['name'] == ctx.author.name:
                    user['amount'] += amount
            for b in betting_doc['bets']:
                if b['code'] == code:
                    b['users'] = bet['users']
            # user exists, update the amount bet
            print("updating user's existing bet")
            try:
                await self.mongo_collection.update_one({'_id': 'betting'},
                                                       {'$set': {'bets': betting_doc['bets']}})
            except Exception as e:
                print("\nException raised: {}\n".format(e))
        print("updated user in the bet, now change their points")
        await self.mongo_collection.update_one({"members.name": ctx.message.author.name},
                                               {"$inc": {"members.$.points": (amount * -1)}})
        await ctx.send(content="{}, your wager for {} has been placed on bet {}".format(ctx.author.name, amount, code))
        print("updated users points. DONE.")

    @commands.command()
    async def viewBet(self, ctx, code):
        """
        View a bet's options and the amount wagered on them given the bet code

        :param code: The unique code of the bet
        """
        print("\nviewBet function")
        betting_doc = await self.mongo_collection.find_one({'_id': 'betting'})
        bet = next((bet for bet in betting_doc['bets'] if bet['code'] == str(code)), None)
        op_1_wager = 0
        op_2_wager = 0
        for user in bet['users']:
            if user['option'] == 1:
                op_1_wager += user['amount']
            else:
                op_2_wager += user['amount']
        return_str = "Bet with code {}: \nOption 1: {} | {} points wagered\nOption 2: {} | {} points wagered".format(
            code, bet['option_one'], op_1_wager, bet['option_two'], op_2_wager)
        try:
            await ctx.send(content=return_str)
        except Exception as e:
            print("couldnt send msg to user, exception: {}".format(e))
        finally:
            print("DONE")

    @commands.command()
    async def availableBets(self, ctx):
        """
        View the bets available in this server
        """
        print("\navailableBets function")
        return_str = "All bets available in this server: \n\n"
        betting_doc = await self.mongo_collection.find_one({'_id': 'betting'})
        op_1_wager = 0
        op_2_wager = 0
        for bet in betting_doc['bets']:
            if bet['guild'] == ctx.guild.id:
                op_1_wager = 0
                op_2_wager = 0
                for user in bet['users']:
                    if user['option'] == 1:
                        op_1_wager += user['amount']
                    else:
                        op_2_wager += user['amount']
                return_str += "Bet with code {}: \nOption 1: {} | {} points wagered\nOption 2: {} | {} points " \
                              "wagered\n\n".format(bet['code'], bet['option_one'], op_1_wager, bet['option_two'],
                                                   op_2_wager)
        try:
            await ctx.send(content=return_str)
        except Exception as e:
            print("Couldn't send msg to user, exception: {}".format(e))
        finally:
            print("DONE")

    @commands.command()
    async def closeBet(self, ctx, code, option):
        """
        Closes an open bet and pays out the winners

        :param code: The 6-digit unique bet code
        :param option: The option which won. 1 or 2.
        """
        print("\n\ncloseBet function")
        option = int(option)
        betting_doc = await self.mongo_collection.find_one({'_id': 'betting'})
        total_1 = 0
        total_2 = 0
        bet = next((bet for bet in betting_doc['bets'] if bet['code'] == str(code)), None)
        if bet['creator'] == ctx.author.name:
            for user in bet['users']:
                if user['option'] == 1:
                    total_1 += user['amount']
                else:
                    total_2 += user['amount']
            odds_1 = int(total_1 / (total_1 + total_2))
            odds_2 = int(total_2 / (total_1 + total_2))
            odds = [odds_1, odds_2]
            # now payout each user
            for user in bet['user']:
                if user['option'] == option:
                    await self.mongo_collection.update_one({"members.name": ctx.message.author.name}, {
                        "$inc": {"members.$.points": int(user['amount'] / odds[option - 1])}})
            await ctx.send(content="{} won {} points".format(user['name'], int(user['amount'] / odds[option - 1])))
        else:
            await ctx.send(content="Only the person who created the bet can close it")
        print("DONE")

    @commands.command()
    async def setAllPoints(self, ctx, points):
        """
        Sets all user's points to the amount specified. Admin only.
        :param points: The number of points to set
        """
        print("\nsetPoints function...")
        if ctx.author.id == 136259896365678593:
            print("access granted...")
            user_list = await self.mongo_collection.find_one({'_id': 'users'})
            member_list = user_list['members']
            for member in member_list:
                await self.mongo_collection.update_one({"members.name": member['name']},
                                                       {"$set": {"members.$.points": int(points)}})
        else:
            await ctx.send("Nice try, jack")

    @commands.command()
    async def setUserPoints(self, ctx, user, points):
        """
        Increment a specified user by some amount of points. Admin only.

        :param user: The user to change points
        :param points: the amount of points
        """
        print("\nsetUserPoints function")
        if ctx.author.id == 136259896365678593:
            print("access granted...")
            await self.mongo_collection.update_one({"members.name": str(user)},
                                                   {"$inc": {"members.$.points": int(points)}})
        else:
            await ctx.send(content="You don't have permission for this command")
        print("DONE")

    @commands.command()
    async def initializePoints(self, ctx):
        """
        Used to initialize the points of users who are new to a server and haven't had their points set yet. Admin only.
        """
        print("\nInitializing users points")
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
        """
        Return the user's currently available points
        """
        print("\nmyPoints function called")
        user_list = await self.mongo_collection.find_one({'_id': 'users'})
        member_list = user_list['members']
        for member in member_list:
            if ctx.author.name == member['name']:
                content_str = "{} you have {} points".format(ctx.author.name, member['points'])
                await ctx.send(content=content_str)
        print("DONE")

    @commands.command()
    async def dailyPoints(self, ctx):
        """
        User can claim their daily 250 points every 22 hours. If they try to claim within the 22 hour period they will
        be notified how much longer the need to wait before claiming again
        """
        print("\n{}'s daily points".format(ctx.author.name))
        user_list = await self.mongo_collection.find_one({'_id': 'users'})
        member_list = user_list['members']
        for member in member_list:
            if ctx.author.name == member['name']:
                if 'points' in member:
                    if 'lastdaily' in member:
                        print("check the time of the last daily")
                        if (int(time.time()) - member['lastdaily']) > 79200:
                            print("user can claim daily")
                            member['points'] = member['points'] + 250
                            await ctx.send(content="{} you have claimed your 250 daily points".format(ctx.author.name))
                            await self.mongo_collection.update_one({"members.name": ctx.message.author.name},
                                                                   {"$set": {
                                                                       "members.$.lastdaily": int(time.time()),
                                                                       "members.$.points": member['points']}})
                        else:
                            print("hasnt been long enough to claim daily")
                            time_remaining = datetime.timedelta(
                                seconds=(79200 - (int(time.time()) - member['lastdaily'])))
                            await ctx.send(content=
                            "{} you have {} remaining before you can claim your next daily".format(
                                ctx.author.name,
                                time_remaining))
                    else:
                        print("User hasnt claimed dailies before, initialize daily time")
                        member['points'] = member['points'] + 250
                        await ctx.send(content="{} you have claimed your 250 daily points".format(ctx.author.name))
                        await self.mongo_collection.update_one({"members.name": ctx.message.author.name},
                                                               {"$set": {
                                                                   "members.$.lastdaily": int(time.time()),
                                                                   "members.$.points": member['points']}})
                else:
                    try:
                        print("initializing user's points and claiming their daily")
                        await self.mongo_collection.update_one({"members.name": ctx.message.author.name},
                                                               {"$set": {
                                                                   "members.$.lastdaily": int(time.time()),
                                                                   "members.$.points": 5250}})
                    except Exception as e:
                        print("Exception when trying to initialize users points and daily time: {}".format(e))
        print("DONE")


def setup(client):
    client.add_cog(Betting(client))
