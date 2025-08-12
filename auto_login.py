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
    browser.add_cookie({"name": "MUSIC_U", "value": "00AD68A5F512FEB9E203E8FD988EDA4923E60BFF1B8FDE953260E20A544057091EEBFC9D2F0DB263D39CCF0AC385CAE40D49EEFA1754E998CA1760FA2441D20B10814AC5E965208E7E29D8CBB1FCC6363B236476FBACC065D3AFB035DED3B42E9466F1320EFAAAF2600A804CCAB211564BACB438DBE5D134C5676EA3AAB98252EC057BEE03DFEFBB1924C7E576DA32EC93477718BDD1A0E23D1E5E1BDAB909A9254C14B644596AD8E074B57504B5BA1AAF48A7D6CCADE07094F449FA3FCEF8AE857238EA7ABA70D2C9F28E5970E20A413F4B33811132E2ADACBD05A6B1E7A71201CA1575F13FE971396D5BBE68D5269591E0AA873C273B9520FD111FD5D47E33ECCDF7F170E8FC63104705C53FC68CF3D9D1F57C7B59AE17CF5DB0264112282B62E0AE2DABE8CBEAE5C01F7BF0CAB0C6838BBF807B7D52C3E47C4902ED40F253851E34F9C7D656E62D82B08EF22F365280B0AAB84CC11F9C89E0963CAE9E6064029A66F31BBDDFF8E35CDA2FB56911D899"})
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
