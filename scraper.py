from bs4 import BeautifulSoup
from selenium import webdriver

from selenium_stealth import stealth

def get_price():
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

    # connect to the target page

    #the below URL works!
    #driver.get("https://vuoriclothing.com/products/womens-performance-jogger-black-heather?variant=39975074660455&msclkid=54f1bccea82817c3d8dddb0d19f8da6a&utm_source=bing&utm_medium=cpc&utm_campaign=WP_Bing_USA_Shopping_Nonbrnd_Shopping_C_FF_Womens_Active&utm_term=4578160299221560&utm_content=All")
    driver.get("https://www.amazon.com/Complete-Mediterranean-Cookbook-Gift-Kitchen-Tested/dp/1948703947/ref=tmm_hrd_swatch_0")

    htmlMarkup = driver.page_source

    soup = BeautifulSoup(htmlMarkup, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib

    hardcoverPrice = soup.find('div', attrs = {'id':'tmm-grid-swatch-HARDCOVER'}) 
    for row in hardcoverPrice.find_all('span', attrs = {'class':'slot-price'}):
        print(row.text)

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
