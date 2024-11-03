# Flask app with one endpoint
from flask import Flask, jsonify, request, render_template
import tester
import feedparse
import json
from collections import deque
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
    else:
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
