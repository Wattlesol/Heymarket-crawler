from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time, os
import json
from dotenv import load_dotenv
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5)
    driver.maximize_window()
    return driver

def manual_login(driver):
    username = os.getenv('USERNAME')
    password = os.getenv("PASSWORD")
    url = "https://app.heymarket.com/account/login/"

    driver.get(url)
    driver.find_element(By.ID,'email').send_keys(username)
    driver.find_element(By.ID,"submit-login").click()
    time.sleep(2)

    driver.find_element(By.ID,"password").send_keys(password)
    driver.find_element(By.ID,'submit-password').click()

    time.sleep(5)

    cookies = driver.get_cookies()
    with open("cookies.json","w") as f:
        json.dump(cookies,f,indent=4)

def login(driver):
    driver.get("https://app.heymarket.com/")
    with open("cookies.json") as f:
        cookies = json.load(f)
    for cookie in cookies:
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print('Cookie error:', e)
            pass
    time.sleep(2)
    driver.refresh()
    if not "login" in driver.current_url:
        manual_login(driver)
    print("Login successful")

def process_list(driver, list_rec, rec_time):
    deliverd = []
    failed = []
    responded = []
    opt_out = []
    
    try:
        login(driver)
        try:
            driver.find_element(By.CSS_SELECTOR,'button[aria-label="Close"]').click()
        except:
            print("No popup")

        driver.find_element(By.CSS_SELECTOR,'a[data-cy="lists-anchor"][href="/lists/"]').click()
        all_lists = driver.find_elements(By.CLASS_NAME,'lists_list-name__mC6WK')
        list_found = False
        for lis in all_lists:
            if lis.text == list_rec:
                list_found = True
                lis.click()
                print(f"List '{list_rec}' found and selected")
                break
        if not list_found:
            return {"error": "List not found"}

        list_acts = driver.find_elements(By.CSS_SELECTOR, 'div[class="broadcast-box broadcast-box_list-broadcast-box__DLwfp"]')
        timestamp_found = False
        for act in list_acts:
            heading = act.find_element(By.CLASS_NAME,'broadcast-box_header__LJVUl').text
            if rec_time in heading:
                timestamp_found = True
                act.find_element(By.CSS_SELECTOR,'a[class="broadcast-box_report-link__suJYa text-only"]').click()
                print(f"Message details for timestamp '{rec_time}' found and accessed")
                break
        if not timestamp_found:
            return {"error": "Timestamp not found"}

        boxes = driver.find_elements(By.CSS_SELECTOR,'div[class="campaign_scheduled-message__BCrXv campaign_campaign-steps__JOTCt mb-0"]')
        content = ""
        for box in boxes:
            content = box.find_element(By.CSS_SELECTOR,'div[class="broadcast-box_wrapper__Zm6eO"]').find_element(By.CSS_SELECTOR,'i[class="sub-text"]').text

        tbl_data = driver.find_elements(By.CSS_SELECTOR,'tr[class="ant-table-row ant-table-row-level-0 selectable"]')
        for data in tbl_data:
            details = data.find_elements(By.TAG_NAME,'td')
            name = details[0].text
            for i, itm in enumerate(details[1:]):
                if itm.find_element(By.TAG_NAME,'span'):
                    break
            if i == 0:
                deliverd.append(name)
            elif i == 1:
                failed.append(name)
            elif i == 2:
                responded.append(name)
            else:
                opt_out.append(name)

        return {
            "List": list_rec,
            "timeStamp": rec_time,
            "Content": content,
            "deliverd": deliverd,
            "failed": failed,
            "responded": responded,
            "opt_out": opt_out
        }

    except Exception as e:
        print("Error:", e)
        return {"error": str(e)}

@app.route('/process_list', methods=['POST'])
def api_process_list():
    data = request.get_json()
    list_rec = data.get('list_rec', 'Test List')
    rec_time = data.get('rec_time', '2024 at 11:21 PM')

    driver = initialize_driver()
    try:
        response = process_list(driver, list_rec, rec_time)
        driver.quit()
        return jsonify(response)
    except Exception as e:
        driver.quit()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)
