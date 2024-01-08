import re
import time
import core.env_manager as env_manager
from loguru import logger
from typing import List
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement


MBASIC_FB_PREFIX = "https://mbasic.facebook.com"


def wait_until_loaded(driver: webdriver.Chrome, timeout: int=30):
    wait = WebDriverWait(driver, timeout)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "html")))
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[not(@aria-busy) and not(@data-loading) and not(@aria-live='polite')]")))
    time.sleep(1)


def start_driver(debug: bool = False) -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    
    if debug is False:
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        
    options.add_argument("--disable-blink-features=AutomationControllered")
    options.add_experimental_option("useAutomationExtension", False)
    prefs = {"profile.default_content_setting_values.notifications": 2}
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--start-maximized")  # open Browser in maximized mode
    options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("disable-infobars")
    driver = webdriver.Remote("http://selenium-standalone:4444/wd/hub", options=options)
    return driver


def convert_cookie(cookie: str) -> str:
    try:
        new_cookie = ["c_user=", "xs="]
        cookie_arr = cookie.split(";")
        for i in cookie_arr:
            if i.__contains__("c_user="):
                new_cookie[0] = new_cookie[0] + (i.strip() + ";").split("c_user=")[1]
            if i.__contains__("xs="):
                new_cookie[1] = new_cookie[1] + (i.strip() + ";").split("xs=")[1]
                if (len(new_cookie[1].split("|"))):
                    new_cookie[1] = new_cookie[1].split("|")[0]
                if (";" not in new_cookie[1]):
                    new_cookie[1] = new_cookie[1] + ";"

        conv = new_cookie[0] + " " + new_cookie[1]
        if (conv.split(" ")[0] == "c_user="):
            return
        else:
            return conv
    except:
        print("Cookie conversion error!")


def execute_login_script(driver: webdriver.Chrome, cookie: str):
    if cookie is None:
        raise Exception("The input cookie is None")
        
    try:
        path = env_manager.get_login_script_path()
        with open(path, "r") as f:
            script = f.read()
            script = script.replace("__{{input-cookie}}__", cookie)
            driver.execute_script(script)
            time.sleep(3)
            return True
    except Exception as e:
        logger.error(e)
        return False


def login_by_cookie(driver: webdriver.Chrome, cookie: str) -> bool:
    try:
        driver.get(MBASIC_FB_PREFIX)
        time.sleep(1)
        driver.get(MBASIC_FB_PREFIX)
        time.sleep(2)
        cookie = convert_cookie(cookie)
        execute_login_script(driver, cookie)
        return True
    except Exception as e:
        logger.error(e)
        return False
    

def search_by_text(driver: webdriver.Chrome, text: str) -> bool:
    try:
        search_box = driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div/form/table/tbody/tr/td[2]/input")
        search_box.clear()
        search_box.send_keys(text)
        search_box.send_keys(Keys.ENTER)
        return True
    except Exception as e:
        logger.error(e)
        return False


def mbasic_goto(driver: webdriver.Chrome, id: str):
    driver.get(f"{MBASIC_FB_PREFIX}/{id}")
    wait_until_loaded(driver)
    

def list_post_ids(driver: webdriver.Chrome) -> list:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    ids = set()
    posts = driver.find_elements(By.TAG_NAME, "article")
    logger.info(f"Found {len(posts)} posts, try to extract post_id")
    for post in posts:
        links = post.find_elements(By.XPATH, "//a[contains(@href, 'shared_from_post_id')]")
        for post in links:
            href = post.get_attribute("href")
            post_id = re.findall("shared_from_post_id=([0-9a-zA-Z]+)", href)[0]
            ids.add(post_id)
    logger.info(f"==> {ids}")
    return ids


def load_more_posts(driver: webdriver.Chrome):
    see_more_div = driver.find_element(By.ID, "see_more_pager")
    if see_more_div is None:
        raise Exception("No <More posts> element!")
    
    logger.info(f"Try to click <Show more>")
    see_more_div.find_element(By.TAG_NAME, "a").click()
    wait_until_loaded(driver)


def list_all_post_ids(driver: webdriver.Chrome, keyword: str, limit: int = 10) -> list:
    search_by_text(driver, keyword)
    res = []
    for _ in range(limit):
        for post_id in list_post_ids(driver):
            res.append(post_id)
        try:
            load_more_posts(driver)
        except:
            break

    return res


def find_post_comment_elements(driver: webdriver.Chrome) -> List[WebElement]:
    xpath = "/html/body/div/div/div[2]/div/div[1]/div[2]/div/div[5]/div[*]"
    elms = driver.find_elements(By.XPATH, xpath)
    return elms


def find_post_show_more_element(elms: List[WebElement]) -> bool:
    for cmt in elms:
        cmt_id = cmt.get_attribute("id")
        if "see_next" in cmt_id:
            return cmt
    return None


def find_post_comments(elms: List[WebElement]) -> list:
    res = []
    for cmt in elms:
        try:
            cmt_id = cmt.get_attribute("id")
            if "see_next" in cmt_id:
                continue
            cmt_content = cmt.find_element(By.XPATH, "./div/div[1]").text
            cmt_date = cmt.find_element(By.TAG_NAME, "abbr").text
            res.append((cmt_id, cmt_content, cmt_date))
        except:
            pass

    return res


def load_more_comments(driver: webdriver.Chrome):
    elms = find_post_comment_elements(driver)
    show_more = find_post_show_more_element(elms)
    if show_more is None:
        raise Exception("No <Show more> element!")

    logger.info(f"Try to click <Show more>")
    show_more.find_element(By.TAG_NAME, "a").click()
    wait_until_loaded(driver)


def list_all_post_comments(driver: webdriver.Chrome, post_id: str, earlystop=10) -> list:
    res = []
    mbasic_goto(driver, post_id)

    for _ in range(earlystop):
        elms = find_post_comment_elements(driver)
        res = res + find_post_comments(elms)
        
        try:
            load_more_comments(driver, elms)
        except:
            pass

    return res