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
from selenium.webdriver.common.alert import Alert
 

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
    driver.get("https://dcg-caf.intel.com/DCG/BHS_GNR_AP_Postsilicon_Github/plan_list/8826/")
    return driver  
def login(driver,username,password):
    username_field=driver.find_element(By.XPATH,"/html/body/div/div[3]/div[2]/form/ul/li[1]/input")
    password_field=driver.find_element(By.XPATH,"/html/body/div/div[3]/div[2]/form/ul/li[2]/input")
    login_button=driver.find_element(By.XPATH,"/html/body/div/div[3]/div[2]/form/ul/li[4]/input")
    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()
    driver.maximize_window()
def InputAtf(driver,artifactoryLink):
    time.sleep(3)    
    atf_button=driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[3]/div/div[2]/div/div[1]/form/div/div[1]/div[1]/div[5]/div/div[1]/div[2]/button")
    atf_button.click()
    time.sleep(3)
    atf_input=driver.find_element(By.XPATH,"/html/body/div[1]/div[10]/div/div/div[2]/div/input[2]")
    atf_input.send_keys(artifactoryLink)
    time.sleep(3)
    atf_close_button=driver.find_element(By.XPATH,"/html/body/div[1]/div[10]/div/div/div[1]/button")
    atf_close_button.click()
    time.sleep(3)
def InputSUTPoolIds(driver,platform_select,article_id_list):
    article_id_list=list(map(lambda x: int(x),article_id_list))

    platform_select=platform_select.upper()
    if len(platform_select)>9:
        platform_select=platform_select[:-1]
    print("Platform Name: ",platform_select)
    time.sleep(3)    
    dropdown = driver.find_element(By.ID, "sut_pool_list")
    driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
    wait = WebDriverWait(driver, 10)
    dropdown = wait.until(EC.element_to_be_clickable((By.ID, "sut_pool_list")))
    time.sleep(2)
    select = Select(dropdown)    
    
    try:
        select.select_by_value(platform_select)
        time.sleep(5)
        print("Item selected successfully.")
    except NoSuchElementException:
        print("Item not found in the dropdown.")
        return "Platform Unavailable"

    time.sleep(3)   

    statusCheck=driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[3]/div/div[2]/div/div[1]/form/div/div[1]/div[2]/div[3]/div[5]/div/table/tbody/tr[2]/td[2]")
    status=statusCheck.get_attribute("innerHTML").strip()
    print("Status: ",status)
    if(status!="IDLE"): return "Not IDLE" 


    span_element = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[3]/div/div[2]/div/div[1]/form/div/div[1]/div[3]/div[2]/div/div[3]/div[2]/div[1]/span/span")
    casenumber = int(span_element.get_attribute("innerHTML").strip())
    print("Case Number:", casenumber)
    print("type",type(casenumber))
    count=0
    delete_count=0
    i=1
    try:
        while i <= casenumber:
            time.sleep(1)
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
    time.sleep(2)

    # for i in range(1, int(casenumber)+1):
    #     table_xpath = f"//table[contains(@id, 'case-block-{i}')]/tbody/tr/td[3]/div/span[@class='content_font']"

    #     # Find all span elements containing the content
    #     span_element = driver.find_element(By.XPATH, table_xpath)
    #     text = span_element.get_attribute("innerHTML").strip()
    #     print(text)
    #     # Split the name_text to extract the test case number
    #     pattern = r'(\d{9,})'
    #     matches = re.findall(pattern, text)
    #     if matches:
    #         test_case_number = int(matches[0])
    #         print(test_case_number)
            
    #         # Check if the test case number is in the list of article IDs
    #         if test_case_number not in article_id_list:
    #             print("Found==",test_case_number)
    #             # checkbox_xpath = f"//ul/li[{i}]/table/tbody/tr/td[10]/input"                
    #             # checkbox = driver.find_element(By.XPATH, checkbox_xpath)
    #             # print("checkbox.is_enabled()",checkbox.is_enabled())
    #             # driver.execute_script("arguments[0].scrollIntoView();", checkbox)
    #             # checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, checkbox_xpath)))
    #             # driver.execute_script("arguments[0].click();", checkbox)
    #             # time.sleep(2)
    #             delete_button_xpath = f"//ul/li[{i}]/table/tbody/tr/td[11]/span[contains(@class, 'delete-case')]"
    #             delete_button = driver.find_element(By.XPATH, delete_button_xpath)                
    #             driver.execute_script("arguments[0].scrollIntoView();", delete_button)
    #             delete_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, delete_button_xpath)))
    #             driver.execute_script("arguments[0].click();", delete_button)                
    #             time.sleep(2) 
    #     else:
    #         print("Regex not matched",text)     
    #         delete_button_xpath = f"//ul/li[{i}]/table/tbody/tr/td[11]/span[contains(@class, 'delete-case')]"
    #         delete_button = driver.find_element(By.XPATH, delete_button_xpath)                
    #         driver.execute_script("arguments[0].scrollIntoView();", delete_button)
    #         delete_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, delete_button_xpath)))
    #         driver.execute_script("arguments[0].click();", delete_button)                
    #         time.sleep(2) 


