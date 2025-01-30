from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from webdriver_manager.chrome import ChromeDriverManager

# LinkedIn Credentials
EMAIL = "srinidhichittiiit@gmail.com"
PASSWORD = "Nidhi@123"
PROFILE_URL = "https://www.linkedin.com/in/srinidhichitti/"

def linkedin_scraper():
    # Setup WebDriver
    options = webdriver.ChromeOptions()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Open LinkedIn Login Page
    driver.get("https://www.linkedin.com/login")
    time.sleep(3)

    # ✅ Correct way to find email field
    email_field = driver.find_element(By.ID, "username")
    email_field.send_keys(EMAIL)

    # ✅ Correct way to find password field
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(PASSWORD)
    password_field.send_keys(Keys.RETURN)

    time.sleep(5)  # Wait for login

    # Navigate to LinkedIn profile
    driver.get(PROFILE_URL)
    time.sleep(5)

    # Extract Profile Information
    try:
        name = driver.find_element(By.CSS_SELECTOR, "h1.text-heading-xlarge").text
        headline = driver.find_element(By.CSS_SELECTOR, "div.text-body-medium.break-words").text
    except:
        name, headline = "Not Found", "Not Found"

    print(f"Name: {name}")
    print(f"Headline: {headline}")

    driver.quit()

linkedin_scraper()