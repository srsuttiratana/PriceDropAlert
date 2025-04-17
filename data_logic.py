import pymongo
import crud_data
import models as item
import send_email

from datetime import datetime

from save_logs import Logger
import copy

log_list_to_insert = []

def insert_item(item):
    # connect to the Atlas cluster
    client = pymongo.MongoClient('mongodb+srv://sarahsuttiratana:M5UtSEPIeJvhSxVu@cluster0.7pcov.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

    try:
        # get the database and collection on which to run the operation
        collection = client['price_drop_alert']['item_lookup']

        #get the item using the product_id, get the latest entry
        latest_single_item = collection.find_one({"product_id": item.product_id}, {"product_id": 1, "datetime_created": 1, "price": 1}, sort=[('_id', pymongo.DESCENDING)])

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
    
def insert_items(item_list_to_insert):
    # connect to the Atlas cluster
    client = pymongo.MongoClient('mongodb+srv://sarahsuttiratana:M5UtSEPIeJvhSxVu@cluster0.7pcov.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

    item_insert_list = []
    try:
        # get the database and collection on which to run the operation
        #collection = client['price_drop_alert']['item_lookup']

        #get list of product_ids
        #product_id_list = [item.product_id for item in item_list]

        #fields_to_query = {"product_id": 1, "price": 1, "datetime_created": 1}
        #get the items using the product_ids, get the latest entries
        latest_item_map = {}
        #latest_item_list = collection.find({"product_id": {"$in": product_id_list}}, fields_to_query, sort=[('_id', pymongo.DESCENDING)])
        # get the database and collection on which to run the operation
        collection = client['price_drop_alert']['item_lookup']

        all_items = [
            {
                '$sort': {'id': -1}  # Sort by id in descending order
            },
            {
                '$group': {
                    '_id': {
                        'product_id': '$product_id',  # Group by the field you want distinct values for
                        'email': '$email'
                    },
                    'latestEntry': {'$last': '$$ROOT'}  # Get the latest entry for each group
                }
            },
            {
                '$replaceRoot': {'newRoot': '$latestEntry'}  # Replace the root with the latest entry document
            }
        ]

        latest_items_with_email = list(collection.aggregate(all_items))

        #create map of items from the database with product_id as the key
        for i in latest_items_with_email:
            i['id'] = str(i.pop('_id'))
            i['type'] = str(i.pop('type'))
            item_temp = {}
            if i['type'] == 'Book':
                item_temp = item.Book(**i)
            elif i['type'] == 'Clothing':
                item_temp = item.Clothing(**i)
            elif i['type'] == 'Video Game':
                item_temp = item.VideoGame(**i)
            print('item_temp 2: ')
            print(item_temp)
        
            if item_temp:
                if (item_temp.product_id) not in latest_item_map.keys():
                    latest_item_map[item_temp.product_id] = [item_temp]
                else:
                    latest_item_map[item_temp.product_id].append(item_temp)

        email_alert_list = []

        #if the item's current price is less than the latest entry, then insert into the database
        for i in item_list_to_insert:
            #get the latest entries of the item, and if it doesn't exist, then set value to 'Default'
            latest_items = latest_item_map.get(i.product_id, 'Default')
            #the item exists in the database
            if latest_items != 'Default': 
                #update price for all entries with the same product id but with different emails
                for li in latest_items:
                    if li.price > i.price:
                        #if the item's price difference is at least 10%, then print for now
                        price_difference_percentage = ((li.price - i.price) / li.price)
                        deep_copy_item = copy.deepcopy(li)
                        deep_copy_item.price = i.price
                        item_insert_list.append(deep_copy_item)
                        if price_difference_percentage >= 0.10:
                            print('The price difference is: ' + str(price_difference_percentage) + ', which is at least 10%')
                            #email_alert_item = models.AlertEmailItem(i.name, i.url, i.price, latest_item.price, i.currency)
                            email_alert_item = item.AlertEmailItem(deep_copy_item.name, deep_copy_item.url, deep_copy_item.price, deep_copy_item.original_price, deep_copy_item.currency, deep_copy_item.email)
                            email_alert_list.append(email_alert_item)
            #the item does not currently exist in the database
            else:
                #insert the new item into the database
                item_insert_list.append(i)
        #insert items if there are new entries or items where there is an acceptable discount percentage
        if (len(item_insert_list) > 0):
            crud_data.insert_data(item_insert_list)
        if (len(email_alert_list) > 0):
            send_email.send_mail(email_alert_list)
        client.close()
    except Exception as e:
        print('Unable to insert items: ', e)
        Logger.add_log(product_id='', url='', subject='Unable to insert items', exception=e)

    Logger.insert_logs()
    
def insert_new_items(item_list):
    try:
        crud_data.insert_data(item_list)
    except Exception as e:
        raise Exception("Error inserting new items: ", e)