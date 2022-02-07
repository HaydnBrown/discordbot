import discord
from discord.ext import commands
import os
import globalvars
import time
import youtube_dl
intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='$', intents=intents)


@client.event
async def on_ready():
    print("Bot is ready...\n")


@client.event
async def on_raw_reaction_add(payload):
    guild = discord.utils.get(client.guilds, id=payload.guild_id)
    user = discord.utils.get(guild.members, id=payload.user_id)
    channel = discord.utils.get(guild.text_channels, id=payload.channel_id)
    msg = await channel.fetch_message(payload.message_id)
    # check if user has results associated with them
    if user.id in globalvars.message_info:
        # check if the message they reacted to is the one containing the results
        if globalvars.message_info[user.id][0] == payload.message_id:
            index = globalvars.message_info[user.id][2]
            if payload.emoji.name == "➡️":
                if index == (len(globalvars.user_results[user.id]) - 1):
                    await channel.send("You've reached the end of the search results")
                else:
                    index = index + 1
                    results_list = globalvars.user_results[user.id][index]
                    new_embed = discord.Embed(title=user.name, description="Amazon search results", colour=0x9D34D1)
                    if results_list[4] != "none":
                        new_embed.set_image(url=results_list[4])
                    new_embed.add_field(name="Product name", value=results_list[0], inline=False)
                    new_embed.add_field(name="Link", value=results_list[3], inline=False)
                    new_embed.add_field(name="Price", value=results_list[1], inline=True)
                    new_embed.add_field(name="Reviews", value=results_list[2], inline=True)
                    text = "Showing result " + str(index + 1) + "/" + str(len(globalvars.user_results[user.id]))
                    new_embed.add_field(name="Result", value=text, inline=False)
                    await msg.edit(embed=new_embed)
                    globalvars.message_info[user.id][2] = index
                    globalvars.message_info[user.id][1] = time.time()
            elif payload.emoji.name == "⬅️":
                if index == 0:
                    await channel.send("This is the first item")
                else:
                    index = index - 1
                    results_list = globalvars.user_results[user.id][index]
                    new_embed = discord.Embed(title=user.name, description="Amazon search results", colour=0x9D34D1)
                    new_embed.add_field(name="Product name", value=results_list[0], inline=False)
                    new_embed.add_field(name="Link", value=results_list[3], inline=False)
                    new_embed.add_field(name="Price", value=results_list[1], inline=True)
                    new_embed.add_field(name="Reviews", value=results_list[2], inline=True)
                    text = "Showing result " + str(index + 1) + "/" + str(len(globalvars.user_results[user.id]))
                    new_embed.add_field(name="Result", value=text, inline=False)
                    await msg.edit(embed=new_embed)
                    globalvars.message_info[user.id][2] = index
                    globalvars.message_info[user.id][1] = time.time()


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command name, please use $help for a list of all commands')


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        print("file loaded: " + filename[:-3])
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(os.environ['basedBotStr'])
