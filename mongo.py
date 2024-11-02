from pymongo import MongoClient, ReturnDocument
from datetime import datetime
from dotenv import load_dotenv
import os
from bson import ObjectId
# set a string equal to the contents of mongodbpassword.txt
load_dotenv()
connection_string = os.getenv("MONGO")

def add_feed(input_data):
    uri = connection_string
    client = MongoClient(uri)
    db = client["Election"]
    collection = db["States"]
    
    try:
        # Upsert the input data into the collection
        collection.replace_one({'url': input_data['url']}, input_data, upsert=True)
        print("Input data upserted successfully.")
    except Exception as e:
        print("An error occurred:", e)

# Call the function to execute it
# add_feed()

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


# get_feed()

def delete_feed():
    uri = connection_string
    client = MongoClient(uri)
    db = client["Election"]
    collection = db["test"]
    
    try:
        # Delete all documents in the collection
        result = collection.delete_many({})
        print(f"Deleted {result.deleted_count} documents.")
    except Exception as e:
        print("An error occurred:", e)
# delete_feed()
# get_feed()