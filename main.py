import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import json
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

engine = create_engine('sqlite:///Products.db', echo=True)
meta = MetaData()

products = Table(
    "products", meta,
    Column("id", Integer, primary_key=True),
    Column("Title", String, nullable=False),
    Column("img_URL", String),
    Column("Price", String),
    Column("Product_Details", String),
)
# meta.create_all(engine) # # commented after creating the tables

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# # Change the path according to where the chrome webdriver is installed on your system

chrome_driver_path = Service(r"D:\viji\Aries\Development\chromedriver.exe")

bot = webdriver.Chrome(service=chrome_driver_path, options=chrome_options)

dicts_list = []

data = pd.read_csv("Amazon Scraping - Sheet1.csv")
# # change the range to your choice to scrape the no of URLS you want
for i in range(0, 200):
    pdt_title = ""
    pdt_img_url = ""
    pdt_price = ""
    pdt_description = []
    row = data.iloc[i]
    country = row.country
    asin = row.Asin
    URL = f"https://www.amazon.{country}/dp/{asin}"

    bot.get(URL)

    time.sleep(2)

    try:
        cookies_accept = bot.find_element("name", "accept")
        cookies_accept.click()

    except NoSuchElementException:
        try:
            time.sleep(2)
            title = bot.find_element("id", "productTitle")
        except NoSuchElementException:
            print(f"{URL} not available")
            time.sleep(2)
            pass
        else:
            pdt_title = title.text

            time.sleep(2)

            img_url = bot.find_element("css selector", "div#leftCol div#main-image-container img")
            pdt_img_url = img_url.get_attribute("src")
            time.sleep(2)

            try:
                price = bot.find_element("css selector", "div#centerCol div#formats a span.a-color-base")
                time.sleep(2)
            except NoSuchElementException:
                price = bot.find_element(
                    "css selector",
                    "div#centerCol div#corePriceDisplay_desktop_feature_div span.priceToPay span.a-price"
                )
                pdt_price = price.text
                time.sleep(2)
            else:
                if not price:
                    price = bot.find_element(
                        "css selector",
                        "div#centerCol div#corePriceDisplay_desktop_feature_div span.a-price"
                    )
                    pdt_price = price.text
                    time.sleep(2)
                else:
                    pdt_price = price.text

            try:
                description = bot.find_elements("css selector",
                                                "div#detailBullets_feature_div  div#detailBullets_feature_div li")
                time.sleep(2)
            except NoSuchElementException:
                description = bot.find_elements("css selector", "div#feature-bullets span.a-list-item")
                time.sleep(2)
                pdt_description = [item.text for item in description]
            else:
                if not description:
                    description = bot.find_elements("css selector", "div#feature-bullets span.a-list-item")

                    pdt_description = [item.text for item in description]
                else:
                    pdt_description = [item.text for item in description]

            time.sleep(2)

    else:
        time.sleep(4)
        title = bot.find_element("id", "productTitle")
        pdt_title = title.text

        time.sleep(1)

        img_url = bot.find_element("css selector", "div#leftCol div#main-image-container img")
        pdt_img_url = img_url.get_attribute("src")
        time.sleep(2)

        try:
            price = bot.find_element("css selector", "div#centerCol div#formats a span.a-color-base")
            time.sleep(2)
        except NoSuchElementException:
            price = bot.find_element(
                "css selector",
                "div#centerCol div#corePriceDisplay_desktop_feature_div span.a-price"
            )
            pdt_price = price.text
            time.sleep(2)
        else:
            if not price:
                price = bot.find_element(
                    "css selector",
                    "div#centerCol div#corePriceDisplay_desktop_feature_div span.a-price"
                )
                pdt_price = price.text
                time.sleep(2)
            else:
                pdt_price = price.text

        try:
            description = bot.find_elements("css selector",
                                            "div#detailBullets_feature_div  div#detailBullets_feature_div li")
            time.sleep(2)
        except NoSuchElementException:
            description = bot.find_elements("css selector", "div#feature-bullets span.a-list-item")
            time.sleep(2)
            pdt_description = [item.text for item in description]
        else:
            if not description:
                description = bot.find_elements("css selector", "div#feature-bullets span.a-list-item")

                pdt_description = [item.text for item in description]
            else:
                pdt_description = [item.text for item in description]

        time.sleep(2)

    data_dict = {
        "Title": pdt_title,
        "Img_URL": pdt_img_url,
        "Price": pdt_price,
        "Product Details": pdt_description,
    }

    if pdt_title != "":
        dicts_list.append(data_dict)

        add_to_db = products.insert().values(
            Title=pdt_title,
            img_URL=pdt_img_url,
            Price=pdt_price,
            Product_Details="\n".join(pdt_description)
        )
        conn = engine.connect()
        result = conn.execute(add_to_db)

json_object = json.dumps({"data": dicts_list}, indent=4)

with open("output.json", "w") as file:
    file.write(json_object)
