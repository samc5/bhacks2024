import json
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def process_browser_logs_for_network_events(logs):
    """Process browser logs and yield relevant network events."""
    for entry in logs:
        log = json.loads(entry["message"])["message"]
        if "Network.response" in log["method"] or "Network.request" in log["method"]:
            yield log

def print_network_traffic(ap_url):
    # Set Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    # Add logging preferences directly to chrome options
    chrome_options.add_experimental_option("w3c", False)
    chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    chrome_options.add_experimental_option("loggingPrefs", {"performance": "ALL"})

    # Specify the path to your ChromeDriver
    homedir = os.path.expanduser("~")
    webdriver_service = Service(f"{homedir}/chromedriver/stable/chromedriver")

    # Create the WebDriver instance with options
    browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)

    # Navigate to the URL
    browser.get(ap_url)

    # Allow some time for the network events to be captured
    time.sleep(5)

    # Fetch the performance logs
    logs = browser.get_log("performance")

    # Process and print the network events
    for log in process_browser_logs_for_network_events(logs):
        # Here we can print the entire log, or specific details
        print(json.dumps(log, indent=2))  # Pretty-print the log entry

    # Clean up
    browser.quit()


# Example usage
game_url = "https://apnews.com/projects/election-results-2024/"  # Replace with the URL you want to inspect
print_network_traffic(game_url)
