import discord
from discord.ext import commands
import os
import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class WebScrape(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.PATH = "/home/haydn/chromedriver.exe"
        self.driver = webdriver.Chrome()

    @commands.command()
    async def find_tech(self, ctx, search_item):
        self.driver.get("https://www.amazon.ca/")
        print(self.driver.title)
        search_bar = self.driver.find_element_by_id("twotabsearchtextbox")
        search_bar.send_keys(search_item)
        search_bar.send_keys(Keys.RETURN)
        try:
            print("we made it to the search page")
            print("Hello1")
            results = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='s-main-slot s-result-list s-search-results "
                                                          "sg-row']"))
            )
            print("Hello2")
            result_items = results.find_elements_by_xpath(".//div[@class='sg-col-4-of-24 sg-col-4-of-12 sg-col-4-of-36 "
                                                          "s-result-item s-asin sg-col-4-of-28 sg-col-4-of-16 sg-col "
                                                          "sg-col-4-of-20 sg-col-4-of-32']")
            print("Hello3")
            print("number of items on page 1: " + str(len(result_items)))
            time.sleep(5)
        except:
            print("The results of the search were not found.")
        finally:
            print("-----closing the web driver-----")
            self.driver.quit()

    @commands.command()
    async def scrape_test(self, ctx):
        print("web scraper cog is working")


def setup(client):
    client.add_cog(WebScrape(client))
