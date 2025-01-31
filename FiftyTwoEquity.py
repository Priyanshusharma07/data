from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def FiftyTwoWeek():
    driver = None
    try:
        # Initialize driver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        # Target URL
        url = 'https://www.nseindia.com/market-data/52-week-high-equity-market'
        driver.get(url)
        time.sleep(8)

        # Extract data
        fifty_two_week_high = driver.find_element(By.ID, "mscm-wkhvalue").text.strip()
        fifty_two_week_low = driver.find_element(By.ID, "mscm-wklvalue").text.strip()

        return {
            "fifty_two_week_high": fifty_two_week_high,
            "fifty_two_week_low": fifty_two_week_low
        }
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}
    finally:
        if driver:
            driver.quit()

