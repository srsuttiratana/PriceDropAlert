import pymongo
import datetime
from datetime import datetime

def insert_data(item_list):
    # connect to your Atlas cluster
    client = pymongo.MongoClient('mongodb+srv://sarahsuttiratana:M5UtSEPIeJvhSxVu@cluster0.7pcov.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

    # get the database and collection on which to run the operation
    collection = client['price_drop_alert']['item_lookup']

    # create new documents
    item_documents = []

    for item in item_list:
        if item.type == 'Book':
            i = {
                    "product_id": item.product_id,
                    "price": item.price,
                    "datetime_created": datetime.now(),
                    "name": item.name,
                    "author": item.author,
                    "url": item.url,
                    "format": item.format,
                    "currency": item.currency,
                    "type" : item.type,
                    "seller" : item.seller
                }
            item_documents.append(i)
        elif item.type == 'Clothing':
            i = {
                    "product_id": item.product_id,
                    "price": item.price,
                    "datetime_created": datetime.now(),
                    "name": item.name,
                    "url": item.url,
                    "currency": item.currency,
                    "brand": item.brand,
                    "type" : item.type,
                    "seller" : item.seller
                }
            item_documents.append(i)
        elif item.type == 'Video Game':
            i = {
                    "product_id": item.product_id,
                    "price": item.price,
                    "datetime_created": datetime.now(),
                    "name": item.name,
                    "url": item.url,
                    "currency": item.currency,
                    "type" : item.type,
                    "seller" : item.seller,
                    "format" : item.format
                }
            item_documents.append(i)

    # insert documents
    collection.insert_many(item_documents)
    client.close()

def update_data(item):
    # connect to your Atlas cluster
    client = pymongo.MongoClient('mongodb+srv://sarahsuttiratana:M5UtSEPIeJvhSxVu@cluster0.7pcov.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

    # get the database and collection on which to run the operation
    collection = client['price_drop_alert']['amazon_item_lookup']

    # query documents
    query_filter = {'product_id' : '0593582128'}

    # update items
    update_operation = { '$set' :
        {
            "datetime_created": datetime.now()
        }
    }

    # insert documents
    result = collection.update_many(query_filter, update_operation)
    client.close()