def addEmails(driver,Emails):
    current_scroll_position = driver.execute_script("return window.scrollY")
    input_element = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[3]/div/div[2]/div/div[1]/form/div/div[1]/div[3]/div[4]/div/div/div[1]/input")
   
    driver.execute_script("arguments[0].scrollIntoView(true);", input_element)
    emails=str(Emails).split(', ')
    for item in emails:
        print("Added Email: ",item)
        input_element.send_keys(item)
        input_element.send_keys(Keys.ENTER)
        time.sleep(3)
    
    driver.execute_script(f"window.scrollTo(0, {current_scroll_position});")      

def checkStatus(platform):
    driver.execute_script("window.open('about:blank', 'new_tab')")

    # Switch to the new tab
    driver.switch_to.window("new_tab")

    # Open a new website in the new tab
    driver.get("https://dcg-caf.intel.com/DCG/BHS_GNR_AP_Postsilicon_Github/dut_edit_view/")
    searchInput=driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[3]/div[2]/div/div[1]/div/div[3]/input")
    # searchInput.send_keys(platform)
    time.sleep(3)
    sutTable=driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[3]/div[2]/div/div[1]/div/div[4]/table")
    rows=driver.find_element(By.TAG_NAME,"tr")
   
    print("rows: ",rows)
   
    for row in rows:
        print("Suttable2: ",row)
    time.sleep(4)
   
    

   

def start(ArtifactoryLink,Emails,Host_Name,ArticleIds,QueryId,testPlan):
    driver=get_driver()
    print("ArtifactoryLink: ",ArtifactoryLink)
    print("Emails: ",Emails)
    print("Host_Name: ",Host_Name)
    print("ArticleIds: ",ArticleIds)
    config = configparser.ConfigParser()    
    config_file_path="C:/FEAST/feast_app/config_data/config.ini"
    config.read(config_file_path)
    username = config['creds']['username']
    password = config['creds']['password']

    jsonPath="C:\\FEAST\\feast_app\\json_data\\AutomatedData.json"
    if os.path.exists(jsonPath):
        print("PathExist")
        with open(jsonPath, 'r') as file:
            data_dict = json.load(file)
    

    # print("username",username)
    # print("password",password)
    article_id_list=ArticleIds.split(', ')
    platform_select=Host_Name
   
    print("article_id_list: ",article_id_list)
    # Initialize the Edge browser
    # driver = webdriver.Chrome()
    login(driver,username,password)
    # InputAtf(driver,ArtifactoryLink)
    status=InputSUTPoolIds(driver,platform_select,article_id_list)
    #status='IDLE'
    if (status=="Not IDLE") or status=="Platform Unavailable" or status=="BUSY":
        print("IDLE OR NOT : ",status )
        data_dict[QueryId][testPlan]["Tcd Config details"][Host_Name]["Trigger status"]=status

        print("StatusIDLE OR NOT: ",status)
        with open(jsonPath, 'w') as json_file:
            json.dump(data_dict, json_file)
        driver.quit()
        return "Not IDLE"
    addEmails(driver,Emails)
    time.sleep(5)
    run_button=driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[3]/div/div[2]/div/div[1]/form/div/div[1]/div[3]/table/tbody/tr/td[2]/button")
    run_button.click()
    alert = driver.switch_to.alert 
    alert.accept()
    time.sleep(5)
    data_dict[QueryId][testPlan]["Tcd Config details"][Host_Name]["Trigger status"]="Under Execution"
    with open(jsonPath, 'w') as json_file:
        json.dump(data_dict, json_file)
    #post_silicon_automation_release_completed
    #driver.quit()
# start(ArtifactoryLink, Emails, Host_name, articleIds,QueryId,testPlan)
