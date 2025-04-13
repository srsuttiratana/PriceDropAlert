from fastapi import FastAPI
import pymongo
import models as item
from datetime import datetime
import scraper
import models
import data_logic

from save_logs import Logger

# connect to the Atlas cluster
client = pymongo.MongoClient('mongodb+srv://sarahsuttiratana:M5UtSEPIeJvhSxVu@cluster0.7pcov.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

list_of_items = []
try:
    # get the database and collection on which to run the operation
    collection = client['price_drop_alert']['item_lookup']

    all_items = [
        {
            '$sort': {'id': -1}  # Sort by id in descending order
        },
        {
            '$group': {
                '_id': '$product_id',  # Group by the field you want distinct values for
                'latestEntry': {'$last': '$$ROOT'}  # Get the latest entry for each group
            }
        },
        {
            '$replaceRoot': {'newRoot': '$latestEntry'}  # Replace the root with the latest entry document
        }
    ]

    result = list(collection.aggregate(all_items))

    for i in result:
        i['id'] = str(i.pop('_id'))
        i['type'] = str(i.pop('type'))
        item_temp = {}
        if i['type'] == 'Book':
            item_temp = item.Book(**i)
        elif i['type'] == 'Clothing':
            item_temp = item.Clothing(**i)
        elif i['type'] == 'Video Game':
            item_temp = item.VideoGame(**i)
        print('item_temp: ')
        print(item_temp)
        
        if item_temp:
            list_of_items.append(item_temp)
    client.close()
    scraper.get_price(list_of_items)

except Exception as e:
    Logger.add_log(product_id=item.product_id, url=item.url, subject='Not Able to Retrieve Price', exception=e)
    Logger.insert_logs()
    raise Exception("Error retrieving documents: ", e)

app = FastAPI()

@app.get("/")

async def root(): 

    #for c in collection:
    #    print(c)
    #return {"message": "Welcome to the Price Drop Alert App!"}
    return list_of_items