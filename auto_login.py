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
    browser.add_cookie({"name": "MUSIC_U", "value": "00A3D2F50C1EDEA512A0CB16985B3C89AA52D124B70BBD335D09942671818C285998EB3D8BA06D79F59D344D25D363ACD336CC05F009B1933C4E55E78A22232EA1008578B45D4E7E63B6F7BFDB2C5C9424DD948E4CDF307931D47A600BBDF88166AE6BE9BF8BF36D8F0BADDD74A501D89273250B5669E64CF7E1EBD206594FF69311718E15448E76988279D7D613F944C39524DAA70F1C0233DD1DB2F6A327E0E8ACB9C52FB31889D40EC6C6D933140C4C6613AF1188F3FE9BCB6037E1D15863F07D233AB72719AFC39CD809931DD804F9296E3B34C3301F32E50F6E127EA303B31923FF4D57CA441B77C105D6BD2735647F7CA5FB0B42AC5E8DE55883A8DDB0C457A5B2B2159AE89644F9669D9AE60B25D64359DEF2633ECAEEB1B14687537B163EC2624A7C2FE725A2CD750F540EDA77074E3F2BE07DD175BFB2CC6036FFB34871C756405B2E561126281254F714DE20979BC1C8219751CE2753865B962C1640"})
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
