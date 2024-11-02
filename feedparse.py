import feedparser
import re

def grab_feed():
    # URL of the RSS feed
    rss_url = 'https://rss.app/feeds/nfQP0BJQ8amXIx94.xml'

    # Parse the RSS feed
    feed = feedparser.parse(rss_url)

    # Print the feed title
    print(f"Feed Title: {feed.feed.title}")

    # Prepare results list
    results = []
    
    # Loop through the first 10 entries in the feed
    for entry in feed.entries[:10]:
        # Remove <img> tags entirely
        cleaned_summary = re.sub(r'<img[^>]*>', '', entry.summary)  # Remove <img> tags
        # Remove <div> and </div> tags but keep the inner content
        cleaned_summary = re.sub(r'</?div[^>]*>', '', cleaned_summary)  # Remove <div> and </div> tags
        
        # Append the cleaned summary along with other data
        results.append({
            "title": entry.title,
            "link": entry.link,
            "date": entry.published,
            "summary": cleaned_summary
        })
    
    return results
