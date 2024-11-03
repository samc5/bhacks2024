import requests

def get_ai_summary(prompt):
    url = 'https://empty-hat-214d.samcowan1968.workers.dev/'  # Replace with your actual Cloudflare Worker URL
    headers = {
        'Content-Type': 'application/json',
    }
    payload = {
        'prompt': prompt,
    }
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.json().get("error", "Unknown error")}

# prompt = """Via Metaculus, Kamala Harris currently has a 52% chance of winning and Donald Trump has a 45% chance of winning. With the results in NE-02, the odds of a tie have increased to around 3%.
# Donald Trump has been holding an election night rally all night in North Carolina, via AP. He has been leading in the state, but early returns have not distinguished a front runner, says the NYT Needle, which puts NC at 60% for Trump.
# """
# summary = get_ai_summary(prompt)
# print(summary)
