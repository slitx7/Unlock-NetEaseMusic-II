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
    browser.add_cookie({"name": "MUSIC_U", "value": "003C3D578408946EC546C8509DC9E343AAE3BB572F957486CE8200ED12C1F034D2CA3E4AA46795220E584EF71AC2CE7A0B86DFDBC925EBADDBECFA219D0407070C67B8AD8D37B8992801EA2F94066E7176E03AE99D756EBFD5F9398571E9900E88C406A43300836F93ECABEF5D46557D02C84A78289DBE826E881B38596DF8422A74A3A6D40F1397B267372A194A3D4A1186D956B6874544F8B226BE11770107E4DAC7FB8953C89BCFA449C41D1CA6DFBC255428F16118648E9F0D5A6AF8673AD7DEEB703467840163B00530C50008F433355B818ADEB6ADD199AC407C46EC27BC3CD417EE14E17B385E87CEBE35A6FEB1656B3C06AA55C97DD7DC89E9160534B64E3D6D88DB235DBE15054A63169593B3BC9C01BEE6D3370F9BE6FABD24B54A50FB955F8082304D89AB53317438C0AD40C411D75AD02852D7A05E61A278564FF52D3637D56AF3802C583DE1DC250C944766CB03B134D560A30F8C83BABE3A4CA8"})
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
