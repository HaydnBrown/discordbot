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


class WebScrape(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.PATH = "/home/haydn/chromedriver.exe"
        self.driver = webdriver.Chrome()
        self.tech_filename = "tech_products.csv"

    @commands.command()
    async def find_tech(self, ctx, *search_items):
        search_item = ""
        for i in search_items:
            search_item = search_item + i + " "

        tech_file = open(self.tech_filename, "w")
        self.driver.get("https://www.amazon.ca/")
        print(self.driver.title)
        search_bar = self.driver.find_element_by_id("twotabsearchtextbox")
        search_bar.send_keys(search_item)
        search_bar.send_keys(Keys.RETURN)
        try:
            print("we made it to the search page")
            # print("Hello1")
            results = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='s-main-slot s-result-list s-search-results "
                                                          "sg-row']"))
            )
            # print("Hello2")
            result_items = results.find_elements_by_xpath(".//div[@class='sg-col-4-of-24 sg-col-4-of-12 sg-col-4-of-36 "
                                                          "s-result-item s-asin sg-col-4-of-28 sg-col-4-of-16 sg-col "
                                                          "sg-col-4-of-20 sg-col-4-of-32']")
            # print("Hello3")
            print("number of items on page 1: " + str(len(result_items)))
            file_headers = "website, product_name, price, reviews\n"
            tech_file.write(file_headers)
            for index, item in enumerate(result_items):
                site = "Amazon"
                name = item.find_element_by_xpath(".//span[@class='a-size-base-plus a-color-base a-text-normal']")
                try:
                    price_whole = item.find_element_by_xpath(".//span[@class='a-price-whole']")
                    price_final = str(price_whole.text)
                except:
                    price_final = 'The price could not be obtained'
                try:
                    rating = item.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div[2]/div/span[3]/div["
                                                        "2]/div[2]/div/span/div/div/div[3]/div/span[1]/span/a/i["
                                                        "1]/span").text
                    reviews = item.find_element_by_xpath(".//span[@class='a-size-base']").text
                    tech_file.write(site + "," + name.text.replace(",", "|") + "," + price_final + "," + "The "
                                                                                                         "rating"
                                                                                                         " is "
                                    + str(rating) + " with " + str(reviews.replace(",", "")) + " reviews" + "\n")
                except:
                    tech_file.write(site + "," + name.text.replace(",",
                                                                   "|") + "," + price_final + "," + "Reviews could not be retrieved" + "\n")
                print(f"The {index}th item is named: {name.text}")
                if index==5:
                    break

            time.sleep(5)
            print("items obtained from amazon")
        except:
            print("The results of the search were not found.")
            tech_file.write("The search results from Amazon were not obtained")
        finally:
            print("done gathering from amazon")

        # now search newegg for same item
        self.driver.get("https://www.newegg.ca/")
        print(self.driver.title)
        search_bar = self.driver.find_element_by_id("SearchBox2020")
        search_bar.send_keys(search_item)
        search_bar.send_keys(Keys.RETURN)
        try:
            print("we made it to the item page")
            results = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='item-cells-wrap border-cells items-grid-view "
                                                          "four-cells expulsion-one-cell']"))
            )
            result_items = results.find_elements_by_xpath(".//div[@class='item-container']")
            print("number of items on page 1: " + str(len(result_items)))
            for index, item in enumerate(result_items):
                site = "Newegg"
                name = item.find_element_by_xpath(".//a[@class='item-title']")
                try:
                    price_final = str(item.find_element_by_xpath(".//li[@class='price-current']/strong").text)
                except:
                    price_final = 'The price could not be obtained'
                try:
                    reviews = item.find_element_by_xpath(".//span[@class='item-rating-num']").text
                    tech_file.write(site + "," + name.text.replace(",", "|") + "," + price_final + "," + "There are " + str(reviews.replace(",", "")) + " reviews" + "\n")
                except:
                    tech_file.write(site + "," + name.text.replace(",",
                                                                   "|") + "," + price_final + "," + "Reviews could not be retrieved" + "\n")
                print(f"The {index}th item is named: {name.text}")
                if index==5:
                    break

            time.sleep(5)
            print("items obtained from newegg")
        except:
            print("The results of the search were not found.")
            tech_file.write("The search results from Newegg were not obtained")
        finally:
            print("done gathering from newegg")

        # now search canada computers for same item
        self.driver.get("https://www.canadacomputers.com/")
        print(self.driver.title)
        search_bar = self.driver.find_element_by_id("cc_quick_search")
        search_bar.send_keys(search_item)
        search_bar.send_keys(Keys.RETURN)
        try:
            print("made it to the search result page")
            results = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.ID, "product-list"))
            )
            result_items = results.find_elements_by_xpath(".//div[@class='col-xl-3 col-lg-4 col-6 mt-0_5 px-0_5 "
                                                          "toggleBox mb-1']")
            print("number of items on page 1: " + str(len(result_items)))
            file_headers = "website, product_name, price, reviews\n"
            for index, item in enumerate(result_items):
                site = "Canada Computers"
                name = item.find_element_by_xpath(".//a[@class='text-dark text-truncate_3']")
                try:
                    price_final = str(item.find_element_by_xpath("/html/body/main/div[2]/section/div[3]/div["
                                                                 "2]/div/div/div[1]/div/div[2]/span["
                                                                 "3]/strong").text)
                except:
                    price_final = 'The price could not be obtained'
                tech_file.write(site + "," + name.text.replace(",", "|") + "," + price_final + "," + "Reviews could not be retrieved" + "\n")
                print(f"The {index}th item is named: {name.text}")
                if index == 5:
                    break

            time.sleep(5)
            print("items obtained from Canada Computers")
        except:
            print("The results of the search were not found.")
            tech_file.write("The search results from Canada Computers were not obtained")
        finally:
            print("-----closing the file, end of function-----")
            tech_file.close()
            await ctx.message.channel.send(file=discord.File('tech_products.csv', 'results.csv'))

    @commands.command()
    async def scrape_test(self, ctx):
        print("web scraper cog is working")


def setup(client):
    client.add_cog(WebScrape(client))
