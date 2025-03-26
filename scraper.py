from bs4 import BeautifulSoup
from selenium import webdriver

from selenium_stealth import stealth

from price_parser import Price

import models as item
import data_logic as data_logic
import copy

import tldextract
import re
from datetime import datetime

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
                    gamePrice = soup.find('div', attrs={'class': 'priceView-hero-price priceView-customer-price'})
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

def add_new_product_info(url):
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
    #connect to the URL
    driver.get(url)
    htmlMarkup = driver.page_source

    #get host name to determine the website
    extracted = tldextract.extract(url)
    hostname = extracted.domain.lower()

    soup = BeautifulSoup(htmlMarkup, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
    #print(soup.prettify())

    new_item = {}
    if hostname == 'uniqlo':
        new_item_brand = 'Uniqlo'
        new_item_type = 'Clothing'
        new_item_seller = 'Uniqlo'
        new_item_url = url
        new_item_price = 0.0
        new_item_currency = ''
        new_item_original_price = 0.0
        new_item_name = ''
        new_item_product_id = ''

        #fetch the product info
        try:
            clothing_info = soup.find('div', attrs={'id': 'root'})
            #get price and currency
            for row in clothing_info.find_all('p', attrs={'class': 'fr-ec-price-text fr-ec-price-text--large fr-ec-price-text--color-primary-dark fr-ec-text-transform-normal'}):
                price = Price.fromstring(row.text)
                print (price.amount_text)
                new_item_price = price.amount_float
                new_item_currency = price.currency
                new_item_original_price = price.amount_float
            #get product info
            for row in clothing_info.find_all('h1', attrs={'class': 'fr-ec-display fr-ec-display--color-primary-dark fr-ec-display--display5 fr-ec-text-align-left fr-ec-text-transform-normal'}):
                product_name = row.text
                print('Product Name: ' + product_name)
                new_item_name = product_name
            #get product ID
            for row in clothing_info.find_all('p', attrs={'class': 'fr-ec-caption fr-ec-caption--color-primary-dark fr-ec-text-align-left fr-ec-mb-spacing-04 fr-ec-caption--standard fr-ec-text-transform-normal'}):
                product_id = get_characters_after_text_string(row.text, 'Product ID: ')
                print('Product ID: ' + product_id)
                new_item_product_id = product_id
        except:
            print('Unable to retrieve product info for url: ' + url)
    
        #insert uniqlo item into database
        try:
            new_item = item.Clothing(datetime_created=datetime.now(), product_id=new_item_product_id, brand=new_item_brand, type=new_item_type, seller=new_item_seller, url=new_item_url, price=new_item_price, original_price=new_item_original_price, currency=new_item_currency, name=new_item_name)
            item_list_to_insert = [new_item]
            data_logic.insert_new_items(item_list_to_insert)
        except Exception as e:
            raise Exception("Error inserting new item: ", e)
    #create new item for Best Buy
    elif hostname == 'bestbuy':
        new_item_type = ''
        new_item_seller = 'Best Buy'
        new_item_url = url
        new_item_price = 0.0
        new_item_currency = ''
        new_item_original_price = 0.0
        new_item_name = ''
        new_item_product_id = ''
        new_item_format = ''

        #fetch the product info
        try:
            electronic_info = soup.find('div', attrs={'class': 'nav-container flex flex-xs-row'})
            print('electronic_info: ')
            #get type and format
            for row in electronic_info.find_all('a', attrs={'data-track': 'Breadcrumb'}):
                product_type = row.text
                print('Product Type: ' + product_type)
                if product_type != "":
                    product_type_lower = product_type.lower() 
                if "video game" in product_type_lower:
                    new_item_type = 'Video Game'
                    print('Item Type: ' + new_item_type)
                if "physical" in product_type_lower:
                    new_item_format = 'Physical'
                    print('Item Format: ' + new_item_format)
                if "digital" in product_type_lower:
                    new_item_format = 'Digital'
                    print('Item Format: ' + new_item_format)
            #get product info
            product_name_info = soup.find('div', attrs={'class': 'shop-product-title'})
            for row in product_name_info.find_all('div', attrs={'class': 'sku-title'}):
                product_name = row.text
                print('Product Name: ' + product_name)
                new_item_name = product_name
            #get product ID
            for row in product_name_info.find_all('div', attrs={'class': 'title-data lv esrb-layout'}):
                start_string = 'SKU:'
                end_string = 'Release Date'
                product_id = get_text_between(row.text, start_string, end_string).rstrip()
                print('Product ID: ' + product_id)
                new_item_product_id = product_id
            #get product price
            try:
                gamePrice = soup.find('div', attrs={'class': 'priceView-hero-price priceView-customer-price'})
                #print('Game Price: ')
                #print(gamePrice)
                for row in gamePrice.find_all('span', attrs={'aria-hidden': 'true'}):
                    price = Price.fromstring(row.text)
                    print (price.amount_text)
                    new_item_price = price.amount_float
                    new_item_currency = price.currency
                    new_item_original_price = price.amount_float
            except:
                print('Unable to retrieve price for: ' + new_item_name)
        except Exception as e:
            print('Unable to retrieve product info for url: ' + url)
            raise Exception('Error retrieving Best Buy item: ', e)
    
        #insert best buy item into database
        try:
            new_item = {}
            if new_item_type == 'Video Game':
                new_item = item.VideoGame(datetime_created=datetime.now(), product_id=new_item_product_id, format=new_item_format, type=new_item_type, seller=new_item_seller, url=new_item_url, price=new_item_price, original_price=new_item_original_price, currency=new_item_currency, name=new_item_name)
            if new_item != {}:
                item_list_to_insert = [new_item]
                data_logic.insert_new_items(item_list_to_insert)
        except Exception as e:
            raise Exception("Error inserting new item: ", e)

    driver.quit()

#helper function to get characters in text_input after a certain string (text_to_skip)
def get_characters_after_text_string(text_input, text_to_skip):
    # Regular expression to find characters after the specific string
    pattern = re.compile(rf'{text_to_skip}(.*)')

    # Search for the pattern in the text
    match = pattern.search(text_input)

    # Extract and print the characters after the specific string
    if match:
        result = match.group(1).strip()
        print(result)
        return result
    else:
        print("The specific string was not found.")
        return ''
    
#helper function to get characters in text_input between start_text_string and end_text_string
def get_text_between(input_string, start_string, end_string):
    # Create a regex pattern to match text between start_string and end_string
    pattern = re.escape(start_string) + r'(.*?)' + re.escape(end_string)
    
    # Search for the pattern in the input_string
    match = re.search(pattern, input_string)
    
    # If a match is found, return the captured group (text between start_string and end_string)
    if match:
        return match.group(1)
    else:
        return None