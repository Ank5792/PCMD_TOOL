from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
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

atf_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[3]/div/div[2]/div/div[1]/form/div/div[1]/div[1]/div[5]/div/div[1]/div[2]/button")
atf_button.click()
time.sleep(3)

atf_input = driver.find_element(By.XPATH, "/html/body/div[1]/div[10]/div/div/div[2]/div/input[2]")
atf_input.send_keys("2")
time.sleep(3)

atf_close_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[10]/div/div/div[1]/button")
atf_close_button.click()
time.sleep(3)

dropdown = driver.find_element(By.ID, "sut_pool_list")
driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)

wait = WebDriverWait(driver, 10)
dropdown = wait.until(EC.element_to_be_clickable((By.ID, "sut_pool_list")))

select = Select(dropdown)

platformName = "BAIFWI486"
try:
    select.select_by_value(platformName)    
    print("Item selected successfully.")
except NoSuchElementException:
    print("Item not found in the dropdown.")

time.sleep(5)

statusCheck = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[3]/div/div[2]/div/div[1]/form/div/div[1]/div[2]/div[3]/div[5]/div/table/tbody/tr[2]/td[2]")
status = statusCheck.get_attribute("innerHTML").strip()
print("Status: ", status)

span_element = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[3]/div/div[2]/div/div[1]/form/div/div[1]/div[3]/div[2]/div/div[3]/div[2]/div[1]/span/span")
casenumber = int(span_element.get_attribute("innerHTML").strip())
print("Case Number:", casenumber)
print("type",type(casenumber))
# 1508605372, 15010138680, 1508613698
article_id_list=['1508605372','1508613698','1508603037','16012520884']
article_id_list=list(map(lambda x: int(x),article_id_list))
row_processed = False
count=0
delete_count=0
i=1
try:
    while i <= casenumber:
        table_xpath = f"//table[contains(@id, 'case-block-{i}')]/tbody/tr/td[3]/div/span[@class='content_font']"
        span_element = driver.find_element(By.XPATH, table_xpath)
        text = span_element.get_attribute("innerHTML").strip()
        #print("Test case Heading: ",text)
        # pattern = r'(\d{9,})'
        pattern = r'(\d{8,12})'
        #//*[@id="case-block-45"]/tbody/tr/td[2]/div/span
        matches = re.findall(pattern, text)
        if matches:
            test_case_number = int(matches[0])
            #print("Test case Number: ",test_case_number)
            if test_case_number  in article_id_list:
                count+=1
              
                
                print(" found: ",text)
            else:
                print("Not Found :",text)
                
                #delete_button_xpath = f"//ul/li[{i}]/table/tbody/tr/td[11]/span/i"
                delete_button_xpath= f'//*[@id="case-block-{i}"]/tbody/tr/td[11]/span/i'
                #print("Xpath==",delete_button_xpath)
                delete_button = driver.find_element(By.XPATH, delete_button_xpath)                
                driver.execute_script("arguments[0].scrollIntoView();", delete_button)
                delete_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, delete_button_xpath)))
                driver.execute_script("arguments[0].click();", delete_button) 
                delete_count+=1
                #//*[@id="case-block-2"]/tbody/tr/td[11]/span/i
              
        else:
           
            print("IFWI FLshing found  : ",text)
            delete_button_xpath= f'//*[@id="case-block-{i}"]/tbody/tr/td[11]/span/i'
            #print("Xpath==",delete_button_xpath)
            delete_button = driver.find_element(By.XPATH, delete_button_xpath)                
            driver.execute_script("arguments[0].scrollIntoView();", delete_button)
            delete_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, delete_button_xpath)))
            driver.execute_script("arguments[0].click();", delete_button)
            delete_count+=1
        i+=1
except Exception as e:
    print("Finished : ",e)


print("Found test cases: ",count)


print("Deleted test cases : ",delete_count)

