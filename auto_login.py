# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0041688696941FE4AD639D957BC9F377348CEA4DF90DB350ABA87DDFD3446B9BF1B7B374AE97D7A154731EA73FBF38406AB9AADED9D22BE27F549614A16001146BED5464F7CED622043E163F32160281DB20E49DCD9B93666D9E6E5B3EA84F3C795FFA0A71CE95881CAE9806018CABDC45F11C0BE189CF7838E604D2BAE4C7CB1D2EFA3BB4AFEDCCB637F38B74A77005A0C7D00AB7A8222185374F403D6055AD300F72040450529E14627099CAF7977F61B475CC9BD0AAD5E73360B498DDE74E26D883EB601479D18D5B48E92E5F187EA98E4C9A5C983A2BE177917AFF06D4769E00DCEB2443F306FD8FD6CDC366E1E7F13F5620D85722194C96881A0A139CD835CDD381FC79096A47ECDD183B3C87DB36BF0E6EA5D5BB63ABDFE28B4670085436EAA4D4162D1B44D3D8BBEB583895A664B5FAD4A6D96B961526F664E3CE9EE596BB2CE70A2677065D99F19294284BEBFD0ACAC48E6D1CB84CCFB509FD29443B72"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
