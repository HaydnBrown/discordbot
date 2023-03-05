import asyncio

import discord
from discord.ext import commands
import os
import random
import youtube_dl


class PeterClips(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def peterClip(self, ctx, clip: str):
        clipName = "audio/PeterGriffin/" + clip + ".mp3"
        print("clip to play: " + clipName)
        voiceChannel = ctx.message.author.voice.channel
        if not voiceChannel:
            await ctx.send("Please connect to a voice channel first")
        else:
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                await voice.move_to(voiceChannel)
            else:
                voice = await voiceChannel.connect()
            voice.play(discord.FFmpegPCMAudio(clipName))


    @commands.command()
    async def rngPeterClip(self, ctx):
        fileName = random.choice(os.listdir('audio/PeterGriffin'))
        fullPath = "audio/PeterGriffin/" + fileName
        channel = ctx.message.author.voice.channel
        if not channel:
            await ctx.send("Please connect to a voice channel first")
        else:
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect()
            voice.play(discord.FFmpegPCMAudio(fullPath))

    @commands.command()
    async def leaveVC(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_connected():
            await voice.disconnect()
        else:
            await ctx.send("Not currently in a voice channel")

    @commands.command()
    async def playYT(self, ctx, url: str):
        channel = ctx.message.author.voice.channel
        if not channel:
            await ctx.send("Please connect to a voice channel first")
        else:
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect()
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    os.rename(file, "song.mp3")
            voice.play(discord.FFmpegPCMAudio("song.mp3"))

    @commands.command()
    async def availableClips(self, ctx):
        output = "The available clip names are: "
        for file in os.listdir('audio/PeterGriffin'):
            output = output + file[:-4] + ", "
        print(output)
        await ctx.send(output)



async def setup(client):
    await client.add_cog(PeterClips(client))
