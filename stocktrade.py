from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def Stock():
    driver = None
    try:
        # Initialize driver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        # Target URL
        url = 'https://www.nseindia.com/market-data/stocks-traded'
        driver.get(url)
        time.sleep(8)

        # Extract data
        Stock_trade = driver.find_element(By.ID, "cm-stocksTradedval").text.strip()


        return {
            "Stock_trade": Stock_trade,

        }
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}
    finally:
        if driver:
            driver.quit()

