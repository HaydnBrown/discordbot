import discord
import youtube_dl
from discord.ext import commands
from discord.utils import get
import os
import shutil
import logging
import asyncio
import random
import json


class AV(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.queues = {}


    @commands.command(pass_context=True)
    async def join(self, ctx):
        global voice
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
        await ctx.send(f"Joined {channel}")

    @commands.command(pass_context=True)
    async def leave(self, ctx):
        channel = ctx.message.author.voice_channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            await ctx.send(f"left {channel}")

    @commands.command()
    async def play(self, ctx, url: str):

        def check_queue():
            Queue_infile = os.path.isdir("./Queue")
            if Queue_infile is True:
                DIR = os.path.abspath(os.path.realpath("Queue"))
                length = len(os.listdir(DIR))
                still_q = length - 1
                try:
                    first_file = os.listdir(DIR)[0]
                except:
                    logging.info("No more queued songs\n")
                    self.queues.clear()
                    return
                main_location = os.path.dirname(os.path.realpath(__file__))
                song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
                if length != 0:
                    logging.info("Song done, playing next in Queue\n")
                    logging.info(f"Songs still in Queue: {still_q}")
                    song_there = os.path.isfile("song.mp3")
                    if song_there:
                        os.remove("song.mp3")
                    shutil.move(song_path, main_location)
                    for file in os.listdir("./"):
                        if file.endswith(".mp3"):
                            os.rename(file, 'song.mp3')

                    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                    voice.source = discord.PCMVolumeTransformer(voice.source)
                    voice.source.volume = 0.07
                else:
                    self.queues.clear()
                    return
            else:
                self.queues.clear()
                logging.info("No songs were queued before the ending of the last song\n")

        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
                self.queues.clear()
                logging.info("Removed old song file")
        except PermissionError:
            logging.info("Trying to delete song file, but its being played")
            await ctx.send("ERROR: Music playing")
            return

        Queue_infile = os.path.isdir("./Queue")
        try:
            Queue_folder = "./Queue"
            if Queue_infile is True:
                logging.info("Removed old Queue folder")
                shutil.rmtree(Queue_folder)
        except:
            logging.info("No old queue folder")

        await ctx.send("Getting everything ready now")

        voice = get(self.client.voice_clients, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            logging.info("Downloading audio now\n")
            ydl.download([url])

        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                name = file
                logging.info(f"Renamed file: {file}\n")
                os.rename(file, "song.mp3")

        voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
        voice.source = discord.PCMVolumeTransformer(voice.source)
        # voice.source.volume = 0.07

        name = name.rsplit("-", 2)
        await ctx.send(f"Playing: {name[0]}")
        logging.info("Playing\n")

    @commands.command(pass_context=True)
    async def pause(self, ctx):

        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            logging.info("Music paused")
            voice.pause()
            await ctx.send("Music paused")
        else:
            logging.info("Music not playing failed pause")
            await ctx.send("Music not playing failed pause")

    @commands.command(pass_context=True)
    async def resume(self, ctx):

        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():
            logging.info("Resumed music")
            voice.resume()
            await ctx.send("Resumed music")
        else:
            logging.info("Music is not paused")
            await ctx.send("Music is not paused")

    @commands.command(pass_context=True)
    async def skip(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)

        self.queues.clear()
        if voice and voice.is_playing():
            logging.info("Music skipped")
            voice.stop()
            await ctx.send("Music skipped")
        else:
            logging.info("No Music playing failed to skip")
            await ctx.send("No music playing failed to skip")

    @commands.command(pass_context=True)
    async def queue(self, ctx, url: str):
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is False:
            os.mkdir("Queue")
        DIR = os.path.abspath(os.path.realpath("Queue"))
        q_num = len(os.listdir(DIR))
        q_num += 1
        add_queue = True
        while add_queue:
            if q_num in self.queues:
                q_num += 1
            else:
                add_queue = False
                self.queues[q_num] = q_num
        queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'outtmpl': queue_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            logging.info("Downloading audio now")
            ydl.download([url])
        await ctx.send("adding song" + str(q_num) + " to the queue")

        logging.info("Song added to Queue\n")


async def setup(client):
    await client.add_cog(AV(client))
