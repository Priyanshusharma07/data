from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_nse_data():
    driver = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        url = 'https://www.nseindia.com/market-data/advance'
        driver.get(url)
        time.sleep(8)

        advance_value = driver.find_element(By.ID, "cm-advancevalue").text.strip()
        decline_value = driver.find_element(By.ID, "cm-declinevalue").text.strip()
        unchanged_value = driver.find_element(By.ID, "cm-unchangedvalue").text.strip()

        return {
            "advance": advance_value,
            "decline": decline_value,
            "unchanged": unchanged_value
        }
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}
    finally:
        if driver:
            driver.quit()
