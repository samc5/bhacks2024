# Flask app with one endpoint
from flask import Flask, jsonify, request, render_template
import tester
import feedparse
import json
from collections import deque
import mongo
import requests

app = Flask(__name__)

feeds = ['https://rss.app/feeds/hrPniMrzl8h6wTuh.xml', 'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml', 'https://feeds.npr.org/1014/rss.xml', 'https://rss.app/feeds/nfQP0BJQ8amXIx94.xml', 'https://rss.politico.com/politics-news.xml', 'https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml', 'https://rss.app/feeds/pYL0Ocz6xle7OWp1.xml', 'https://rss.app/feeds/VhAOOiFwbGFd4WlF.xml', 'https://www.natesilver.net/feed', 'https://rss.app/feeds/BXihygZ4d2NKfzPW.xml', 'https://centerforpolitics.org/crystalball/feed/', 'https://rss.app/feeds/h5Tu1PAwpnnM1qmI.xml', 'https://rss.app/feeds/HJEKIUADv4wOdVjJ.xml', 'https://rss.app/feeds/lEjDG1mAtpWKTp7q.xml', 'https://rss.app/feeds/mEa6aVrq00pYzudF.xml']
# cache = deque(maxlen=5) 


def metaculus():
    # question_id = 12345  # example question ID
    url = f"https://www.metaculus.com/api2/questions/11245/"

    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        question_data = response.json()

        # print(question_data)
        print("Failed to fetch question data:", response.status_code)


@app.route("/")
def main():
    prompters = feedparse.grab_feed(feeds)
    prompters = prompters[:20]
    json_string = json.dumps(prompters, indent=4)
    # prompters = jsonify(feedparse.grab_feed(feeds))
    # # print(prompters)
    # json_string = json.dumps(prompters[0], indent=4)
    # cached_prompts = "\n\n".join(cache)
    live_summary = tester.get_ai_summary(json_string + "\n\nThe following are your most recent five summaries: Please avoid repeating information in these unless you have a different source talking about it")
    summary = live_summary[0]["response"]["response"]
    # cache.append(summary)
    # Prepare the prompt using the cached summaries (the last 5 results)
    htmlsummary = summary.replace("\n", "<br>")
    return render_template("main.html", live_summary=htmlsummary)

@app.route("/get_updates")
def get_updates():
    # You can add logic to fetch new updates here
    
    return jsonify(feedparse.grab_feed(feeds))

@app.route('/get_votes')
def get_votes():
    print("IM WORKING")
    states = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
    ]
    
    state_mapping = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
    "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
    "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
    "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
    "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
    "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York",
    "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
    "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
    "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
    "WI": "Wisconsin", "WY": "Wyoming"
        }


    def get_color(value):
        if value < 0 or value > 1:
            raise ValueError("Value must be between 0 and 1.")
        blue = int(value*255)
        red = int((0.98-value)*255)
        return (red, 0, blue)
    
    def rgbToHex(rgb):
        return '#{:02x}{:02x}{:02x}'.format(rgb[0],rgb[1],rgb[2])


    # Function to get full state name from abbreviation
    def state_name(abbreviation):
        return state_mapping.get(abbreviation, "Unknown State")
    
    result = []
    print(result)
    
    for state in states:
        blue = mongo.get_candidate_percentage("Kamala Harris", state)[0]
        
        
        color = rgbToHex(get_color(blue))
        result.append((state_name(state), color))
        
    print(f"Result: {result}")
    
    final = [{"state": state, "color": color} for state, color in result]
    print(jsonify(final))
    return jsonify(final)


    return jsonify(feedparse.grab_feed(feeds))

@app.route("/get_summary")
def get_summary():
    prompters = feedparse.grab_feed(feeds)
    prompters = prompters[:10]
    json_string = json.dumps(prompters, indent=4)
    # cached_prompts = "\n\n".join(cache)
    live_summary = tester.get_ai_summary(json_string + "\n\nThe following are your most recent five summaries: Please avoid repeating information in these unless you have a different source talking about it" )
    summary = live_summary[0]["response"]["response"]
    # cache.append(summary)
    # print(f': cache: {cache}')
    # Prepare the prompt using the cached summaries (the last 5 results)
    htmlsummary = summary.replace("\n", "<br>")
    return jsonify(htmlsummary)

    
if __name__ == "__main__":
    app.debug = True
    app.run()
