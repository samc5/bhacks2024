import feedparser

# URL of the RSS feed
rss_url = 'https://rss.app/feeds/nfQP0BJQ8amXIx94.xml'

# Parse the RSS feed
feed = feedparser.parse(rss_url)

# Print the feed title
print(f"Feed Title: {feed.feed.title}")

# Print the titles of the first 5 entries
for entry in feed.entries[:10]:
    print(f"Title: {entry.title}")
    print(f"Link: {entry.link}")
    print(f"Date: {entry.published}")
    print(f"Summary: {entry.summary}")
    print()