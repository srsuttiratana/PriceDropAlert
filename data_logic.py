import pymongo
import datetime
from datetime import datetime
import PriceDropAlert.models as item
import PriceDropAlert.crud_data as crud_data

def insert_item(item):
    # connect to the Atlas cluster
    client = pymongo.MongoClient('mongodb+srv://sarahsuttiratana:M5UtSEPIeJvhSxVu@cluster0.7pcov.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

    try:
        # get the database and collection on which to run the operation
        collection = client['price_drop_alert']['amazon_item_lookup']

        #get the item using the isbn, get the latest entry
        latest_single_item = collection.find_one({"isbn": item.isbn}, {"isbn": 1, "datetime_created": 1, "price": 1}, sort=[('_id', pymongo.DESCENDING)])

        print(latest_single_item)

        #if the item's current price is less than the latest entry, then insert into the database
        if latest_single_item['price'] > item.price:
            crud_data.insert_data(item)
            #if the item's price difference is at least 10%, then print for now
            price_difference_percentage = ((latest_single_item['price'] - item.price) / latest_single_item['price'])
            if price_difference_percentage >= 0.10:
                print('The price difference is: ' + str(price_difference_percentage) + ', which is at least 10%')

        client.close()
    except Exception as e:
        raise Exception("Error retrieving documents: ", e)