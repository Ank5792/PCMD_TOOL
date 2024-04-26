from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

import time
import configparser
from selenium.webdriver.chrome.service import Service
import os
import json
import re
def get_driver():
    service=Service('C:\\FEAST\\feast_app\\chromedriver.exe')
    options=webdriver.ChromeOptions()
    options.add_argument("disable-infobars")
    options.add_argument("start-maximized")
    options.add_argument("disable-dev-shm-usage")
    options.add_argument("no-sandbox")
    options.add_experimental_option("excludeSwitches",["enable-automation"])
    options.add_argument("disable-blink-features=AutomationControlled")
 
    driver=webdriver.Chrome(service=service,options=options)
    #driver.get("http://automated.pythonanywhere.com/")
    return driver

driver=get_driver()
driver.get("https://dcg-caf.intel.com/DCG/BHS_GNR_AP_Postsilicon_Github/plan_list/8826")
time.sleep(3)  
platformName="BAIFWI486"
username_field = driver.find_element(By.XPATH, "/html/body/div/div[3]/div[2]/form/ul/li[1]/input")
password_field = driver.find_element(By.XPATH, "/html/body/div/div[3]/div[2]/form/ul/li[2]/input")
login_button = driver.find_element(By.XPATH, "/html/body/div/div[3]/div[2]/form/ul/li[4]/input")

username_field.send_keys("nsonal")
password_field.send_keys("IN@let$2024")
login_button.click()

driver.maximize_window()
time.sleep(3)  

status_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[3]/div/div[1]/div/ul[1]/li[2]/span")
status_button.click()
time.sleep(2)
# Wait until the table is displayed
table_locator = (By.XPATH, "/html/body/div[1]/div[1]/div[3]/div/div[2]/div/div[1]/form/div/div[2]/table")
wait = WebDriverWait(driver, 35)  # Increased timeout to 30 seconds

table_element = wait.until(EC.visibility_of_element_located(table_locator))
table_outerHTML = table_element.get_attribute('outerHTML')
print("Table is now visible!")
    # Find all rows in the table
rows = table_element.find_elements(By.TAG_NAME, "tr")

target_plan_name = "BHS_PostSilicon_Automated_Test_Cases_for_PCMD_Tool"
target_id = None

# Iterate through the rows
for row in rows:
    # Find the cell containing the "Plan Name" value
    cells = row.find_elements(By.TAG_NAME, "td")
    if len(cells) >= 2:
            # Extract plan name from the second cell
            plan_name_cell = cells[1]
            plan_name = plan_name_cell.text.strip()
            if plan_name == target_plan_name:
                # Extract the ID from the onclick attribute of the first cell
                id_cell = cells[0]
                target_id = id_cell.text.strip()                
                break

if target_id:
        print("Corresponding ID found:", target_id)
        # Open the link with the target ID appended
        target_url = f"https://dcg-caf.intel.com/DCG/BHS_GNR_AP_Postsilicon_Github/case_overview/{target_id}/"
        driver.get(target_url)
        print("Opened link with target ID appended:", target_url)

        # Wait for the page to load
        wait.until(EC.url_to_be(target_url))
        print("Page fully loaded.")
        time.sleep(5) 
        summary_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/ul/li[2]/span")
        summary_button.click()
        time.sleep(2)
        table_locator = (By.XPATH, "/html/body/div[1]/div[1]/div[3]/div[2]/table")
        wait = WebDriverWait(driver, 5)  
        table_element = wait.until(EC.visibility_of_element_located(table_locator))        
        rows = table_element.find_elements(By.TAG_NAME, "tr")
        # Initialize variables to count the number of each status
        passed_count = 0
        failed_count = 0
        running_count = 0
        notstarted_count = 0
        for row in rows:
            # Find the cell containing the "Plan Name" value
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 2:
                  
                status = cells[1].text.strip()
                    
                if status == "PASS":
                    passed_count += 1
                elif status == "FAIL":
                    failed_count += 1
                elif status == "RUNNING":
                    running_count += 1
                elif status == "NOTSTART":
                        notstarted_count += 1

        print("Number of test cases passed:", passed_count)
        print("Number of test cases failed:", failed_count)
        print("Number of test cases running:", running_count)
        print("Number of test cases not started:", notstarted_count)


else:
        print("Plan Name not found:", target_plan_name)



