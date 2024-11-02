import requests

def fetch_post():
    url = "https://www.metaculus.com/api/posts/11245/"
    response = requests.get(url)
    
    if response.status_code == 200:
        post_content = response.json()
        print(post_content)
    else:
        print(f"Failed to fetch post. Status code: {response.status_code}")

if __name__ == "__main__":
    fetch_post()