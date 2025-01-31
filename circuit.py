from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def circuit():
    driver = None
    try:
        # Initialize driver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        # Target URL
        url = 'https://www.nseindia.com/market-data/upper-band-hitters'
        driver.get(url)
        time.sleep(8)

        # Extract data
        Upper_circuit = driver.find_element(By.ID, "cm-advancevalue").text.strip()
        Lower_circuit = driver.find_element(By.ID, "cm-declinevalue").text.strip()

        return {
            "Upper_circuit": Upper_circuit,
            "Lower_circuit": Lower_circuit
        }
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}
    finally:
        if driver:
            driver.quit()

