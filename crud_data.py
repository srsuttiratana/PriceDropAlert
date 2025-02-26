import pymongo
import datetime
from datetime import datetime

def insert_data(item_list):
    # connect to your Atlas cluster
    client = pymongo.MongoClient('mongodb+srv://sarahsuttiratana:M5UtSEPIeJvhSxVu@cluster0.7pcov.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

    # get the database and collection on which to run the operation
    collection = client['price_drop_alert']['amazon_item_lookup']

    # create new documents
    cookbookDocuments = []

    for item in item_list:
        i = {
                "isbn": item.isbn,
                "price": item.price,
                "datetime_created": item.datetime_created,
                "name": item.name,
                "author": item.author,
                "url": item.url
            }
        cookbookDocuments.append(i)

    # insert documents
    collection.insert_many(cookbookDocuments)
    client.close()

def update_data(item):
    # connect to your Atlas cluster
    client = pymongo.MongoClient('mongodb+srv://sarahsuttiratana:M5UtSEPIeJvhSxVu@cluster0.7pcov.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

    # get the database and collection on which to run the operation
    collection = client['price_drop_alert']['amazon_item_lookup']

    # query documents
    query_filter = {'isbn' : '0593582128'}

    # update items
    update_operation = { '$set' :
        {
            "datetime_created": datetime.now()
        }
    }

    # insert documents
    result = collection.update_many(query_filter, update_operation)
    client.close()