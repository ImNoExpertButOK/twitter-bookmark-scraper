import time
import pickle
import csv
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

URL = "https://x.com/i/bookmarks"
driver = webdriver.Firefox()
screen_height = 900
index = 1
buffer = []

def save_cookies(driver):
    with open("cookies.pkl", 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)

def load_cookies(driver, file):
    with open(file, 'rb') as f:
        cookies = pickle.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)

def login_twitter():
    # Run this the first time you use this script.
    # This function will open a browser window and give you 30 seconds to login to Twitter.
    # Then it will export your cookies to cookies.pkl, which will be used to login
    # everytime you use the script.

    driver.get(URL)
    time.sleep(30)
    save_cookies(driver)
    driver.quit()

driver.get(URL)
time.sleep(5)
load_cookies(driver, "cookies.pkl")
driver.get(URL)
time.sleep(5)

# Change 4200 to alter how many scrolls it does. Could be an infinite loop, if you're willing to shut it down manually
for scroll in tqdm(range(1, 4200)):

    time.sleep(2)

    for i in range(1, 10):
        try:
            tweet = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[4]/section/div/div/div[{i}]/div/div/article/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[3]/a")
            link = tweet.get_attribute("href")

            if not link in buffer:
                buffer.append(link)

        except (NoSuchElementException, StaleElementReferenceException):
            pass

    with open("bookmarks.csv", "a") as f:
        writer = csv.writer(f)
        if len(buffer) >= 20:
            for line in buffer[0:4]:
                writer.writerow([index, line])
                index += 1
            del buffer[0:4]

    driver.execute_script(f"window.scrollTo(0, {screen_height}*{scroll});")

print("Links coletados:", index)
driver.quit()
