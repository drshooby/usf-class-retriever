import time

import dotenv
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

'''
Build the driver object.
'''
def create_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    return driver

'''
Helper functions for performing page-load waits.
'''
def wait_for_page_load(driver, title, timeout=10):
    WebDriverWait(driver, timeout).until(
        ec.title_contains(title)
    )

def wait_for_element(driver, by, value, timeout=10):
    WebDriverWait(driver, timeout).until(
        ec.visibility_of_element_located((by, value))
    )

'''
Uses Selenium to interact with the DOM and automate the retrieval of class schedule information.
'''
def get_cookies_from_login(term_code):
    driver = create_driver()

    try:
        config = dotenv.dotenv_values()

        print("Logging You In...")
        driver.get("https://myusf.usfca.edu/dashboard")
        driver.find_element(By.CLASS_NAME, "login-btn").click()
        username_input = driver.find_element(By.ID, "username")
        username_input.clear()

        if "usf-username" not in config or "usf-password" not in config:
            print("Env fields are missing. Try checking credentials.")
            driver.quit()
            return None

        username_input.send_keys(config["usf-username"])
        password_input = driver.find_element(By.ID, "password")
        password_input.clear()
        password_input.send_keys(config["usf-password"])
        driver.find_element(By.NAME, "submit").click()

        print("Confirming Login Success...")
        time.sleep(2)
        try:
            error_msg = driver.find_element(By.ID, "loginErrorsPanel")
            print(error_msg.text)
            driver.quit()
            return None
        except NoSuchElementException:
            pass

        print("Navigating To Registration Page...")
        wait_for_page_load(driver, "Dashboard")
        driver.get("https://reg-prod.ec.usfca.edu/StudentRegistrationSsb/ssb/registration")
        driver.find_element(By.ID, "registerLink").click()

        print("Entering Term Info...")
        driver.find_element(By.ID, "s2id_txt_term").click()
        wait_for_element(driver, By.ID, term_code)
        driver.find_element(By.ID, term_code).click()
        wait_for_element(driver, By.ID, "term-go")
        driver.find_element(By.ID, "term-go").click()

        print("Extracting Relevant Cookies...")
        wait_for_element(driver, By.CLASS_NAME, "section-details-link")

        cookies = driver.get_cookies()
        cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies if cookie['name'] in ["JSESSIONID", "AWSALB", "AWSALBCORS"]}

        return cookies_dict
    except NoSuchElementException as e:
        print("Page Element Error - maybe check inputs?:", e)
        return None
    except Exception as e:
        print("Error:", e)
        return None
    finally:
        driver.quit()
