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
    browser.add_cookie({"name": "MUSIC_U", "value": "00E6DF475B6FE31CB809C66F7F210639F19982AAF62AC6B2AF1836D645E452608ACC414FEFF2BEE148068832F628FEB9D945B243068ACCDCBF50CD29A4862571C6A821455F0714C60057835F824F342B4247AD180431B0235865D9AD50E9AE1CCBF4B2ECD355F95E0FB8BF8C192BE5E43A1A82F445DB2ACA99D9C270DC6F5C26DBE4559D79F2D20713EB73A3E8A8CED6A5A1BDF7FB252EBD9EF2E28A834E94589B7875044E40A70B6CD542DCD0A818471826B5E434E481BFB1D605526BA5B0B37179875B95BB417B42614B9BA4930ADAFC64E939664A897DFC8C39C25C637EDDD8661086E1F83F9ECAB568FDA355E2C5BF21E3B53F102130721A1BC66A8AFC451AE263CF6B9DDC750039E9BE250CC9B887CEC8D5C3F256202C63367AB09B18866CC701B500A83184F49D47BCAB6223FD892910DE4AC70BC5BA17610FCADD855C9850EAD6F6826FA1885FBB7D33F2D321E9"})
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
