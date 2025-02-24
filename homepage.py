from fastapi import FastAPI
import pymongo
import PriceDropAlert.crud_data as crud_data
import PriceDropAlert.models as item
from datetime import datetime

sample_item = item.Item(author="America's Test Kitchen", isbn = "1940352649", name = "The Complete Mediterranean Cookbook: 500 Vibrant, Kitchen-Tested Recipes for Living and Eating Well Every Day (The Complete ATK Cookbook Series)", price = 17.00, url = "https://www.amazon.com/Complete-Mediterranean-Cookbook-Vibrant-Kitchen-Tested/dp/1940352649/", datetime_created = datetime.now())

crud_data.insert_data(sample_item)
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