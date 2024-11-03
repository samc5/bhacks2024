from pymongo import MongoClient, ReturnDocument
from datetime import datetime
from dotenv import load_dotenv
import os, json, requests
from mongoadd import *
# set a string equal to the contents of mongodbpassword.txt
load_dotenv()
connection_string = os.getenv("MONGO")

candidate_ids = {
    'Kamala Harris': '64984',
    'Donald Trump': '8639'
}

states = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]


def add_feed():
    add_new_election_data()

# Call the function to execute it
# add_feed()

def get_feed(state=None):
    uri = connection_string
    client = MongoClient(uri)
    db = client["Election"]
    collection = db["States"]
    
    try:
        # Find documents based on the state
        if state is None:
            documents = collection.find()
        else:
            documents = collection.find({"statePostal": state})
        # Print each document
        
        return documents
    except Exception as e:
        print("An error occurred:", e)



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

def get_candidate_percentage(candidate_id, state):
    if state not in states:
        print("Invalid state code")
        return 0
    if candidate_id not in candidate_ids and candidate_id not in candidate_ids.values():
        print("Invalid candidate ID")
        return 0
    def get_candidate_info(candidate_id, state):
        try:
            candidate_idint = int(candidate_id)
        except:
            candidate_id = candidate_ids[candidate_id]
        candidate_list = list(get_feed(state))[0]["candidates"]
        candidate_info = next((candidate for candidate in candidate_list if candidate['candidateID'] == candidate_id), None)
        if candidate_info:
            return candidate_info, candidate_list.index(candidate_info), state
        else:
            print(f"No candidate found with ID {candidate_id}")

    def get_total_votes(candidate_id, state):
        candidate_info, candidate_index, state = get_candidate_info(candidate_id, state)
        if candidate_info:
            candidate_list = list(get_feed(state))[0]["candidates"]
            total_votes = sum(candidate['voteCount'] for candidate in candidate_list)
            return total_votes
        else:
            return 0

    def get_candidate_votes(candidate_id, state):
        candidate_info, candidate_index, state = get_candidate_info(candidate_id, state)
        if candidate_info:
            return candidate_info['voteCount']
        else:
            return 0
    #the candidate_id is the same across the three functions

    def get_candidate_proportion(votecount, totalcount):
        return round(abs((votecount[0] / totalcount)), 2) if totalcount != 0 else 0.5

    return (get_candidate_proportion(get_candidate_votes(candidate_id, state), get_total_votes(candidate_id, state)), state)

print(get_candidate_percentage('Kamala Harris', 'WY'))
