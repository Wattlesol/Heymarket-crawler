# Initialize WebDriver
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time

driver = webdriver.Chrome()
driver.implicitly_wait(1)
driver.maximize_window()

# Amazon URL
url = "https://www.amazon.com/s?k=iphone+accessories&adgrpid=81255912693&hvadid=673535400915&hvdev=c&hvlocphy=1011082&hvnetw=g&hvqmt=b&hvrand=5478681371910811608&hvtargid=kwd-2750142405&hydadcr=7545_13674059&tag=hydglogoo-20&ref=pd_sl_3y0kcuy0ab_b"
driver.get(url)
time.sleep(3)

collected_items = set()
# Find results
while True:
    try:
        board = driver.find_element(By.CSS_SELECTOR, 'span[data-component-type="s-search-results"]')
        print('Search Result Found....')

        results = board.find_elements(By.CSS_SELECTOR, 'div[role="listitem"]')
        print("Total Results:", len(results))

        items = []
        for result in results:
            # Scroll to each element
            driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", result)
            time.sleep(0.5)  # Allow some time for the scroll and potential lazy-loading

            try:
                name = result.find_element(By.TAG_NAME, 'h2').text
            except:
                continue

            try:
                reviews = result.find_element(By.CSS_SELECTOR, 'div[data-cy="reviews-block"]').text
            except:
                reviews = "N/A"

            try:
                price = result.find_element(By.CSS_SELECTOR, 'span.a-price-whole').text
            except:
                price = "N/A"

            print("Item:", name)
            print("Rating:", reviews)
            print("Price:", price)
            items.append((name, reviews, price))

        # Write to CSV
        with open("items.csv", 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if f.tell() == 0:  # Check if file is empty to write the header
                writer.writerow(["Name", "Reviews", "Price"])
            for item in items:
                if item in collected_items:
                    continue
                writer.writerow(item)

        # Check and click the "Next" button
        try:
            nextbtn = driver.find_element(By.CSS_SELECTOR, '.s-pagination-next')
            if nextbtn.is_enabled():
                nextbtn.click()
                time.sleep(2)  # Allow some time for the next page to load
            else:
                print("No more pages.")
                break
        except Exception as e:
            print("Next button not found or not clickable:", e)
            break

    except Exception as e:
        print("An error occurred:", e)
        break