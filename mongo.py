from pymongo import MongoClient, ReturnDocument
from datetime import datetime
from dotenv import load_dotenv
import os, json, requests
from mongoadd import *
# set a string equal to the contents of mongodbpassword.txt
load_dotenv()
connection_string = os.getenv("MONGO2")

Trump_keys = {'AL': '5063', 'AK': '6638', 'AZ': '9677', 'AR': '12686', 'CA': '21873', 'CO': '13676', 'CT': '21816', 'DE': '10612', 'FL': '21369', 'GA': '20740', 'HI': '19882', 'ID': '18718', 'IL': '28467', 'IN': '21368', 'IA': '22627', 'KS': '6603', 'KY': '5609', 'LA': '25078', 'ME': '29633', 'MD': '31633', 'MA': '35088', 'MI': '35597', 'MN': '34606', 'MS': '31907', 'MO': '9228', 'MT': '34536', 'NE': '31489', 'NV': '37487', 'NH': '49453', 'NJ': '39528', 'NM': '38878', 'NY': '84296', 'NC': '43783', 'ND': '40669', 'OH': '45853', 'OK': '45322', 'OR': '5792', 'PA': '50814', 'RI': '46719', 'SC': '48236', 'SD': '47682', 'TN': '49749', 'TX': '60390', 'UT': '55311', 'VT': '53669', 'VA': '51373', 'WA': '9289', 'WV': '57048', 'WI': '27062', 'WY': '55501'}
Biden_keys = {'AL': '5755', 'AK': '7073', 'AZ': '10391', 'AR': '13356', 'CA': '22519', 'CO': '13659', 'CT': '21813', 'DE': '10797', 'FL': '22906', 'GA': '21510', 'HI': '19883', 'ID': '19379', 'IL': '28469', 'IN': '22147', 'IA': '23547', 'KS': '7454', 'KY': '6175', 'LA': '25061', 'ME': '30791', 'MD': '31626', 'MA': '35087', 'MI': '37091', 'MN': '34605', 'MS': '32595', 'MO': '10565', 'MT': '35547', 'NE': '31822', 'NV': '37488', 'NH': '49452', 'NJ': '39529', 'NM': '38883', 'NY': '83621', 'NC': '44621', 'ND': '41107', 'OH': '46647', 'OK': '46413', 'OR': '5789', 'PA': '52480', 'RI': '46718', 'SC': '49150', 'SD': '48305', 'TN': '50581', 'TX': '61613', 'UT': '56065', 'VT': '53668', 'VA': '51802', 'WA': '9288', 'WV': '58209', 'WI': '28080', 'WY': '55500'}

candidate_ids = {
    'Kamala Harris': '64984',
    'Donald Trump': '8639',
    'Donald Trump 2020': '5063',
    'Joe Biden': '22519',
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
    db = client["2020"]
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

    def get_candidate_info(candidate_id, state):
        try:
            candidate_idint = int(candidate_id)
        except:
            if (candidate_id) == "Donald Trump":
                candidate_id = Trump_keys[state]
            elif (candidate_id) == "Joe Biden":
                candidate_id = Biden_keys[state]
        # print(list(get_feed(state)))
        candidate_list = list(get_feed(state))[0]["candidates"]
        candidate_info = next((candidate for candidate in candidate_list if candidate['candidateID'] == candidate_id), None)
        if candidate_info:
            return candidate_info, candidate_list.index(candidate_info), state
        else:
            print(f"No candidate found with ID {candidate_id}")

    def get_total_votes(candidate_id, state):
        candidate_info, c, state = get_candidate_info(candidate_id, state)
        if candidate_info:
            candidate_list = list(get_feed(state))[0]["candidates"]
            total_votes = sum(candidate['voteCount'] for candidate in candidate_list)
            return total_votes
        else:
            return 0

    def get_candidate_votes(candidate_id, state):
        candidate_info, c, state = get_candidate_info(candidate_id, state)
        if candidate_info:
            return candidate_info['voteCount']
        else:
            return 0
    #the candidate_id is the same across the three functions

    def get_candidate_proportion(votecount, totalcount):
        return round(abs((votecount / totalcount)), 2) if totalcount != 0 else 0.5

    return (get_candidate_proportion(get_candidate_votes(candidate_id, state), get_total_votes(candidate_id, state)), state)

# print(get_candidate_percentage('Joe Biden', 'WY'))
# print(list(get_feed()))