from bs4 import BeautifulSoup
from selenium import webdriver

from selenium_stealth import stealth

from price_parser import Price

import models as item
import data_logic as data_logic
import copy

def get_price(item_list):
    options = webdriver.ChromeOptions()

    options.add_argument("--headless")

    # start a Chrome instance

    driver = webdriver.Chrome(options=options)

    # configure the WebDriver to avoid bot detection

    # with Selenium Stealth

    stealth(

    driver,

    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",

    languages=["en-US", "en"],

    vendor="Google Inc.",

    platform="Win32",

    webgl_vendor="Intel Inc.",

    renderer="Intel Iris OpenGL Engine",

    fix_hairline=True,

    )

    item_list_to_insert = []
    for item in item_list:
        #connect to the URL
        driver.get(item.url)
        htmlMarkup = driver.page_source

        soup = BeautifulSoup(htmlMarkup, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
        #print(soup.prettify())

        if item.type == 'Book':
            if item.format == 'Hardcover':
                try:
                    hardcoverPrice = soup.find('div', attrs = {'id':'tmm-grid-swatch-HARDCOVER'}) 
                    print(hardcoverPrice)
                    for row in hardcoverPrice.find_all('span', attrs = {'class':'slot-price'}):
                        price = Price.fromstring(row.text)
                        print(price.amount_text)
                        if item.price > price.amount_float:
                            item.price = price.amount_float
                            item_list_to_insert.append(item)
                except:
                    print('Unable to retrieve price for: ' + item.name)

        elif item.type == 'Clothing':
            if item.seller == 'Vuori':
                try: 
                    clothingPrice = soup.find('main', attrs={'id': 'main-content'})
                    #print('Clothing Price: ')
                    #print(clothingPrice)
                    for row in clothingPrice.find_all('h3', attrs={'data-testid': 'productdescriptionprice-price'}):
                        price = Price.fromstring(row.text)
                        print (price.amount_text)
                        if item.price > price.amount_float:
                            item.price = price.amount_float
                            item_list_to_insert.append(item)
                except:
                    print('Unable to retrieve price for: ' + item.name)
            elif item.seller == 'Uniqlo':
                try:
                    clothingPrice = soup.find('div', attrs={'id': 'root'})
                    #print('Clothing Price: ')
                    #print(clothingPrice)
                    for row in clothingPrice.find_all('p', attrs={'class': 'fr-ec-price-text fr-ec-price-text--large fr-ec-price-text--color-primary-dark fr-ec-text-transform-normal'}):
                        price = Price.fromstring(row.text)
                        print (price.amount_text)
                        if item.price > price.amount_float:
                            deep_copy_item = copy.deepcopy(item)
                            deep_copy_item.price = price.amount_float
                            item_list_to_insert.append(deep_copy_item)
                except:
                    print('Unable to retrieve price for: ' + item.name)
        elif item.type == 'Video Game':
            if item.seller == 'Best Buy':
                try:
                    gamePrice = soup.find('div', attrs={'class': 'pricing-price'})
                    #print('Game Price: ')
                    #print(gamePrice)
                    for row in gamePrice.find_all('span', attrs={'aria-hidden': 'true'}):
                        price = Price.fromstring(row.text)
                        print (price.amount_text)
                        if item.price > price.amount_float:
                            deep_copy_item = copy.deepcopy(item)
                            deep_copy_item.price = price.amount_float
                            item_list_to_insert.append(deep_copy_item)
                except:
                    print('Unable to retrieve price for: ' + item.name)
    
    if len(item_list_to_insert) > 0:
        data_logic.insert_items(item_list_to_insert, item_list)

    # get the current window size

    #original_size = driver.get_window_size()

    # get the body width and height

    #full_width = driver.execute_script("return document.body.parentNode.scrollWidth")

    #full_height = driver.execute_script("return document.body.parentNode.scrollHeight")

    # set the browser window to the body width and height

    #driver.set_window_size(full_width, full_height)

    # take a screenshot of the entire page

    #driver.save_screenshot("screenshot.png")

    # restore the original window size

    #driver.set_window_size(original_size["width"], original_size["height"])

    # close the browser and release its resources

    driver.quit()
