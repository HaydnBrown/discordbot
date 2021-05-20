import discord
from discord.ext import commands
import os
import youtube_dl
intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='$', intents=intents)


@client.event
async def on_ready():
    print("Bot is ready...\n")


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

client.run('NzU5MjE1NDgwOTI5NjQ4NzIx.X26QhA.oT5-bMTd_0QIYxeawOOWod0jAiY')
