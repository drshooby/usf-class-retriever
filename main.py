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
Helper functions for performing page-load waits
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
def login(semester, term_year):
    driver = create_driver()

    try:
        config = dotenv.dotenv_values()

        sem_translate = {
            "fall": "10",
            "spring": "20",
            "summer": "30"
        }

        if semester not in sem_translate:
            raise ValueError(f"Invalid semester: {semester}! Valid options are 'fall', 'spring', or 'summer'.")

        print("Logging You In...")
        driver.get("https://myusf.usfca.edu/dashboard")
        driver.find_element(By.CLASS_NAME, "login-btn").click()
        username_input = driver.find_element(By.ID, "username")
        username_input.clear()
        username_input.send_keys(config["usf-username"])
        password_input = driver.find_element(By.ID, "password")
        password_input.clear()
        password_input.send_keys(config["usf-password"])
        driver.find_element(By.NAME, "submit").click()

        print("Navigating To Registration Page...")
        wait_for_page_load(driver, "Dashboard")
        driver.get("https://reg-prod.ec.usfca.edu/StudentRegistrationSsb/ssb/registration")
        driver.find_element(By.ID, "registerLink").click()

        print("Entering Term Info...")
        driver.find_element(By.ID, "s2id_txt_term").click()
        term_code = str(term_year) + sem_translate[semester]
        wait_for_element(driver, By.ID, term_code)
        driver.find_element(By.ID, term_code).click()
        wait_for_element(driver, By.ID, "term-go")
        driver.find_element(By.ID, "term-go").click()

        print("Getting Your Classes...")
        wait_for_element(driver, By.CLASS_NAME, "section-details-link")
        details = driver.find_elements(By.CLASS_NAME, "section-details-link")

        time_and_classes = set()
        for elem in details:
            parts = elem.text.split("\n")
            if len(parts) == 2:
                time_and_classes.add((parts[0], parts[1]))

        return time_and_classes
    except NoSuchElementException as e:
        print("Page Element Error - maybe check inputs?:", e)
    except Exception as e:
        print("Error:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    v = login("spring", 2025)
    print(v)


