from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Enable network logging
chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

# Set up Chrome driver
driver_path = "./chromedriver"  # Replace with your ChromeDriver path
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the website
url = "https://apnews.com/projects/election-results-2024/"
driver.get(url)

# Give the page time to load requests
time.sleep(10)  # Adjust as necessary based on network conditions

# Capture network logs and filter for JSON requests
logs = driver.get_log("performance")
json_urls = []

for log in logs:
    message = log["message"]
    if "summary.json" in message or "metadata.json" in message:
        # Parse the message to get the URL
        start_idx = message.find("https://")
        end_idx = message.find(".json") + len(".json")
        json_url = message[start_idx:end_idx]
        
        if json_url not in json_urls:
            json_urls.append(json_url)

# Output the URLs
for url in json_urls:
    print(url)

# Close the driver
driver.quit()
