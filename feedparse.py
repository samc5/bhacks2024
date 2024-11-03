import feedparser
import re
from datetime import datetime
from mongo2 import convert_to_date
import requests
def grab_feed(rss_urls):
    # URL of the RSS feed
    results = []
    for i in rss_urls:
        rss_url = i
        # Parse the RSS feed
        response = requests.get(rss_url, headers={"Cache-Control": "no-cache", "Pragma": "no-cache"})
        response.raise_for_status()
        feed = feedparser.parse(response.content)
        # print(feed)

        # Print the feed title
        print(f"Feed Title: {feed.feed.title}")

        # Prepare results list
        
        # Loop through the first 3 entries in the feed
        for entry in feed.entries[:3]:
            # Remove <img> tags entirely
            cleaned_summary = re.sub(r'<img[^>]*>', '', entry.summary)  # Remove <img> tags
            # Remove <div> and </div> tags but keep the inner content
            cleaned_summary = re.sub(r'</?div[^>]*>', '', cleaned_summary)  # Remove <div> and </div> tags
            cleaned_summary = re.sub(r'</?p[^>]*>', '', cleaned_summary)  # Remove <p> and </p> tags
            cleaned_summary = re.sub(r'</?blockquote[^>]*>', '', cleaned_summary)  # Remove <blockquote> and </blockquote> tags
            cleaned_summary = re.sub(r'</?a[^>]*>', '', cleaned_summary)  # Remove <a> and </a> tags

            # print(cleaned_summary)
            # Append the cleaned summary along with other data
            results.append({
                "feed_title": feed.feed.title,
                "title": entry.title,
                "link": entry.link,
                "date": entry.published,
                "summary": cleaned_summary
            })
    results = sorted(results, key=lambda x: convert_to_date(x['date']), reverse=True)
    # print(results)
    return results
