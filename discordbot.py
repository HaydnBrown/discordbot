import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print("Bot is ready...")


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
        client.load_extension(f'cogs.{filename[:-3]}')


client.run('NzU5MjE1NDgwOTI5NjQ4NzIx.X26QhA.nSJXHYZFVF55m-sb4XYEHnep1Qs')
