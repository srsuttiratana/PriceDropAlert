from fastapi import FastAPI
import pymongo
import PriceDropAlert.data_logic as data_logic
import PriceDropAlert.models as item
from datetime import datetime
import PriceDropAlert.scraper as scraper

# connect to the Atlas cluster
client = pymongo.MongoClient('mongodb+srv://sarahsuttiratana:M5UtSEPIeJvhSxVu@cluster0.7pcov.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

list_of_items = []
try:
    # get the database and collection on which to run the operation
    #collection = client['price_drop_alert']['amazon_item_lookup']
    collection = client['price_drop_alert']['uniqlo_item_lookup']

    all_items = collection.find({})

    for i in all_items:
        i['id'] = str(i.pop('_id'))
        i['type'] = str(i.pop('type'))
        item_temp = {}
        if i['type'] == 'Book':
            item_temp = item.Book(**i)
        elif i['type'] == 'Clothing':
            item_temp = item.Clothing(**i)
        print('item_temp: ')
        print(item_temp)
        
        if item_temp:
            list_of_items.append(item_temp)
    client.close()
    scraper.get_price(list_of_items)

except Exception as e:
    raise Exception("Error retrieving documents: ", e)

app = FastAPI()

@app.get("/")

async def root(): 

    #for c in collection:
    #    print(c)
    #return {"message": "Welcome to the Price Drop Alert App!"}
    return list_of_items