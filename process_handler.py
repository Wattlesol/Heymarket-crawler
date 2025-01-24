import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from database_handler import Database
from datetime import datetime
def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(5)
    print("----------------driver Started-----------------")
    return driver

def manual_login(driver, username, password):
    url = "https://app.heymarket.com/"
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'email'))).send_keys(username)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "submit-login"))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys(password)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'submit-password'))).click()

# Define a function to add the ordinal suffix to the day
def get_day_with_suffix(day):
    if 11 <= day <= 13:  # Special cases for 11th, 12th, 13th
        return f"{day}th"
    if day % 10 == 1:  # 1st
        return f"{day}st"
    elif day % 10 == 2:  # 2nd
        return f"{day}nd"
    elif day % 10 == 3:  # 3rd
        return f"{day}rd"
    else:  # Everything else
        return f"{day}th"

def process_list(driver, list_id, message_content:str, message_timestamp:str, username:str, password:str):
    deliverd = []
    failed = []
    responded = []
    opt_out = []

    try:
        manual_login(driver, username, password)
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Close"]'))).click()
        except:
            print("No pop-up")

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-cy="lists-anchor"]')))
        print("Main page loaded")

        # all_lists = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'lists_list-name__mC6WK')))
        # list_found = False
        # for lis in all_lists:
        #     if lis.text == list_rec:
        #         list_found = True
        #         lis.click()
        #         print(f"List '{list_rec}' found and selected")
        #         break
        # if not list_found:
        #     return {"error": "List not found"}

        list_url = f"https://app.heymarket.com/lists/{list_id}/details/"
        driver.get(list_url)

        list_acts = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[class="broadcast-box broadcast-box_list-broadcast-box__DLwfp"]')))
        print("All List Reports Loaded")
        timestamp_found = False
        for act in list_acts:
            driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", act)
            message_heading = act.find_element(By.CSS_SELECTOR,'div[class="broadcast-box_header__LJVUl"]').text
            try:
                act_content = act.find_element(By.CSS_SELECTOR,'i[class="sub-text"]').text
            except:
                act_content = "Message is a template"

            if message_timestamp.strip() in message_heading and message_content.strip() in act_content:
                print("Message_content:",act_content)
                print("Report_heading:", message_heading)
                report_id = int(act.find_element(By.CSS_SELECTOR, 'a[class="broadcast-box_report-link__suJYa text-only"]').get_attribute('href').split("report/")[-1].removesuffix('/'))
                timestamp_found = True
                act.find_element(By.CSS_SELECTOR, 'a[class="broadcast-box_report-link__suJYa text-only"]').click()
                print(f"Message details for '{message_timestamp}' found and accessed")
                break
        if not timestamp_found:
            return {"error": "Required message not found"}
        
        boxes = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[class="campaign_scheduled-message__BCrXv campaign_campaign-steps__JOTCt mb-0"]')))
        content = ""
        Campaign, send_to, heading, list_name = "", "", "", ""
        print(driver.current_url)
        try:
            list_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'h1[class="page-header-title mb-0"]'))).text
            heading = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div[class="broadcast-box_header__LJVUl"]'))).text
            print("List:",list_name)
            print("heading:",heading)
            for box in boxes:
                try:
                    content = box.find_element(By.CSS_SELECTOR, 'div[class="broadcast-box_wrapper__Zm6eO"]').find_element(By.CSS_SELECTOR, 'i[class="sub-text"]').text
                except:
                    content = "message is template"
                Campaign = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="icon-inbox-black-filled broadcast-box_item-with-icon__YNeBK"]'))).text
                send_to = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="icon-contacts broadcast-box_item-with-icon__YNeBK"]'))).text
                print("Campaign name:", Campaign)
                print("Send to:", send_to)
        except Exception as e:
            print("Error while fetching campaign or send_to details:", e)
        reports_data = {}
        try:
            reports = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.reports-stats-list_stat__n5FxB')))
            for i, itm in enumerate(reports):
                    sub_elements = itm.find_elements(By.XPATH, ".//*")
                    if sub_elements:
                        reports_data.update({sub_elements[0].text :sub_elements[1].text})
            print("reports data:",reports_data)
        except Exception as e:
            print("Error while Fetching reports data")

        tbl_data = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'tr[class="ant-table-row ant-table-row-level-0 selectable"]')))
        for data in tbl_data:
            try:
                # Get all <td> elements in the current row
                details = data.find_elements(By.TAG_NAME, 'td')

                # Ensure there are enough <td> elements to avoid index errors
                if not details or len(details) < 4:
                    print("Skipping row due to insufficient data")
                    continue

                name = details[0].text  # First <td> contains the name

                # Determine the column with sub-elements
                category_index = None
                for i, itm in enumerate(details[1:]):
                    sub_elements = itm.find_elements(By.XPATH, ".//*")
                    if sub_elements:
                        category_index = i
                        break

                # Classify the name based on the column index
                if category_index == 0:
                    deliverd.append(name)
                elif category_index == 1:
                    failed.append(name)
                elif category_index == 2:
                    responded.append(name)
                elif category_index == 3:
                    opt_out.append(name)
                else:
                    print(f"Unexpected data structure for row: {name}")

            except Exception as e:
                print("Error while processing table data:", e)

        scraped_data = {
            "List_id": list_id,
            "List": list_name.strip(),
            "Msg_heading": heading.strip(),
            "Content": content.strip(),
            "deliverd": deliverd,
            "failed": failed,
            "responded": responded,
            "opt_out": opt_out,
            "Campaign": Campaign.strip(),
            "send_to": send_to.strip(),
            "reports": reports_data,
            "report_id": report_id
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
    finally:
        print("Process completed")

def async_process_list(data):
    driver = initialize_driver()
    list_id = data.get('list_id', '')
    message_content = data.get('message_content', '')
    message_timestamp = data.get('message_timestamp','')
    username = data.get("username", '')
    password = data.get("password", "")
    scrap_Data=process_list(driver, list_id, message_content, message_timestamp, username, password)
    print(scrap_Data)
