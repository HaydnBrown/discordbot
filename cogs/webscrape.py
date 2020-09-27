import discord
from discord.ext import commands
import os
import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup


class WebScrape(commands.Cog):

    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(WebScrape(client))
