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
import csv
import globalvars
import urllib.request


class WebScrape(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.PATH = "/home/haydn/chromedriver.exe"
        self.tech_filename = "tech_products.csv"

    @commands.command()
    async def amazon(self, ctx, *search_items):
        driver = webdriver.Chrome()
        search_item = ""
        for i in search_items:
            search_item = search_item + i + " "
        tech_file = open(self.tech_filename, "w")
        driver.get("https://www.amazon.ca/")
        print(driver.title)
        search_bar = driver.find_element_by_id("twotabsearchtextbox")
        search_bar.send_keys(search_item)
        search_bar.send_keys(Keys.RETURN)
        results_list = [[]]
        try:
            results = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='s-main-slot s-result-list s-search-results "
                                                          "sg-row']"))
            )
            result_items = results.find_elements_by_xpath(".//div[@class='s-expand-height s-include-content-margin s-border-bottom s-latency-cf-section']")
            print("number of items on page 1: " + str(len(result_items)))
            file_headers = "website, product_name, price, reviews\n"
            tech_file.write(file_headers)
            image = "none"
            for index, item in enumerate(result_items):
                site = "Amazon"
                name = item.find_element_by_xpath(".//span[@class='a-size-base-plus a-color-base a-text-normal']")
                try:
                    link_element = item.find_element_by_xpath(".//a[@class='a-link-normal a-text-normal']")
                    link = link_element.get_attribute('href')
                except:
                    link = "link couldnt be found"
                try:
                    image = item.find_element_by_xpath(".//img[@class='s-image']").get_attribute('src')
                    # filename = "tempfiles/" + ctx.author.name + str(index) + ".png"
                    # urllib.request.urlretrieve(image, filename)
                except:
                    image = "none"
                try:
                    price_symbol = item.find_element_by_xpath(".//span[@class='a-price-symbol']")
                    price_whole = item.find_element_by_xpath(".//span[@class='a-price-whole']")
                    price_fraction = item.find_element_by_xpath(".//span[@class='a-price-fraction']")
                    price_final = price_symbol.text + str(price_whole.text) + "." + str(price_fraction.text)
                except:
                    price_final = 'The price could not be obtained'
                try:
                    rating = item.find_element_by_xpath(".//span[@class='a-icon-alt']").text
                    reviews = item.find_element_by_xpath(".//span[@class='a-size-base']").text
                    tech_file.write(site + "," + name.text.replace(",", "|") + "," + price_final + "," + "The "
                                                                                                         "rating"
                                                                                                         " is "
                                    + str(rating) + " with " + str(reviews) + " reviews " + link + "\n")
                except:
                    reviews = "could not find number of reviews"
                    tech_file.write(site + "," + name.text.replace(",",
                                                                   "|") + "," + price_final + "," + "Reviews could not be retrieved " + link + "\n")
                print(f"The {index}th item is named: {name.text}")
                results_list.insert(index, [name.text.replace(",", "|"), price_final, reviews, link, str(image)])

            time.sleep(2)
            print("-----closing the file-----")
            tech_file.close()
            embed = discord.Embed(title=ctx.author.name, description="Amazon search results", colour=0x9D34D1)
            if image != "none":
                embed.set_image(url=image)
            embed.add_field(name="Product name", value=results_list[0][0], inline=False)
            embed.add_field(name="Link", value=results_list[0][3], inline=False)
            embed.add_field(name="Price", value=results_list[0][1], inline=True)
            embed.add_field(name="Reviews", value=results_list[0][2], inline=True)
            text = "Showing result 1/" + str(len(results_list))
            embed.add_field(name="Result", value=text, inline=False)
            msg = await ctx.message.channel.send(embed=embed)
            await msg.add_reaction("⬅️")
            await msg.add_reaction("➡️")
            globalvars.user_results[ctx.author.id] = results_list
            globalvars.message_info[ctx.author.id] = [msg.id, time.time(), 0]
            print(globalvars.message_info[ctx.author.id])
            # Implement the loop to wait for the timer to expire here
            # await ctx.message.channel.send(file=discord.File('tech_products.csv', 'results.csv'))
        except:
            print("The results of the search were not found.")
            await ctx.message.channel.send("Results could not be found")


async def setup(client):
    await client.add_cog(WebScrape(client))
