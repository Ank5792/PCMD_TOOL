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

# def get_driver():
#     service=Service('C:\\PCMD\\pcmd_app\\chromedriver.exe')
#     options=webdriver.EdgeOptions()
#     options.add_argument("disable-infobars")
#     options.add_argument("start-maximized")
#     options.add_argument("disable-dev-shm-usage")
#     options.add_argument("no-sandbox")
#     options.add_experimental_option("excludeSwitches",["enable-automation"])
#     options.add_argument("disable-blink-features=AutomationControlled")
 
#     driver=webdriver.Edge(service=service,options=options)
#     #driver.get("http://automated.pythonanywhere.com/")
#     return driver
 

def start(ArtifactoryLink,Emails,Host_Name,ArticleIds):
    print("ArtifactoryLink: ",ArtifactoryLink)
    print("Emails: ",Emails)
    print("Host_Name: ",Host_Name)
    print("ArticleIds: ",ArticleIds)
    config = configparser.ConfigParser()    
    config_file_path="C:/FEAST/pcmd_app/config_data/config.ini"
    config.read(config_file_path)
    username = config['creds']['username']
    password = config['creds']['password']
    print("username",username)
    print("password",password)
    article_id_list=[1508605022,1508613272,1508604598,1508613322]
    platform_select="BAIFWI466"
    # Initialize the Edge browser
    driver = webdriver.Edge()
    # driver=get_driver()
    driver.get("https://dcg-caf.intel.com/DCG/BHS_GNR_AP_Postsilicon_Github/plan_list/8826/?username={}&password={}".format(username, password))
    time.sleep(3)    
    username_field=driver.find_element(By.XPATH,"/html/body/div/div[3]/div[2]/form/ul/li[1]/input")
    password_field=driver.find_element(By.XPATH,"/html/body/div/div[3]/div[2]/form/ul/li[2]/input")
    login_button=driver.find_element(By.XPATH,"/html/body/div/div[3]/div[2]/form/ul/li[4]/input")
    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()
    driver.maximize_window()
    time.sleep(3)    


    atf_button=driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[3]/div/div[2]/div/div[1]/form/div/div[1]/div[1]/div[5]/div/div[1]/div[2]/button")
    atf_button.click()
    time.sleep(3)
    atf_input=driver.find_element(By.XPATH,"/html/body/div[1]/div[10]/div/div/div[2]/div/input[2]")
    atf_input.send_keys("Enter valid link")
    time.sleep(3)

    atf_close_button=driver.find_element(By.XPATH,"/html/body/div[1]/div[10]/div/div/div[1]/button")
    atf_close_button.click()
    time.sleep(3)
    span_element = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[3]/div/div[2]/div/div[1]/form/div/div[1]/div[3]/div[2]/div/div[3]/div[2]/div[1]/span/span")
    time.sleep(3)    
    dropdown = driver.find_element(By.ID, "sut_pool_list")
    driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
    wait = WebDriverWait(driver, 10)
    dropdown = wait.until(EC.element_to_be_clickable((By.ID, "sut_pool_list")))
    select = Select(dropdown)
    
    try:
        select.select_by_value(platform_select)
        time.sleep(5)
        print("Item selected successfully.")
    except NoSuchElementException:
        print("Item not found in the dropdown.")

    casenumber = span_element.get_attribute("innerHTML").strip()
    print("Case Number:", casenumber)
    print("type",type(casenumber))

    for i in range(1, int(casenumber)+1):
        table_xpath = f"//table[contains(@id, 'case-block-{i}')]/tbody/tr/td[3]/div/span[@class='content_font']"

        # Find all span elements containing the content
        span_element = driver.find_element(By.XPATH, table_xpath)
        text = span_element.get_attribute("innerHTML").strip()
        print(text)
        if '[TC_' in text:
            # Split the name_text to extract the test case number
            test_case_number = int(text.split("[TC_")[1].split("]")[0])
            print(test_case_number)
            
            # Check if the test case number is in the list of article IDs
            if test_case_number not in article_id_list:
                print("Found==",test_case_number)
                checkbox_xpath = f"//ul/li[{i}]/table/tbody/tr/td[10]/input"                
                checkbox = driver.find_element(By.XPATH, checkbox_xpath)
                print("checkbox.is_enabled()",checkbox.is_enabled())
                driver.execute_script("arguments[0].scrollIntoView();", checkbox)
                checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, checkbox_xpath)))
                driver.execute_script("arguments[0].click();", checkbox)
                time.sleep(2)  
        else:
            print("Not matched==",text)
    current_scroll_position = driver.execute_script("return window.scrollY")
    input_element = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[3]/div/div[2]/div/div[1]/form/div/div[1]/div[3]/div[4]/div/div/div[1]/input")

    input_element.send_keys("ankita.hora@intel.com")
    input_element.send_keys(Keys.ENTER)
    time.sleep(2)
    input_element.send_keys("tejas.kawale@intel.com")
    input_element.send_keys(Keys.ENTER)
    time.sleep(2)
    driver.execute_script(f"window.scrollTo(0, {current_scroll_position});")      
    
    driver.quit()
start(1,2,3,4)
