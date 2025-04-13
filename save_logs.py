import pymongo
import datetime
from datetime import datetime

import models

class Logger:
    log_list_to_insert = []

    def __init__(self):
        self.log_list_to_insert = []

    @classmethod
    #for adding new error logs
    def add_log(cls, exception, product_id = '', url = '', subject = ''):
        try:
            cls.log_list_to_insert.append(models.Log(datetime_created=datetime.now(), product_id=product_id, url=url, subject=subject, exception_type=str(exception), error_message=repr(exception)))
        except Exception as e:
            raise Exception("Error adding new logs: ", e)

    @classmethod
    #for inserting new error logs
    def insert_logs(cls):
        try:
            if len(cls.log_list_to_insert) > 0:
                cls.insert_log_data(cls.log_list_to_insert)
                #clear out log list
                cls.log_list_to_insert = []
        except Exception as e:
            raise Exception("Error inserting new logs: ", e)

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