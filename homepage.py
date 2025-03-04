from fastapi import FastAPI
import pymongo
import PriceDropAlert.data_logic as data_logic
import PriceDropAlert.models as item
from datetime import datetime
import PriceDropAlert.scraper as scraper

sample_item1 = item.Item(author="America's Test Kitchen", isbn = "1940352649", name = "The Complete Mediterranean Cookbook: 500 Vibrant, Kitchen-Tested Recipes for Living and Eating Well Every Day (The Complete ATK Cookbook Series)", price = 10.00, url = "https://www.amazon.com/Complete-Mediterranean-Cookbook-Vibrant-Kitchen-Tested/dp/1940352649/", datetime_created = datetime.now())
sample_item2 = item.Item(author="Suzy Karadsheh", isbn = "0593234278", name = "The Mediterranean Dish: 120 Bold and Healthy Recipes You'll Make on Repeat: A Mediterranean Cookbook", price = 10.00, url = "https://www.amazon.com/Mediterranean-Dish-Healthy-Recipes-Cookbook/dp/0593234278/", datetime_created = datetime.now())

sample_item_list = [sample_item1, sample_item2]

#data_logic.insert_items(sample_item_list)

scraper.get_price()
# connect to the Atlas cluster
client = pymongo.MongoClient('mongodb+srv://sarahsuttiratana:M5UtSEPIeJvhSxVu@cluster0.7pcov.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

listOfBooks = ""
try:
    # get the database and collection on which to run the operation
    collection = client['price_drop_alert']['amazon_item_lookup']

    all_items = collection.find({})

    for i in all_items:
        #listOfBooks = listOfBooks + i.name + "\n"
        print(i)
    client.close()

except Exception as e:
    raise Exception("Error retrieving documents: ", e)

app = FastAPI()

@app.get("/")

async def root(): 

    #for c in collection:
    #    print(c)
    #return {"message": "Welcome to the Price Drop Alert App!"}
    return listOfBooks