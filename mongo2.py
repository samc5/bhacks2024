from pymongo import MongoClient, ReturnDocument
from datetime import datetime
from dotenv import load_dotenv
import os
from bson import ObjectId
# set a string equal to the contents of mongodbpassword.txt
load_dotenv()
connection_string = os.getenv("MONGO")

def get_feed():
    uri = connection_string
    client = MongoClient(uri)
    db = client["Election"]
    collection = db["test"]
    
    try:
        # Find all documents in the collection
        documents = collection.find()
        
        # Print each document
        for document in documents:
            print(document)
    except Exception as e:
        print("An error occurred:", e)

get_feed()


def convert_to_date(date_str):
    formats = ['%a, %d %b %Y %H:%M:%S', '%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%SZ',
    '%Y-%m-%dT%H:%M:%S%z','%Y-%m-%d %H:%M:%S',       
    '%Y-%m-%dT%H:%M:%S.%f%z', '%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%dT%H:%M:%S.000Z',
    '%Y-%b-%d %H:%M:%S',    
    '%Y-%B-%d %H:%M:%S',  '%Y-%m-%dT%H:%M:%S.%fZ', 'Y-%m-%dT%H:%M:%SZ', '%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%dT%H:%M:%S+00:00'      
    ]
    #2024-05-21T14:04:52+00:00
    if date_str:
        if ' ' in date_str:
            date_str = date_str[:date_str.rindex(' ')]
        if date_str == '':
            return datetime.utcfromtimestamp(0)
    for date_format in formats:
        try:
            datetime_object = datetime.strptime(date_str, date_format)
            return datetime_object
        except ValueError:
       #     print(f"bad: {date_str}, {date_format}")
            continue
    return datetime.utcfromtimestamp(0)