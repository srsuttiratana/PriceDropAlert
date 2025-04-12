import pymongo
import datetime
from datetime import datetime

#to insert error logs into database
def insert_log_data(log_list):
    # connect to your Atlas cluster
    client = pymongo.MongoClient('mongodb+srv://sarahsuttiratana:M5UtSEPIeJvhSxVu@cluster0.7pcov.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

    # get the database and collection on which to run the operation
    collection = client['price_drop_alert']['logs']

    # create new log documents
    log_documents = []

    for log in log_list:
        l = {
                "product_id": log.product_id,
                "datetime_created": datetime.now(),
                "url": log.url,
                "subject": log.subject,
                "exception_type": log.exception_type,
                "error_message" : log.error_message
            }
        log_documents.append(l)

    # insert log documents
    collection.insert_many(log_documents)
    client.close()