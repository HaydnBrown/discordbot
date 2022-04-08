import discord
from discord.ext import commands
import youtube_dl
import os
import random


class Audio(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def stop(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            voice.stop()
        else:
            await ctx.send("Music not playing, failed to stop")

    @commands.command()
    async def supastar(self, ctx):
        voiceChannel = ctx.message.author.voice.channel
        if not voiceChannel:
            await ctx.send("Please connect to a voice channel first")
        else:
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                await voice.move_to(voiceChannel)
            else:
                voice = await voiceChannel.connect()
            voice.play(discord.FFmpegPCMAudio('audio/songs/superstar.mp3'))

    @commands.command()
    async def soultrain(self, ctx):
        voiceChannel = ctx.message.author.voice.channel
        if not voiceChannel:
            await ctx.send("Please connect to a voice channel first")
        else:
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                await voice.move_to(voiceChannel)
            else:
                voice = await voiceChannel.connect()
            voice.play(discord.FFmpegPCMAudio('audio/songs/soultrain.mp3'))

    @commands.command()
    async def gusscream(self, ctx):
        voiceChannel = ctx.message.author.voice.channel
        if not voiceChannel:
            await ctx.send("Please connect to a voice channel first")
        else:
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                await voice.move_to(voiceChannel)
            else:
                voice = await voiceChannel.connect()
            voice.play(discord.FFmpegPCMAudio('audio/misc/gusscream.mp3'))

    @commands.command()
    async def watchthis(self, ctx):
        voiceChannel = ctx.message.author.voice.channel
        if not voiceChannel:
            await ctx.send("Please connect to a voice channel first")
        else:
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                await voice.move_to(voiceChannel)
            else:
                voice = await voiceChannel.connect()
            voice.play(discord.FFmpegPCMAudio('audio/terry/watchthis.mp3'))

    @commands.command()
    async def smartest(self, ctx):
        voiceChannel = ctx.message.author.voice.channel
        if not voiceChannel:
            await ctx.send("Please connect to a voice channel first")
        else:
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                await voice.move_to(voiceChannel)
            else:
                voice = await voiceChannel.connect()
            voice.play(discord.FFmpegPCMAudio('audio/terry/smartestprogrammer.mp3'))

    @commands.command()
    async def divine(self, ctx):
        voiceChannel = ctx.message.author.voice.channel
        if not voiceChannel:
            await ctx.send("Please connect to a voice channel first")
        else:
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                await voice.move_to(voiceChannel)
            else:
                voice = await voiceChannel.connect()
            voice.play(discord.FFmpegPCMAudio('audio/terry/divineintellect.mp3'))

    @commands.command()
    async def compiler(self, ctx):
        voiceChannel = ctx.message.author.voice.channel
        if not voiceChannel:
            await ctx.send("Please connect to a voice channel first")
        else:
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                await voice.move_to(voiceChannel)
            else:
                voice = await voiceChannel.connect()
            voice.play(discord.FFmpegPCMAudio('audio/terry/64bitcompiler.mp3'))

    @commands.command()
    async def keemscream(self, ctx):
        voiceChannel = ctx.message.author.voice.channel
        if not voiceChannel:
            await ctx.send("Please connect to a voice channel first")
        else:
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                await voice.move_to(voiceChannel)
            else:
                voice = await voiceChannel.connect()
            voice.play(discord.FFmpegPCMAudio('audio/misc/keemscream-final.mp3'))

    @commands.command()
    async def kinky(self, ctx):
        voiceChannel = ctx.message.author.voice.channel
        if not voiceChannel:
            await ctx.send("Please connect to a voice channel first")
        else:
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                await voice.move_to(voiceChannel)
            else:
                voice = await voiceChannel.connect()
            voice.play(discord.FFmpegPCMAudio('audio/misc/joebuddenkinky.mp3'))

    @commands.command()
    async def dayum(self, ctx):
        voiceChannel = ctx.message.author.voice.channel
        if not voiceChannel:
            await ctx.send("Please connect to a voice channel first")
        else:
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                await voice.move_to(voiceChannel)
            else:
                voice = await voiceChannel.connect()
            voice.play(discord.FFmpegPCMAudio('audio/misc/dayum_1.wav'))

    @commands.command()
    async def truevoice(self, ctx):
        voiceChannel = ctx.message.author.voice.channel
        if not voiceChannel:
            await ctx.send("Please connect to a voice channel first")
        else:
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                await voice.move_to(voiceChannel)
            else:
                voice = await voiceChannel.connect()
            voice.play(discord.FFmpegPCMAudio('audio/misc/thatstrue.mp3'))

    @commands.command()
    async def lookspongebob(self, ctx):
        voiceChannel = ctx.message.author.voice.channel
        if not voiceChannel:
            await ctx.send("Please connect to a voice channel first")
        else:
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                await voice.move_to(voiceChannel)
            else:
                voice = await voiceChannel.connect()
            voice.play(discord.FFmpegPCMAudio('audio/misc/lookspongebob.mp3'))

    @commands.command()
    async def threepirates(self, ctx):
        voiceChannel = ctx.message.author.voice.channel
        if not voiceChannel:
            await ctx.send("Please connect to a voice channel first")
        else:
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                await voice.move_to(voiceChannel)
            else:
                voice = await voiceChannel.connect()
            voice.play(discord.FFmpegPCMAudio('audio/misc/3pirates.mp3'))

    @commands.command()
    async def goober(self, ctx):
        voiceChannel = ctx.message.author.voice.channel
        if not voiceChannel:
            await ctx.send("Please connect to a voice channel first")
        else:
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                await voice.move_to(voiceChannel)
            else:
                voice = await voiceChannel.connect()
            voice.play(discord.FFmpegPCMAudio('audio/misc/goober-trim.mp3'))


def setup(client):
    client.add_cog(Audio(client))
