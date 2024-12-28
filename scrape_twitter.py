from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pymongo
import uuid

# Function to get a new proxy IP from ProxyMesh
def get_proxy():
    return "http://username:password@proxy.proxy_mesh.com:port"  # Replace with actual credentials

# MongoDB setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["twitter_data"]
collection = db["trends"]

def scrape_trending_topics():
    # Set up the Selenium WebDriver with ProxyMesh
    proxy = get_proxy()  # Ensure this function is called after its definition
    options = webdriver.ChromeOptions()
    options.add_argument(f'--proxy-server={proxy}')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        # Log in to Twitter (replace with your credentials)
        driver.get("https://x.com/i/flow/login")
        time.sleep(3)
        
        username_input = driver.find_element(By.NAME, "text")
        username_input.send_keys("your_username")  # Replace with your Twitter username
        username_input.send_keys(Keys.RETURN)
        time.sleep(3)
        
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys("your_password")  # Replace with your Twitter password
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)

        # Navigate to the home page and scrape trending topics
        driver.get("https://x.com/home")
        time.sleep(5)

        trends = driver.find_elements(By.XPATH, '//div[@data-testid="trend"]//span')[:5]
        trending_topics = [trend.text for trend in trends]

        # Generate unique ID and store data in MongoDB
        unique_id = str(uuid.uuid4())
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        
        record = {
            "unique_id": unique_id,
            "trends": trending_topics,
            "timestamp": timestamp,
            "ip_address": proxy.split('@')[1].split(':')[0]  # Extract IP from proxy string
        }
        
        collection.insert_one(record)
        
        return record

    finally:
        driver.quit()

if __name__ == "__main__":
    result = scrape_trending_topics()
    print(result)