# while casenumber>0 :
#     i=1+count
#     if(casenumber<=len(article_id_list)):
#         break
#     while i<=casenumber :
#         try:
#             table_xpath = f"//table[contains(@id, 'case-block-{i}')]/tbody/tr/td[3]/div/span[@class='content_font']"
#             # Find all span elements containing the content
#             span_element = driver.find_element(By.XPATH, table_xpath)
#             text = span_element.get_attribute("innerHTML").strip()
#             print(text)
#             # Split the name_text to extract the test case number
#             pattern = r'(\d{9,})'
#             matches = re.findall(pattern, text)
#             if matches:
#                 test_case_number = int(matches[0])
#                 print(test_case_number)
                
#                 # Check if the test case number is in the list of article IDs
#                 if test_case_number not in article_id_list:
#                         print("Found==",test_case_number)
#                         # checkbox_xpath = f"//ul/li[{i}]/table/tbody/tr/td[10]/input"                
#                         # checkbox = driver.find_element(By.XPATH, checkbox_xpath)
#                         # print("checkbox.is_enabled()",checkbox.is_enabled())
#                         # driver.execute_script("arguments[0].scrollIntoView();", checkbox)
#                         # checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, checkbox_xpath)))
#                         # driver.execute_script("arguments[0].click();", checkbox)
#                         # time.sleep(2)
                        
#                         delete_button_xpath = f"//ul/li[{i}]/table/tbody/tr/td[11]/span/i"
#                         print("Xpath==",delete_button_xpath)
#                         delete_button = driver.find_element(By.XPATH, delete_button_xpath)                
#                         driver.execute_script("arguments[0].scrollIntoView();", delete_button)
#                         delete_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, delete_button_xpath)))
#                         driver.execute_script("arguments[0].click();", delete_button)   
#                         row_processed = True             
#                         time.sleep(2)
#                         break
#                 else:
#                     print("testcase matched :",test_case_number)
#                     row_processed=False
#                     break
#             else:
#                 print("Regex not matched",text)     
#                 delete_button_xpath = f"//ul/li[{i}]/table/tbody/tr/td[11]/span/i"
#                 print("Xpath==",delete_button_xpath)
#                 delete_button = driver.find_element(By.XPATH, delete_button_xpath)                
#                 driver.execute_script("arguments[0].scrollIntoView();", delete_button)
#                 delete_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, delete_button_xpath)))
#                 driver.execute_script("arguments[0].click();", delete_button)    
#                 row_processed = True
#                 time.sleep(2)          
#                 break
#         except NoSuchElementException:
#             break
        
        
        

#     casenumber = int(driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[3]/div/div[2]/div/div[1]/form/div/div[1]/div[3]/div[2]/div/div[3]/div[2]/div[1]/span/span").get_attribute("innerHTML").strip())
#     if not row_processed:
#         print("Inside == i's value ",i)
#         print("test_case_number",test_case_number)        
#         count=count+1
        
#     else:
#         # Reset the flag for the next iteration
#         row_processed = False


    


time.sleep(200)

current_scroll_position = driver.execute_script("return window.scrollY")

input_element = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[3]/div/div[2]/div/div[1]/form/div/div[1]/div[3]/div[4]/div/div/div[1]/input")

item = "tejas.kawale@intel.com"
print("Added Email: ", item)

try:
    driver.execute_script("arguments[0].scrollIntoView(true);", input_element)
   
    time.sleep(2)
    input_element.send_keys(item)
    input_element.send_keys(Keys.ENTER)
    input_element.send_keys('vinay1.kumar@intel.com')
    input_element.send_keys(Keys.ENTER)
    input_element.send_keys('ankita.hora@intel.com')
    input_element.send_keys(Keys.ENTER)
    print("Email successfully added.")
    time.sleep(5)
except Exception as e:
    print("An error occurred while adding the email:", str(e))

driver.execute_script(f"window.scrollTo(0, {current_scroll_position});")    