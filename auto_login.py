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
    browser.add_cookie({"name": "MUSIC_U", "value": "0031C3DFDD46438EC725CF7DDFF9BEDC776954FFFD4F76D910DF15D3F8257F154BD6D165FF387585A261412A2A3321126E21AFFC6D3EE48F448604B41BBD0A650F4D101C843A27CD4CB2181EF07DBE2F63A230587FE25C7F7ABA473C39FCCE0AC3562B7D16E63C2D70722F6EA5829C81B8484DD8679F7F472AEBBF367D5996A074E0E600C5AFEEAA61AAA76503D66B0FAB57C17D2B2D796EB2C65877098506001D2779BACDF2E5DC1CAC05C9BF4D54B1C59ACF0E490709FFA9E843E4BE8154F44186AF767F01933AC791EF860FD51DA46AAEAEC34B963CB7D88D2C4A0AB02133F60478A2C963C1A66FC78616804652334B3ED5809C7522E1957440AC79B19E5B2942CE228D3CF0DC0403B6564268BA16C5532753218D50A3A2043BE0E4CCDEE0A8EFA8F3D8BCA41556749B5AB7744E134470AC2F829BBBB0005461578C51490A8FAE2E33EAE2455133DE1C810876953A3AB8ADB9055D7680383F7D03F4E89AE6EC"})
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
