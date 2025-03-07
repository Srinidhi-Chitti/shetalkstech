from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from webdriver_manager.chrome import ChromeDriverManager

# LinkedIn Credentials
EMAIL = "srinidhichittiiit@gmail.com"
PASSWORD = "Nidhi@123"
PROFILE_URL = "https://www.linkedin.com/in/srinidhichitti/"

def linkedin_scraper():
    # Setup WebDriver with anti-detection options
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 15)

    try:
        # Open LinkedIn Login Page
        driver.get("https://www.linkedin.com/login")
        
        # Login process with explicit waits
        email_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        email_field.send_keys(EMAIL)
        
        password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_field.send_keys(PASSWORD)
        password_field.send_keys(Keys.RETURN)

        # Wait for login to complete
        wait.until(EC.url_contains("feed"))

        # Navigate to profile page
        driver.get(PROFILE_URL)
        
        # Wait for profile to load
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".top-card-layout__title")))

        # Extract Profile Information with updated selectors
        name = driver.find_element(By.CSS_SELECTOR, ".top-card-layout__title").text.strip()
        headline = driver.find_element(By.CSS_SELECTOR, ".top-card-layout__headline").text.strip()

        print(f"Name: {name}")
        print(f"Headline: {headline}")

    except Exception as e:
        print(f"Error occurred: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    linkedin_scraper()