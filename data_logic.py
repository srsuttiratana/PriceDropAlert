import pymongo
import PriceDropAlert.crud_data as crud_data

def insert_item(item):
    # connect to the Atlas cluster
    client = pymongo.MongoClient('mongodb+srv://sarahsuttiratana:M5UtSEPIeJvhSxVu@cluster0.7pcov.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

    try:
        # get the database and collection on which to run the operation
        collection = client['price_drop_alert']['amazon_item_lookup']

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
    
def insert_items(item_list):
    # connect to the Atlas cluster
    client = pymongo.MongoClient('mongodb+srv://sarahsuttiratana:M5UtSEPIeJvhSxVu@cluster0.7pcov.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

    try:
        # get the database and collection on which to run the operation
        #collection = client['price_drop_alert']['amazon_item_lookup']
        collection = client['price_drop_alert']['uniqlo_item_lookup']

        #get list of product_ids
        product_id_list = [item.product_id for item in item_list]

        fields_to_query = {"product_id": 1, "price": 1, "datetime_created": 1}
        #get the items using the product_ids, get the latest entries
        latest_item_map = {}
        latest_item_list = collection.find({"product_id": {"$in": product_id_list}}, fields_to_query, sort=[('_id', pymongo.DESCENDING)])

        #create map of items from the database with product_id as the key
        for i in latest_item_list:
            if i['product_id'] not in latest_item_map.keys():
                latest_item_map[i['product_id']] = i 

        item_insert_list = []

        #if the item's current price is less than the latest entry, then insert into the database
        for i in item_list:
            #get the latest entry of the item, and if it doesn't exist, then set value to 'Default'
            latest_item = latest_item_map.get(i.product_id, 'Default')
            #the item exists in the database
            if latest_item != 'Default':   
                if latest_item['price'] > i.price:
                    #if the item's price difference is at least 10%, then print for now
                    price_difference_percentage = ((latest_item['price'] - i.price) / latest_item['price'])
                    item_insert_list.append(i)
                    if price_difference_percentage >= 0.10:
                        print('The price difference is: ' + str(price_difference_percentage) + ', which is at least 10%')
            #the item does not currently exist in the database
            else:
                #insert the new item into the database
                item_insert_list.append(i)
        #insert items if there are new entries or items where there is an acceptable discount percentage
        if (len(item_insert_list) > 0):
            crud_data.insert_data(item_insert_list)
        client.close()
    except Exception as e:
        raise Exception("Error retrieving documents: ", e)