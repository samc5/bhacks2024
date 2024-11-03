# Elector
In 2020, a lot of the false narratives about the election were based on the "horse race" idea of traditional news media covering the election. That's why we dashboard based on calm analysis of things as they happen without any of the sensationalism.
### What it does

Aggregates news from various analysts and news sources and synthesizes it with a Mistral LLM hosted with Cloudflare.

It is more or less ready for the election! The app is by far most important on election night and in the days after, but we tried to show how it will look by hooking up the 2020 election data (which is the exact same format as 2024 will be).

### How we built it
  - Flask backend
- MongoDB database to store live election results scraped from AP
  - Bootstrap for frontend
  - Mistral LLM hosted on Cloudflare
  - Pulling and parsing RSS feeds ## Challenges we ran into Getting live election data is... really hard (we found an AP private API) ## Accomplishments that we're proud of Live news updates from various sources by parsing RSS feeds The election map worked in the end! It scrapes data from the AP's live election results, and puts it into a MongoDB database, then fetches it to display the election map. We created an alternate MongoDB cluster which is identical to the real live updating one, but using the 2020 election results to prove that the map works. ## What we learned

### What's next for Elector

    Preparing for the election in 2 days
    Expanding to focus on midterms and even local elections
