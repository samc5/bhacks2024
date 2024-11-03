import requests
from pymongo import MongoClient
from dotenv import load_dotenv
import os, time
# MongoDB connection
load_dotenv()
connection_string = os.getenv("MONGO2")
uri = "mongodb+srv://samcowan1968:VtEVUM30MpuPRKDZ@2020.3f92k.mongodb.net/?retryWrites=true&w=majority&appName=2020"
client = MongoClient(uri)
db = client["2020"]
collection = db["States"]

# List of state abbreviations
states = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]

# Base URL format
def add_new_election_data():
    base_url = "https://interactives.apelections.org/election-results/data-live/2020-11-03/results/races/{}/20201103{}0/metadata.json"
    base_url2 = "https://interactives.apelections.org/election-results/data-live/2020-11-03/results/races/{}/20201103{}0/summary.json"
    for state in states:
        url = base_url.format(state, state)  # Generate the URL for the current state
        url2 = base_url2.format(state, state)
        try:
            # Download JSON content
            response = requests.get(url)
            response.raise_for_status()  # Check for request errors
            json_data = response.json()  # Parse JSON content
            response2 = requests.get(url2)
            response2.raise_for_status()  # Check for request errors
            json_data2 = response2.json()  # Parse JSON content
            filter = {"statePostal": state}
            filter2 = {"statePostal": state}
            # Insert JSON data into MongoDB
            collection.replace_one(filter, json_data, upsert=True)
            collection.replace_one(filter2, json_data2, upsert=True)
            print(json_data, json_data2)
            print(f"Data from {url} added to MongoDB successfully!")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
        except Exception as e:
            print(f"Error inserting data from {url}: {e}")

if __name__ == "__main__":
    add_new_election_data()