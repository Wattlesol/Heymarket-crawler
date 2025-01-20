import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from database_handler import Database

def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(5)
    return driver

def manual_login(driver, username, password):
    url = "https://app.heymarket.com/"
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'email'))).send_keys(username)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "submit-login"))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys(password)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'submit-password'))).click()

def process_list(driver, list_rec, rec_time, username, password):
    deliverd = []
    failed = []
    responded = []
    opt_out = []

    try:
        manual_login(driver, username, password)
        try:
            WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Close"]'))).click()
        except:
            print("No pop-up")

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-cy="lists-anchor"]'))).click()
        all_lists = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'lists_list-name__mC6WK')))
        list_found = False
        for lis in all_lists:
            if lis.text == list_rec:
                list_found = True
                lis.click()
                print(f"List '{list_rec}' found and selected")
                break
        if not list_found:
            return {"error": "List not found"}

        list_acts = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[class="broadcast-box broadcast-box_list-broadcast-box__DLwfp"]')))
        timestamp_found = False
        for act in list_acts:
            heading = act.find_element(By.CLASS_NAME, 'broadcast-box_header__LJVUl').text
            if rec_time in heading:
                timestamp_found = True
                act.find_element(By.CSS_SELECTOR, 'a[class="broadcast-box_report-link__suJYa text-only"]').click()
                print(f"Message details for timestamp '{heading}' found and accessed")
                break
        if not timestamp_found:
            return {"error": "Timestamp not found"}

        boxes = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[class="campaign_scheduled-message__BCrXv campaign_campaign-steps__JOTCt mb-0"]')))
        content = ""
        Campaign, send_to = "", ""
        try:
            for box in boxes:
                content = box.find_element(By.CSS_SELECTOR, 'div[class="broadcast-box_wrapper__Zm6eO"]').find_element(By.CSS_SELECTOR, 'i[class="sub-text"]').text
                Campaign = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="icon-inbox-black-filled broadcast-box_item-with-icon__YNeBK"]'))).text
                send_to = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="icon-contacts broadcast-box_item-with-icon__YNeBK"]'))).text
                print("Campaign name:", Campaign)
                print("Send to:", send_to)
        except Exception as e:
            print("Error while fetching campaign or send_to details:", e)

        tbl_data = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'tr[class="ant-table-row ant-table-row-level-0 selectable"]')))
        for data in tbl_data:
            try:
                details = data.find_elements(By.TAG_NAME, 'td')
                name = details[0].text
                for i, itm in enumerate(details[1:]):
                    if itm.find_element(By.TAG_NAME, 'span'):
                        break
                if i == 0:
                    deliverd.append(name)
                elif i == 1:
                    failed.append(name)
                elif i == 2:
                    responded.append(name)
                else:
                    opt_out.append(name)
            except Exception as e:
                print("Error while processing table data:", e)

        scraped_data = {
            "List": list_rec,
            "timeStamp": rec_time,
            "Content": content,
            "deliverd": deliverd,
            "failed": failed,
            "responded": responded,
            "opt_out": opt_out,
            "Campaign": Campaign,
            "send_to": send_to
        }

        db = Database()
        db.save_scraped_data(scraped_data)

        print("Scraping completed successfully and data saved to database")
        driver.quit()

        return scraped_data

    except Exception as e:
        print("Error during process_list execution:", e)
        driver.quit()
        return {"error": str(e)}

def async_process_list(data):
    driver = initialize_driver()
    list_rec = data.get('list_rec', 'Test List')
    rec_time = data.get('rec_time', '2024 at 11:21 PM')
    username = data.get("username", '')
    password = data.get("password", "")
    process_list(driver, list_rec, rec_time, username, password)
