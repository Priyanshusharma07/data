from selenium import webdriver   
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def Advance():
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

def StockTrade():
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

