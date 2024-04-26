from flask import Blueprint,render_template,request,flash,redirect,url_for
from flask_login import login_required,current_user
from pcmd_app.utils.psql import get_all_projects,insert_new_project,get_all_saved_users,update_project
from pcmd_app.web.models import NewProject
from pcmd_app.utils.flask_utils import user_list_to_dictionary,clean_rec_project_data,get_statistics,increase_hits,get_latest_path
from flask import send_from_directory
from pcmd_app import app
from concurrent.futures  import ThreadPoolExecutor
from datetime import datetime,timedelta
from datetime import date
import pandas as pd
import threading
import redfish
import subprocess
import psycopg2
import openpyxl
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from pcmd_app.web.hsdes_api_handler import HsdesApiHandler
import pcmd_app.web.Repo_update as updater
# import pcmd_app.web.testAutomation as automater
import pcmd_app.web.temp as dimm_data
import os
import re
import numpy as np
import psycopg2
import openpyxl
import pandas as pd
import nltk
from nltk.corpus import stopwords
import string
import json
from flask import jsonify ,session
import pcmd_app.web.app_constants as app_constants
import time
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import configparser



web = Blueprint('web', __name__)
total_ids=1
count1=0
start_time=None
current_directory=os.getcwd()
#live_hw_sheet_path="C:\\PCMD\\database\\GNR.xlsx"
live_hw_sheet_path=os.path.join(current_directory,'database','GNR.xlsx')
master_sheet_path = os.path.join(os.getcwd(), 'database', 'Master_Sheet', 'master_sheet.xlsx')

handler = HsdesApiHandler(r"C:\\Users\\ahora\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\pip\\_vendor\\certifi\\cacert.pem")  # Instantiate the HsdesApiHandler class
global folder_name
os.environ["HTTPS_PROXY"] = "http://child-prc.intel.com:913"
os.environ["HTTP_PROXY"] = "http://child-prc.intel.com:913"

def get_normal(selected_id,folder_name):
  
    #identify_hw_requirement2 function to check data from DF sheet is already exist no need to code again
    #load the master sheet

    excel_file_path = f"C:/FEAST/database/GNR.xlsx"
    excel_file_path=os.path.join(current_directory,'database','GNR.xlsx')
    data = pd.read_excel(excel_file_path)
    

    print("data == ",type(data),"dat= ",data)    
    #json_file_path = f"C:/FEAST/database/{folder_name}/mapping.json"
    json_file_path=os.path.join(current_directory,'database',folder_name,'mapping.json')
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)

    
    # Check if the selected_id exists in the JSON data
    if str(selected_id) in json_data:
        # Assuming 'platform_id' is the key in the JSON data
        BMC_IP_list = json_data[selected_id].get('BMC_IP', [])
    else:
        print("did not fnd the article id ==",selected_id)

    non_reserved_data1 = data[data['BMC IP'].isin(BMC_IP_list)]
    print("non_reserved_data1 == \n",non_reserved_data1,"len== ",non_reserved_data1.shape[0])
    json_data = non_reserved_data1.to_dict(orient='records')
 

    return non_reserved_data1

@app.route('/get_data/<selected_id>/<path:wanted_path>')
def get_data(selected_id,wanted_path):
    # Connect to the PostgreSQL database
    print("selected_id",selected_id)
    print("wanted_path",wanted_path)
   
    username='root1'
    password='0penBmc1'
    #df=dimm_data.getDimmData(selected_id,username,password)
  
    print("we are looknig for this ip== ",selected_id)
    
    #json_file_path = "C:/FEAST/pcmd_app/json_data/dimm_output.json"
    json_file_path = os.path.join(wanted_path,'dimm_output.json')
    print("json path", json_file_path)
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)
        
    try:    
        jsonify_data=jsonify(json_data[selected_id])
    except :
        empty_json_object = []
        return empty_json_object
    return jsonify_data

@app.route('/get_data_article_id/<selected_id>')
def get_data_article_id(selected_id):
   
    print("We got data as == ",selected_id)
    selected_id=selected_id.split(',')
    folder_name=selected_id[0]
    
    BMC_IP=selected_id[2]
    query_id=selected_id[1]
    testcaseType=selected_id[3]
    print("Testcasetype : ",selected_id[3])
   
    if testcaseType=="Automated":
        rautodf=pd.read_excel(os.path.join(current_directory,"database",folder_name,"rautomated.xlsx"))
        rautodf=rautodf[rautodf['BMC IP']==BMC_IP]
        print("Display Df=",rautodf['Test Case / Article Ids'])
        article_ids=rautodf['Test Case / Article Ids']
        print("type= ",type(article_ids)," article ids : ",article_ids)
        article_ids_str=article_ids.tolist()
        article_ids_list=str(article_ids).split(', ')
        print("artilce id:: ",article_ids_list) 
    else:
        df_rmapping=pd.read_excel(os.path.join(current_directory,"database",folder_name,"rmapping.xlsx"))
        df_rmapping=df_rmapping[df_rmapping['BMC IP']==BMC_IP]
        print("Display Df=",df_rmapping)
        article_ids=df_rmapping['Test Case / Article Ids']
        print("type= ",type(article_ids)," article ids : ",article_ids)
        article_ids_str=article_ids.tolist()
        article_ids_list=str(article_ids_str[0]).split(', ')
        print("artilce id:: ",article_ids_list)

    #article_ids_list=article_ids.split(',')
    #print("Artilcle Ids== ",article_ids_list)

    pd.set_option('display.max_colwidth', None)
    df_csv=pd.read_csv(os.path.join(current_directory,"database",folder_name,f"{query_id}.csv"))
   
    # Write the DataFrame to an Excel file
   
    print("data from  csv\n",df_csv)
    dict={}

    base_url="https://hsdes-api.intel.com/rest/article/"
       

    for id in article_ids_list:
        # url=base_url + str(id)
        # data=handler.get_article_data(url)['data']
        # component=data[0]["component"]
        # title=data[0]["title"]
        # tag=data[0]["central_firmware.test_case_definition.pre_condition"]

        print("Id: ",id)
        pattern = r'(\d{8,12})'
       
        matches = re.findall(pattern, id)
        if matches:
            id = matches[0]
        else:
            continue
        df_csv['id'] = df_csv['id'].astype(str)
        df=df_csv[df_csv["id"]==id]
        print("df== ",df)
        title=df['title']
        print("title ",title)
        component=df['component']
        print("component ",component)
        tag=str(df['pre_condition'])

        
        tag=handler.remove_html_tags(tag)
        print("A: ",tag)
        pattern = r'\[GNR-AP_HW_requirement:\s*([^\]]+)\]'
        
        match = re.search(pattern, str(tag)) 
        print("after pattern matching: ",match)
        
    
        if match:   
            matched_string = match.group(0)     
            print("mathced string ",matched_string)
            pre_condition=matched_string
        else:
            pre_condition="No Hardware found"
      
       
        print("tag ",tag)
        dict[str(id)]={}
        dict[str(id)]["title"]=title
        dict[str(id)]["component"]=component
        dict[str(id)]["pre-condition"]=pre_condition



    print("dict== ",dict)
    df1=pd.DataFrame(dict)
    df1=df1.T
    df1.reset_index(inplace=True)
    df1.index=np.arange(1,len(df1)+1)    
    df1.columns=["id","title","component","pre-condition"]
    #print("data to send==",df1)
    json_data=df1.to_json(orient="records")
    #print("json data=",json_data)
    return json_data
@app.route('/get_data_pci/<selected_id>/<path:wanted_path>')
def get_data_pci(selected_id,wanted_path):
    # Connect to the PostgreSQL database
    
    username='root1'
    password='0penBmc1'
    #df=dimm_data.getDimmData(selected_id,username,password)
  
    print("we are looknig for this ip== ",selected_id)
    
    #json_file_path = "C:/FEAST/pcmd_app/json_data/pcicxl_output.json"
    json_file_path = os.path.join(wanted_path,'pcicxl_output.json')
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)
    try :    
        jsonify_data=jsonify(json_data[selected_id])
    except :
        empty_json_object = []
        return empty_json_object
    return jsonify_data

def Converting_json(folder_name,option):
   
    relative_path = os.path.join('database', folder_name, 'rmapping.xlsx')
    excel_file_path = os.path.join(current_directory, relative_path)
    #excel_file_path = f'C:\\PCMD\\database\\{folder_name}\\mapping.xlsx'
    df = pd.read_excel(excel_file_path)
    if(option==1):
        json_data = df.set_index('BMC IP').to_dict(orient='index')
    else:
        json_data = df.set_index('id').to_dict(orient='index')

        

    relative_path = os.path.join('database', folder_name, 'mapping.json')
    json_file_path = os.path.join(current_directory, relative_path)    
    #json_file_path = f'C:\\PCMD\\database\\{folder_name}\\mapping.json'
    with open(json_file_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=2)


def Converting_json1(option):
   
    df = pd.read_excel("HW.xlsx")
    if(option==2):
        json_data = df.set_index('BMC IP').to_dict(orient='index')
    else:
        json_data = df.set_index('id').to_dict(orient='index')

    with open("HW.json", 'w') as json_file:
        json.dump(json_data, json_file, indent=2)

def ConvertingToJson(folder_name):
    #excel_file_path = f'C:\\PCMD\\database\\{folder_name}\\mapping.xlsx'
    excel_file_path= os.path.join(current_directory,'database',folder_name,'mapping.xlsx')
    df = pd.read_excel(excel_file_path)
    
    df['BMC_IP'] = df['BMC_IP'].apply(lambda x: [str(i) for i in str(x).split('\n')] if pd.notna(x) else [])
    # Assuming 'column1' is the main key, convert the DataFrame to JSON
    json_data = df.set_index('article_id').to_dict(orient='index')

    # Save the JSON data to a file
    #json_file_path = f'C:\\PCMD\\database\\{folder_name}\\mapping.json'
    json_file_path= os.path.join(current_directory,'database',folder_name,'mapping.json')
    with open(json_file_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=2)

def UpdateMappingSheet1():   
    file_path ="HW.xlsx"

    # Read the Excel file
    data_df = pd.read_excel(file_path, engine="openpyxl")
    print("hw.xlsx")
    print("Datadf== ",data_df)
    GNR_Data= pd.read_excel( live_hw_sheet_path,engine="openpyxl")
    data_df_GNR =GNR_Data
    print("Initial sheet is ",data_df_GNR)
    # print("columns=  ",GNR_Data.columns)
    BMC_IP_list =set()
    
    for index, row in data_df.iterrows():
        # keyword = str(row['HW_Config']).lower()
        # keywords = keyword.split(' ')
        keyword = str(row['HW_Config']).lower()
        keywords = keyword.split(' ')
        print("keywords found== ",keywords)
        data_df_GNR =GNR_Data
        if keyword=='nan':
            list1=[2,4]
            DPS_DF=GNR_Data[GNR_Data['DIMM Qty'].isin(list1)]            
            BMC_IP_list=DPS_DF['BMC IP'].to_list()
            Platform_IP_list=DPS_DF['Platform ID'].to_list()
            hostname_list=DPS_DF['Host Name'].to_list()
            data_df.at[index, 'BMC_IP'] = ', '.join(map(str, BMC_IP_list))     
            data_df.at[index,'Platform Ids'] = ', '.join(map(str, Platform_IP_list))
            data_df.at[index,'Host Name']= ', '.join(map(str, hostname_list))

            continue    
      
        elif("dps" in keyword):
            print("found dps")
            dps=int(keyword[:-3])*2
            dps_list=[str(dps)]
            DPS_DF=GNR_Data[GNR_Data['DIMM Qty'].isin(dps_list)]            
            BMC_IP_list=DPS_DF['BMC IP'].to_list()
            Platform_IP_list=DPS_DF['Platform ID'].to_list()
            hostname_list=DPS_DF['Host Name'].to_list()
            data_df.at[index, 'BMC_IP'] = ', '.join(map(str, BMC_IP_list))     
            data_df.at[index,'Platform Ids'] = ', '.join(map(str, Platform_IP_list))
            data_df.at[index,'Host Name']= ', '.join(map(str, hostname_list))

            # print("found dps ",GNR_Data)


        for keyword in keywords:
            
            if(keyword.lower()=="1dps"):
                keyword=2
            elif(keyword.lower()=="2dps"):
                keyword=4    
            elif(keyword.lower()=="4dps"):
                keyword=8       
            elif(keyword.lower()=="12dps"):
                keyword=24  
            elif(keyword.lower()=="6dps"):
                keyword=12 
            elif(keyword.lower()=="8dps"):
                keyword=16    
            # Initialize an empty list to store matching platform_ids
            BMC_IP_list = set()
            platform_ids_list=set()
            Host_names_list=set()
            # Iterate over rows in the data DataFrame
            for data_index, data_row in data_df_GNR.iterrows():
                # Check if the keyword is present in any cell of the current row
                if any(str(keyword).lower() in str(cell).lower() for cell in data_row):
                    # Extract the "platform_id" from the current row
                  
                    BMC_IP = data_row['BMC IP']
                    platform_ids=data_row['Platform ID']
                    Host_names=data_row['Host Name']
                    #print("keyword== ",keyword," found ",BMC_IP)
                    # Append the platform_id to the list
                    BMC_IP_list.add(BMC_IP)
                    platform_ids_list.add(platform_ids)
                    Host_names_list.add(Host_names)
                   
           
           
            
            
            # Use the list to filter the DataFrame
            data_df_GNR = data_df_GNR[data_df_GNR['BMC IP'].isin(BMC_IP_list)]

        print("we got bmc ip list as== ",BMC_IP_list)  
        #print("data of GNR== ",data_df_GNR) 
        data_df.at[index, 'BMC_IP'] = ', '.join(map(str, BMC_IP_list))
        data_df.at[index, 'Platform Ids'] = ', '.join(map(str, platform_ids_list))
        data_df.at[index, 'Host Name'] = ', '.join(map(str, Host_names_list))

    
    #print("latest data df",data_df[['BMC_IP','Platform Ids']])
    data_df.to_excel("HW.xlsx", index=False, engine='openpyxl')


def UpdateMappingSheet(folder_name):
    #data_df = pd.read_excel( f'C:\\PCMD\\database\\{folder_name}\\mapping.xlsx',engine="openpyxl")
    current_directory = os.getcwd()

    relative_path = os.path.join('database', folder_name, 'mapping.xlsx')
    file_path = os.path.join(current_directory, relative_path)

    # Read the Excel file
    data_df = pd.read_excel(file_path, engine="openpyxl")
    data_df['All Host Names'] = "" 
    GNR_Data= pd.read_excel( live_hw_sheet_path,engine="openpyxl")
    data_df_GNR =GNR_Data
    #print("Initial sheet is ",data_df_GNR)
    # print("columns=  ",GNR_Data.columns)
    BMC_IP_list =set()
    Test_case_distribution={}
    Not_executable_TestCases=[]
    for index,row in  GNR_Data.iterrows():
        Test_case_distribution[row['BMC IP']]=0
    for index, row in data_df.iterrows():
        # keyword = str(row['HW_Config']).lower()
        # keywords = keyword.split(' ')
        keyword = str(row['HW_Config']).lower()
        keywords = keyword.split(' ')
        
        items_to_remove=["windows","centos","itp"]
        for key in keywords:
            for word in items_to_remove:
                if(key.lower()==word.lower()):
                    keywords.remove(key)  
        data_df_GNR =GNR_Data
        if keyword=='nan':
            list1=[2,4]
            DPS_DF=GNR_Data[GNR_Data['DIMM Qty'].isin(list1)]            
            BMC_IP_list=DPS_DF['BMC IP'].to_list()
            Platform_IP_list=DPS_DF['Platform ID'].to_list()
            hostname_list=DPS_DF['Host Name'].to_list()
            # data_df.at[index, 'BMC_IP'] = ', '.join(map(str, BMC_IP_list))     
            # data_df.at[index,'Platform Ids'] = ', '.join(map(str, Platform_IP_list))
            # data_df.at[index,'Host Name']= ', '.join(map(str, hostname_list))
           
           
            min_key = None
            min_value = float('inf')  # Set to positive infinity initially
            min_index = None

            # Iterate through the keys in the list
            for key in BMC_IP_list:
                # Check if the key exists in the dictionary and its value is less than the current minimum value
                if key in Test_case_distribution and Test_case_distribution[key] < min_value:
                    # Update the minimum key, value, and index
                    min_key = key
                    min_value = Test_case_distribution[key]
                    min_index = BMC_IP_list.index(key)

            Test_case_distribution[BMC_IP_list[min_index]]=Test_case_distribution[BMC_IP_list[min_index]]+1
            data_df.at[index, 'BMC_IP'] =     BMC_IP_list[min_index]
            data_df.at[index,'Platform Ids'] = Platform_IP_list[min_index]
            data_df.at[index,'Host Name']= hostname_list[min_index]
            continue    
  
                                 
        for keyword in keywords:
            if(keyword.lower()=="windows" or keyword.lower()=="centos" or keyword.lower()=="itp" or keyword.lower()=="2dps"):
                continue
            # Initialize an empty list to store matching platform_ids
            BMC_IP_list = set()
            platform_ids_list=set()
            Host_names_list=set()
            if("dps" in keyword.lower()):
                    dps=int(keyword[:-3])*2
                    print("dpssize: ",dps)
                    #DPS_DF=GNR_Data[GNR_Data['DIMM Qty']==dps]   
                    DPS_DF=data_df_GNR[data_df_GNR['DIMM Qty']==dps]  
                    data_df_GNR=DPS_DF 
                    print("Found this dps data:")
                    list1=DPS_DF['BMC IP'].to_list()
                    list2=DPS_DF['Platform ID'].to_list()
                    list3=DPS_DF['Host Name'].to_list()
                  
                    BMC_IP_list.update(list1)
                    platform_ids_list.update(list2)
                    Host_names_list.update(list3)

                    #print("found dps ",DPS_DF)
            elif("gb" in keyword.lower()) :
                size=int(keyword[:-2])
                
                size_df=GNR_Data[GNR_Data['DIMM Size/Capacity (Gb)']==size]    
                size_df=data_df_GNR[data_df_GNR['DIMM Size/Capacity (Gb)']==size]    
                data_df_GNR=size_df
                list1=size_df['BMC IP'].to_list()
                list2=size_df['Platform ID'].to_list()
                list3=size_df['Host Name'].to_list()
                
                BMC_IP_list.update(list1)
                platform_ids_list.update(list2)
                Host_names_list.update(list3)

               
                   
            # Iterate over rows in the data DataFrame
            else:
                for data_index, data_row in data_df_GNR.iterrows():
                    # Check if the keyword is present in any cell of the current row
                    if any(keyword.lower() in str(cell).lower() for cell in data_row):
                        # Extract the "platform_id" from the current row
                        BMC_IP = data_row['BMC IP']
                        platform_ids=data_row['Platform ID']
                        Host_names=data_row['Host Name']

                        # Append the platform_id to the list
                        BMC_IP_list.add(BMC_IP)
                        platform_ids_list.add(platform_ids)
                        Host_names_list.add(Host_names)

           
           
            
            
            # Use the list to filter the DataFrame
            data_df_GNR = data_df_GNR[data_df_GNR['BMC IP'].isin(BMC_IP_list)]
        BMC_IP_list=list(BMC_IP_list)
        platform_ids_list=list(platform_ids_list)
        Host_names_list=list(Host_names_list)
       
       
        min_key = None
        min_value = float('inf')  # Set to positive infinity initially
        min_index = None

        # Iterate through the keys in the list
        for key in BMC_IP_list:
            # Check if the key exists in the dictionary and its value is less than the current minimum value
            if key in Test_case_distribution and Test_case_distribution[key] < min_value:
                # Update the minimum key, value, and index
                min_key = key
                min_value = Test_case_distribution[key]
                min_index = BMC_IP_list.index(key)

        if min_index is not None:
            Test_case_distribution[BMC_IP_list[min_index]]=Test_case_distribution[BMC_IP_list[min_index]]+1
        # data_df.at[index, 'BMC_IP'] = ', '.join(map(str, BMC_IP_list))
        # data_df.at[index, 'Platform Ids'] = ', '.join(map(str, platform_ids_list))
        # data_df.at[index, 'Host Name'] = ', '.join(map(str, Host_names_list))
        if BMC_IP_list:
            data_df.at[index, 'BMC_IP'] = BMC_IP_list[min_index] 
            platform_id = GNR_Data.loc[GNR_Data['BMC IP'] ==  BMC_IP_list[min_index], 'Platform ID'].iloc[0]
            Host_name = GNR_Data.loc[GNR_Data['BMC IP'] ==  BMC_IP_list[min_index], 'Host Name'].iloc[0]
            data_df.at[index,'Platform Ids'] = platform_id
            data_df.at[index,'Host Name'] = Host_name
            pil=[]
            hnl=[]
            for ip in BMC_IP_list:
                platform_id = GNR_Data.loc[GNR_Data['BMC IP'] ==  ip, 'Platform ID'].iloc[0]
                Host_name = GNR_Data.loc[GNR_Data['BMC IP'] ==  ip, 'Host Name'].iloc[0]
                pil.append(platform_id)
                hnl.append(Host_name)
            pidn=', '.join(pil)
            hnn=', '.join(hnl)
            data_df.at[index,'All Host Names'] = hnn

        else:
            Not_executable_TestCases.append(row["id"])
        # if platform_ids_list:
        #     data_df.at[index,'Platform Ids'] = platform_ids_list[min_index]

        # if Host_names_list:
        #     data_df.at[index,'Host Name'] = Host_names_list[min_index]

    #print("Test_case_distribution: ",Test_case_distribution)
    #print("Not executable testcases: ",len(Not_executable_TestCases))
   
    # new_row_values={'id':"Not executable ids",'BMC_IP':'','Platform Ids':'','Host Name':''}
    # data_df.loc[len(data_df)] = new_row_values
    #print(Not_executable_TestCases)
    current_directory = os.getcwd()
    statusList=[]
    GNRdf=pd.read_excel(live_hw_sheet_path)
    for index,row in data_df.iterrows():
        hostName=str(row['Host Name']).strip()
        print("Seaching: ",hostName)
        status=""
        if "baifwi" in hostName.lower():
            status= GNRdf.loc[GNRdf['Host Name'] == hostName, 'Platform Status'].iloc[0]

        if status=="Automated":
            statusList.append("Automated")
        else:
            statusList.append("Manual")

    data_df['Platform Status']=statusList   
    relative_path = os.path.join('database', folder_name, 'mapping.xlsx')
    excel_file_path = os.path.join(current_directory, relative_path)

    data_df.to_excel(excel_file_path, index=False, engine='openpyxl')

    return Not_executable_TestCases

def fetch_hw_req_new(df,folder_name):
    dict1={}
    base_url="https://hsdes-api.intel.com/rest/article/"
    count=0
    for index in range(len(df.index)):   
        
        # data=handler.get_article_data(url)['data'] 
        # print("")       
        article_id=df.iat[index,0]
        # title=df.iat[index,1]
        url=base_url + str(article_id)
        data=handler.get_article_data(url)['data']
        component=data[0]["component"]
        title=data[0]["title"]
        tag=data[0]["tag"]
        
        #print(article_id," here " ,title," ",component)
        dict1[str(article_id)] = {'HW_Config': [], 'title': ""}
        #print("article id= ",article_id," title== ",title)
        #print(f"Processing article id : {article_id} and index: {index}")
       
        #dict1[str(article_id)]['title']=""
        url=base_url + str(article_id)   
        
        
      
                
        # print("tag== ",tag)
        # print("type== ",type(tag))
        keywords=tag.split(',')
        
        templates = {"OS_","DIMM_Vendor_", "DIMM_Size_","DIMM_Freq_","DIMM_Type_","DIMM_Rank_","DIMM_POP_","PCIE_Vendor_","CXL_","PCIE_Vendor_","PCIe_Speed_","PCI_Card_Slot_","RAS_CARD_","IFWI_Flasher_","Debug_"}
        
        # print("Keywords= ",keywords)
        try:
            result_list = [extract_string3(keyword, templates) for keyword in keywords]
            parts_to_remove = ["GB", "x2"] 
            # print(result_list)

            modified_list = remove_parts(result_list, parts_to_remove)
            
            result_list = extract_second_parts(modified_list)
           
            keywords=result_list
            #print("keywords= ",keywords)
        except :
            keywords=[]
            # print("HW Data is not in specific format")

        dict1[str(article_id)]['title']=title 
        dict1[str(article_id)]['HW_Config'] = ' '.join(keywords)
     
        # if(count==2):
        #     break
    #print("new Dictionary : ",dict1)
    
    df1=pd.DataFrame(dict1)
    df1=df1.T
    df1.reset_index(inplace=True)
    df1.index=np.arange(1,len(df1)+1)
    #print("dict1== ",dict1)
    df1.columns=["article_id","HW_Config","title"]
    
    #excel_file_path = f"C:\\PCMD\\database\\{folder_name}\\mapping.xlsx"
    excel_file_path=os.path.join(current_directory,'database',folder_name,'mapping.xlsx')
    # Use the to_excel method to convert and save the DataFrame to an Excel file
    #print("Query Id Data== \n",df1)
    try:
        df1.to_excel(excel_file_path, index=False)
        print("Mapping sheet created successfully")
    except Exception as e:
        print("File not created ==  ",e)
    

@web.route('/send_data_for_query', methods=['GET', 'POST'])
@login_required
def send_data_for_query():
    print("Inside the reserve")
    selected_rows = request.form.getlist('selected_rows[]')
    # selected_rows = request.form.getlist('time_selection[]')
    print("selected row== ",selected_rows)
    folder_name='random'
    try :
        folder_name=request.form["folder_name"]
    except:   
        print("Initially not found")    
    #excel_file_path=f"C:\\PCMD\\database\\{folder_name}\\mapping.xlsx"
    excel_file_path=os.path.join(current_directory,'database',folder_name,'mapping.xlsx')

    # Read the Excel file into a DataFrame
    df = pd.read_excel(excel_file_path)    
    selected_data = df.loc[df.index.isin(map(int, selected_rows))]
    
    #return render_template('reserve.html', columns=df.columns, df=df, selected_data=selected_data)   

def is_query_valid(query):
    pattern=r"^\\d+$"
    return bool(re.match(pattern,query))

def check_data(query_id,folder_name):
    if(query_id):
        df=extract_data(query_id,folder_name)     
        df1=get_article_ids(query_id,folder_name)
        #fetch_hw_req(df,folder_name)
        #fetch_hw_req_new(df,folder_name)                   
    else:
        pass

def extract_data(query_id,folder_name):
    filename=os.path.join(os.getcwd(),"database",folder_name,f"{query_id}.csv")
    print("csv path:",filename)
    
    if os.path.exists(filename):
        df = pd.read_csv(filename)
    else:
        data = handler.run_query_by_id(query_id)['data']
        df = pd.DataFrame(data)
        df.to_csv(filename,index=False)
    return df

dict1={}
count=0
def threaded_get_article_ids(article_id):
    base_url="https://hsdes-api.intel.com/rest/article/"
    url=base_url + str(article_id)   
    print("article_id ",article_id)
    data=handler.get_article_data(url)['data']
   
    # title=df.iat[index,1]
    url=base_url + str(article_id)
    data=handler.get_article_data(url)['data']


    component=data[0]["component"]
    title=data[0]["title"]
    #tag=data[0]["tag"]
    #HW-details=data[0]["pre-condition"]
    tag=data[0]["central_firmware.test_case_definition.pre_condition"]
    keywords=[]
    if(tag is not None):
        #dict1[str(article_id)].append(tag.split(","))
        # print(tag)
        tag=handler.remove_html_tags(tag)
        #print(tag)
        pattern = r'\[GNR-AP_HW_requirement:\s*([^\]]+)\]'            
        match = re.search(pattern, tag)            
        if match:
            hardware_details = match.group(1)
            hardware_list = [item.strip() for item in hardware_details.split(',')]
            #print("Hardware details:", hardware_list)
        else:
            print("No hardware details found.")

    
        keywords = hardware_list
        #formatting
        for i in range(len(keywords)):
            if(keywords[i]=="Any_DIMM_Config"):
                keywords[i]="DIMM_POP_1DPS"
                # keywords.append("DIMM_POP_2DPS")
                break



    templates = {"DIMM_Vendor_", "DIMM_Size_","DIMM_Freq_","DIMM_Type_","DIMM_Rank_","DIMM_POP_","PCIE_Vendor_","CXL_","PCIE_Vendor_","PCIe_Speed_","PCI_Card_Slot_","RAS_CARD_","IFWI_Flasher_","Debug_","OS_"}
    
    
    print("Keywords= ",keywords)
    try :
        result_list = [extract_string3(keyword, templates) for keyword in keywords]
        # parts_to_remove = ["GB", "x2"] 
        # print(result_list)

        # modified_list = remove_parts(result_list, parts_to_remove)
        # print(modified_list)
        # result_list = extract_second_parts(modified_list)
        print(result_list)
        keywords=result_list
        print("keywords= ",keywords)
    except:
        keywords=[]
        print("Non in Proper format for ip= ",article_id)

    keywords = [word for item in keywords for word in item.split("_")]    
    # items_to_remove=["Windows","CENTOS","ITP"]
    # for key in keywords:
    #     for word in items_to_remove:
    #         if(key==word):
    #             keywords.remove(key)
    #             break  
    dict1[str(article_id)] = {'title': "" ,'component':"",'HW_Config':""}
    dict1[str(article_id)]['title']=title 
    
    dict1[str(article_id)]['component']=component 
    dict1[str(article_id)]['HW_Config']=' '.join(keywords)
    print("article id: ",article_id)
    count=count+1
    print("countvalue: ",count)


def get_article_ids(query_id,folder_name):
    if(query_id):
        df=extract_data(query_id,folder_name)     
    article_id_list=[]
    for index in range(len(df.index)):   
        article_id_list.append(df.iat[index,0])
    print("Article Ids: ",article_id_list)
    print("Total Ids: ",len(article_id_list))
    start_time=datetime.now()
   
    with ThreadPoolExecutor(max_workers=30) as executer:
        executer.map(threaded_get_article_ids,article_id_list)
    end_time=datetime.now()
    print(f"Time taken for query{query_id}",end_time-start_time)
    # global count1
    # global total_ids
    # count1=0
    # total_ids=1
    # if(query_id):
    #     df=extract_data(query_id,folder_name) 
    
    # total_ids=df.shape[0]
      
    # dict1={}
    # base_url="https://hsdes-api.intel.com/rest/article/"
    # for index in range(len(df.index)):   
                   
    #     article_id=df.iat[index,0]
    #     title=df.iat[index,1]
    
    #     count1=count1+1
    #     print("article id= ",article_id," title== ",title)
    #     print(f"Processing article id : {article_id} and index: {index}")
       
    #     #dict1[str(article_id)]['title']=""
    #     url=base_url + str(article_id)   
    #     data=handler.get_article_data(url)['data']
    #     article_id=df.iat[index,0]
    #     # title=df.iat[index,1]
    #     url=base_url + str(article_id)
    #     data=handler.get_article_data(url)['data']
    #     component=data[0]["component"]
    #     title=data[0]["title"]
    #     tag=data[0]["tag"]
    #     #HW-details=data[0]["pre-condition"]
    #     tag=data[0]["central_firmware.test_case_definition.pre_condition"]
    #     keywords=[]
    #     if(tag is not None):
    #         #dict1[str(article_id)].append(tag.split(","))
    #         print(tag)
    #         tag=handler.remove_html_tags(tag)
    #         print(tag)
    #         pattern = r'\[GNR-AP_HW_requirement:\s*([^\]]+)\]'            
    #         match = re.search(pattern, tag)            
    #         if match:
    #             hardware_details = match.group(1)
    #             hardware_list = [item.strip() for item in hardware_details.split(',')]
    #             print("Hardware details:", hardware_list)
    #         else:
    #             print("No hardware details found.")
   
      
    #     keywords = hardware_list
    #     #----------------code to take tags as keywords---------

    #     # keywords=tag.split(',')
        
        # templates = {"DIMM_Vendor_", "DIMM_Size_","DIMM_Freq_","DIMM_Type_","DIMM_Rank_","DIMM_POP_","PCIE_Vendor_","CXL_","PCIE_Vendor_","PCIe_Speed_","PCI_Card_Slot_","RAS_CARD_","IFWI_Flasher_","Debug_","OS_"}
        
        
        # print("Keywords= ",keywords)
        # try :
        #     result_list = [extract_string3(keyword, templates) for keyword in keywords]
        #     parts_to_remove = ["GB", "x2"] 
        #     print(result_list)

        #     modified_list = remove_parts(result_list, parts_to_remove)
        #     print(modified_list)
        #     result_list = extract_second_parts(modified_list)
        #     print(result_list)
        #     keywords=result_list
        #     print("keywords= ",keywords)
        # except:
        #     keywords=[]
        #     print("Non in Proper format for ip= ",article_id)
    #     #-----------------------------------------------------------


    #     dict1[str(article_id)] = {'title': "" ,'component':"",'HW_Config':""}
    #     dict1[str(article_id)]['title']=title 
       
    #     dict1[str(article_id)]['component']=component 
    #     dict1[str(article_id)]['HW_Config']=' '.join(keywords)
        # if count1==7:
        #     pass
    df1=pd.DataFrame(dict1)
    df1=df1.T
    df1.reset_index(inplace=True)
    df1.index=np.arange(1,len(df1)+1)
    #print("dict1== ",dict1)
    df1.columns=["id","title","component","HW_Config"]
    
    #excel_file_path = f"C:\\PCMD\\database\\{folder_name}\\mapping.xlsx"
    current_directory = os.getcwd()

   

    relative_path = os.path.join('database', folder_name, 'mapping.xlsx')
    excel_file_path = os.path.join(current_directory, relative_path)
    # Use the to_excel method to convert and save the DataFrame to an Excel file
    print("Query Id Data== \n",df1)
    try:
        df1.to_excel(excel_file_path, index=False)
        print("Mapping sheet created successfully")
    except Exception as e:
        print("File not created ==  ",e)   
def fetch_hw_req(df,folder_name):
    dict1={}
   
    base_url="https://hsdes-api.intel.com/rest/article/"
    pattern1=r"(H.W|hw|HW).*?(<*?<\\/.*>)"
    pattern2='((H.W|HW|hw).*?)(?:(SW|S.W|sw))'
    count=0
    for index in range(len(df.index)):   
                   
        article_id=df.iat[index,0]
        title=df.iat[index,1]
        dict1[str(article_id)] = {'HW_Config': [], 'title': ""}
        print("article id= ",article_id," title== ",title)
        print(f"Processing article id : {article_id} and index: {index}")
       
        #dict1[str(article_id)]['title']=""
        url=base_url + str(article_id)   
        data=handler.get_article_data(url)['data']
        str1=''
        str2=''
        str3=''
        try:
            str1=data[0]["central_firmware.test_case_definition.pre_condition"]
            str2=data[0]["description"]
            str3=data[0]["test_case_definition.test_steps"]
        except:
            pass
       
        str1=re.sub('\\s+',' ',str1)
        str2=re.sub('\\s+',' ',str2)
        str3=re.sub('\\s+',' ',str3)
        
        dict1[str(article_id)]['title']=title 
        
        if re.findall(pattern2,str1) and len(handler.remove_html_tags((re.findall(pattern2,str1))[0][0]))>5:
            dict1[str(article_id)]['HW_Config'].append(handler.remove_html_tags((re.findall(pattern2,str1))[0][0]))
           
            
        elif re.findall(pattern1,str1):
            dict1[str(article_id)]['HW_Config'].append(handler.remove_html_tags((re.findall(pattern1,str1))[0][1]))
            
        elif re.findall(pattern2,str2) and len(handler.remove_html_tags((re.findall(pattern2,str2))[0][0]))>5:
            dict1[str(article_id)]['HW_Config'].append(handler.remove_html_tags((re.findall(pattern2,str2))[0][0]))  
            
        elif re.findall(pattern1,str2):
            dict1[str(article_id)]['HW_Config'].append(handler.remove_html_tags((re.findall(pattern1,str2))[0][1]))
           
        elif re.findall(pattern2,str3) and len(handler.remove_html_tags((re.findall(pattern2,str3))[0][0]))>5:
            dict1[str(article_id)]['HW_Config'].append(handler.remove_html_tags((re.findall(pattern2,str3))[0][0]))  
           
        elif re.findall(pattern1,str3):
            dict1[str(article_id)]['HW_Config'].append(handler.remove_html_tags((re.findall(pattern1,str3))[0][1]))
            
        if not dict1[str(article_id)]:
            dict1[str(article_id)]['HW_Config'].append("None")  
                

        count=count+1
        if(count==2):
            break
    
    #st.write(dict1)
    df1=pd.DataFrame(dict1)
    df1=df1.T
    df1.reset_index(inplace=True)
    df1.index=np.arange(1,len(df1)+1)
    #print("dict1== ",dict1)
    df1.columns=["article_id","HW_Config","title"]
    
    #excel_file_path = f"C:\\PCMDWD\\database\\{folder_name}\\mapping.xlsx"
    excel_file_path=os.path.join(current_directory,'database',folder_name,'mapping.xlsx')

    # Use the to_excel method to convert and save the DataFrame to an Excel file
    print("Query Id Data== \n",df1)
    try:
        df1.to_excel(excel_file_path, index=False)
        print("Mapping sheet created successfully")
    except Exception as e:
        print("File not created ==  ",e)
    
#------------code for checking the database every minute--------------------------

# Initialize the SQLAlchemy instance

# db = SQLAlchemy(web)
 
# # Define the metadata and the table
# metadata = MetaData()
# your_table = Table('hw_config', metadata, autoload_with=db.engine)

# def update_database():
#     # Query the database
#     conn = psycopg2.connect(
#         host="localhost",
#         database="feast_db",
#         port="5432",
#         user="postgres",
#         password="sonalnirmal"
#     )
#     cursor = conn.cursor()
#     query = "SELECT hw_id,platform_id,expiry_date,expiry_time,reserved from hw_config where reserved=true " 
#     cursor.execute(query) 
    
#     rows = cursor.fetchall()
    
    
#     if not rows:
#         return "<h1 style='color:green;'>You have not reserved hw.Thanks</h1>"
#         # Get the column names from the cursor description
#     columns = [desc[0] for desc in cursor.description]

#         # Create a DataFrame
#     data = pd.DataFrame(rows, columns=columns) 

    
#     data['expiry_date'] = pd.to_datetime(data['expiry_date']) # Convert 'date' column to datetime
#     data['minutes'] = data['expiry_time'].apply(lambda x: int(datetime.strptime(x, "%H:%M").hour * 60 + datetime.strptime(x, "%H:%M").minute))
    
#     data['time1'] = data['minutes'].apply(lambda x: pd.to_timedelta(x, unit='m')) # Convert 'time' column to timedelta
    
#     current_datetime = datetime.now()
    
#     # Calculate future date and time and store in 'future_datetime' column
#     data['future_datetime'] = data['expiry_date'] + data['time1']
    
#     # Calculate time left for reservation and store in 'time_left' column
#     data['time_left'] = data['future_datetime'] - current_datetime
    
#     # # Convert 'time_left' to minutes
#     data['time_left'] = data['time_left'].dt.total_seconds().div(60)
    
    
#     negative_time_rows = data[data['time_left'] <= 0]

#     # Extract the 'platform_id' for those rows
#     platform_ids = negative_time_rows['platform_id'].tolist()

#     print("time left== \n",data)
    
#     print("Anything Expired\n",platform_ids)
#     for platform_id in zip(platform_ids):
#         query = "UPDATE hw_config SET reserved=false,reservedby=NULL,expiry_date=NULL,expiry_time=NULL WHERE platform_id = %s" 
#         cursor.execute(query, (platform_id,)) 
#     conn.commit()
#     # Close connections
#     cursor.close()
#     conn.close()  
# #    result = db.session.query(your_table).filter(your_table.columns.time <= 0).all()
 
# #    # Update the database
# #    for row in result:
# #        db.session.query(your_table).filter(your_table.columns.platform_id == row.platform_id).update({your_table.columns.reserved: False})
 
# #    db.session.commit()
 
 

 
# # Create a background scheduler
# scheduler = BackgroundScheduler()
 
# # Schedule the update_database function to run every minute
# scheduler.add_job(update_database, 'interval', seconds=5)
 
# # Start the scheduler
# scheduler.start()


# #-------------------------------------------------------------------------------------------------------------



#handler = HsdesApiHandler(r"C:\\Users\\tkawale\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\certifi\\cacert.pem")  # Instantiate the HsdesApiHandler class
#os.environ["HTTPS_PROXY"] = "http://child-prc.intel.com:913"
#os.environ["HTTP_PROXY"] = "http://child-prc.intel.com:913"

def identify_hw_requirement2(article_id_to_find, data, data1):
       
    title = ""
    filtered_df = data1[data1["test_case_definition.id"] == article_id_to_find]
    if not filtered_df.empty:
        corresponding_title = filtered_df["title"].iloc[0]
        title = corresponding_title
        print(f"Title for Article ID {article_id_to_find}: {corresponding_title}")
    else:
        print(f"No matching record found for Article ID {article_id_to_find}")

    if title: 
        keywords = title.split('_')
        keys = [keyword for keyword in keywords if ' ' not in keyword]
        for key in keys:
            mask = data.apply(lambda row: row.astype(str).str.contains(key, case=False, na=False).any(), axis=1)
            if mask.any():
                data = data[mask]
    else:
        return pd.DataFrame()
    

    # After identifying the HW requirement, filter the dataframe to show only non-reserved items
    # if 'reserved' in data.columns:
    #        non_reserved_data = data[data['reserved'] == False]
       
    # else:
    #     print("The 'Reserved' column is not present in the dataset.")
    #     return

    return data


def identify_hw_requirement1(article_id_to_find, data, data1, data2):
   
    title = ""
    filtered_df = data1[data1["test_case_definition.id"] == article_id_to_find]
    if not filtered_df.empty:
        corresponding_title = filtered_df["title"].iloc[0]
        title = corresponding_title
        print(f"Title for Article ID {article_id_to_find}: {corresponding_title}")
    else:
        print(f"No matching record found for Article ID {article_id_to_find}")

    
    keywords = title.split('_')
    keys = [keyword for keyword in keywords if ' ' not in keyword]
    for key in keys:
        mask = data.apply(lambda row: row.astype(str).str.contains(key, case=False, na=False).any(), axis=1)
        if mask.any():
            data = data[mask]
    
    filtered_df = data2[data2["article_id"] == article_id_to_find]
    HW_requirement = filtered_df["HW_Config"].iloc[0]
    keys = HW_requirement.split(' ')
    hw = data.columns
    finalkeys = [key for key in keys for hw1 in hw if hw1.find(key) != -1]

    for key in finalkeys:
        mask = data.apply(lambda row: row.astype(str).str.contains(key, case=False, na=False).any(), axis=1)
        if mask.any():
            data = data[mask]

    # After identifying the HW requirement, filter the dataframe to show only non-reserved items
    if 'reserved' in data.columns:
           non_reserved_data = data[data['reserved'] == False]
       
    else:
        print("The 'Reserved' column is not present in the dataset.")
        return

    return non_reserved_data

# @web.route('/reserve',methods=['GET','POST'])
# @login_required
# def reserve():
#     print("Inside the reserve")
#     selected_rows = request.form.getlist('selected_rows[]')
#     selected_rows = request.form.getlist('time_selection[]')
#     selected_data = df.loc[df.index.isin(map(int, selected_rows))]
    
#     return render_template('reserve.html', columns=df.columns, df=df, selected_data=selected_data)


@web.route('/unreserve', methods=['GET', 'POST'])
@login_required
def unreserve():
 
    print("Inside the reserve")
    selected_rows = request.form.getlist('selected_rows[]')
    selected_rows = list(map(int, selected_rows))
    print("selected_rows== ",selected_rows)
    
    conn = psycopg2.connect(
        host="localhost",
        database="feast_db",
        port="5432",
        user="postgres",
        password="sonalnirmal"
    )
    cursor = conn.cursor()

    
    query = "SELECT hw_id,platform_id,expiry_date,expiry_time,reserved from hw_config WHERE reservedby= %s" 
    cursor.execute(query, (current_user.nick_name,)) 
    
    rows = cursor.fetchall()
    
    
    if not rows:
        return "<h1 style='color:green;'>You have not reserved hw.Thanks</h1>"
        # Get the column names from the cursor description
    columns = [desc[0] for desc in cursor.description]

        # Create a DataFrame
    data = pd.DataFrame(rows, columns=columns)    
    platform_ids = data.loc[selected_rows, 'platform_id'].tolist()
    print("platform_ids== ",platform_ids)
    table_html = data.to_html(classes='table table-striped', index=False)
    
    for platform_id in zip(platform_ids):
        query = "UPDATE hw_config SET reserved=false,reservedby=NULL,expiry_date=NULL,expiry_time=NULL WHERE platform_id = %s" 
        cursor.execute(query, (platform_id,)) 
        
    
    conn.commit()
    # Close connections
    cursor.close()
    conn.close()  

    return "<h1>Unreserved Successfully</h1>"

# @web.route('/send_reserve', methods=['GET', 'POST'])
# @login_required
# def send_reserve():
   
#     conn = psycopg2.connect(
#         host="localhost",
#         database="feast_db",
#         port="5432",
#         user="postgres",
#         password="sonalnirmal"
#     )
#     cursor = conn.cursor()

    
#     query = "SELECT hw_id,platform_id,expiry_date,expiry_time,reserved from hw_config WHERE reservedby= %s" 
#     cursor.execute(query, (current_user.nick_name,)) 
    
#     rows = cursor.fetchall()
    
    
#     if not rows:
#         return "<h1 style='color:green;'>You have not reserved hw.Thanks</h1>"
#         # Get the column names from the cursor description
#     columns = [desc[0] for desc in cursor.description]

#         # Create a DataFrame
#     data = pd.DataFrame(rows, columns=columns) 
    
    
#     data['expiry_date1'] = pd.to_datetime(data['expiry_date']) # Convert 'date' column to datetime
#     #data['expiry_date'] = pd.to_datetime(data['expiry_date']).dt.date
#     data['minutes'] = data['expiry_time'].apply(lambda x: int(datetime.strptime(x, "%H:%M").hour * 60 + datetime.strptime(x, "%H:%M").minute))
    
#     data['time1'] = data['minutes'].apply(lambda x: pd.to_timedelta(x, unit='m')) # Convert 'time' column to timedelta
    
#     current_datetime = datetime.now()
    
#     # Calculate future date and time and store in 'future_datetime' column
#     data['future_datetime'] = data['expiry_date1'] + data['time1']
    
#     # Calculate time left for reservation and store in 'time_left' column
#     data['time_left'] = data['future_datetime'] - current_datetime
    
#     # # Convert 'time_left' to minutes
#     data['time_left'] = data['time_left'].dt.total_seconds().div(60)
    
#     # Drop unnecessary columns
#     data = data.drop(['time1','future_datetime','expiry_date1'], axis=1)
#     print("data== ",data)
    
#     data['time_delta'] = pd.to_timedelta(data['time_left'], unit='m')

#     # Extract days, hours, and minutes from the timedelta
#     data['days'] = data['time_delta'].dt.days
#     data['hours'], remainder = divmod(data['time_delta'].dt.seconds, 3600)
#     data['minutes'] = remainder // 60

#     # Create a new column with the desired format
#     data['Time Left'] = data.apply(lambda row: f"{row['days']} days {row['hours']} hrs {row['minutes']} mins", axis=1)


#     # Drop intermediate columns if needed
#     data = data.drop(['time_delta','time_left','days', 'hours', 'minutes','reserved'], axis=1)
        
#     #4180 mins=== 2 days 23 hrs 3 mins left
    
#     # date = data['date'].tolist()
#     # time = data['time'].tolist()
    
#     # data['date'] = pd.to_datetime(data['date'])
#     # date_list = data['date'].tolist()
#     # days_left_list = [(datetime.now() - date).days for date in date_list]
#     # print("days_left_list== ",days_left_list)
    
#     # current_time = datetime.now().time()
#     # total_minutes = current_time.hour * 60 + current_time.minute
#     # time = [abs(total_minutes - time) for time in time]
#     # print("time== ",time)

#     # print("total_minutes",total_minutes)
#     # time_left_data="yet to cal"
#     # df['time_left'] = time_left_data
    
#     table_html = data.to_html(classes='table table-striped', index=False)
#     conn.commit()
#     # Close connections
#     cursor.close()
#     conn.close()  
    
#     return render_template('send_reserve.html',columns=data.columns, df=data,reserved_data=table_html)




@web.route('/reserve', methods=['GET', 'POST'])
@login_required
def reserve():
    print("Inside the reserve")
    selected_rows = request.form.getlist('selected_rows[]')
    selected_times1 = request.form.getlist('time_selection[]')
    clean_times = [time for time in selected_times1 if time]
    
    print("clean_times:", clean_times)
    
    selected_times = clean_times
    # Create a default mapping dictionary with empty strings for all rows
    default_times_dict = {row: '' for row in df.index}

    # Update the default dictionary with the selected times
    for row, time in zip(selected_rows, selected_times):
        if time:
            default_times_dict[int(row)] = time

    # Print for debugging
    selected_rows = list(map(int, selected_rows))
    df.loc[selected_rows, 'reserved'] = True
    print("username= ",current_user.nick_name)
    platform_ids = df.loc[selected_rows, 'platform_id'].tolist()
    df.loc[selected_rows,'reservedby']=current_user.nick_name
    print("Selected platform_ids:", platform_ids)
    print("Selected Rows:", selected_rows)
    print("Selected Times:", selected_times)
    print("Default Times Dictionary:", default_times_dict)

    # Map the selected times to the "time" column in the DataFrame
    df['time'] = df.index.map(default_times_dict)
    df.loc[selected_rows,'expiry_date']=date.today()
    print("default_times_dict== ",default_times_dict)
    
    # Connect to PostgreSQL database
    conn = psycopg2.connect(
        host="localhost",
        database="feast_db",
        port="5432",
        user="postgres",
        password="sonalnirmal"
    )

   
    cursor = conn.cursor()
    for hwid,clearn_times in zip(platform_ids,clean_times):
        print("hwId=",hwid)
        query = "UPDATE hw_config SET reserved = %s WHERE platform_id = %s" 
        cursor.execute(query, (True, hwid)) 
        
        query = "UPDATE hw_config SET reservedby = %s WHERE platform_id = %s" 
        cursor.execute(query, (current_user.nick_name, hwid)) 
        
        query = "UPDATE hw_config SET expiry_date = %s WHERE platform_id = %s" 
        date_string = clearn_times.split(" ")[0]
        print("date_string= ",date_string)
        date_object = datetime.strptime(date_string, "%Y-%m-%d").date()
        cursor.execute(query, (date_object,hwid))
        
        query = "UPDATE hw_config SET expiry_time = %s WHERE platform_id = %s" 
        hrs=int(clearn_times.split(" ")[1].split(":")[0])
        mins=int(clearn_times.split(" ")[1].split(":")[1])
        time=hrs*60+mins
        print("hrs == ",hrs,"min == ",mins," time== ",time)
        # time=str(time)
        cursor.execute(query, (clearn_times.split(" ")[1],hwid))
        
        
        conn.commit()

    # Close connections
    cursor.close()
    conn.close()    
    # Print for debugging
    print("DataFrame after mapping:")
    print(df)

    # Filter DataFrame to get the selected data
    selected_data = df.loc[df.index.isin(map(int, selected_rows))]
   
   
        
    #-----------------------------------------------------------------
    conn = psycopg2.connect(
        host="localhost",
        database="feast_db",
        port="5432",
        user="postgres",
        password="sonalnirmal"
    )
    cursor = conn.cursor()

   
    query = "SELECT * from hw_config WHERE reservedby= %s" 
    cursor.execute(query, (current_user.nick_name,)) 
    
    rows = cursor.fetchall()
    
    
    if not rows:
        return "<h1 style='color:green;'>You have not reserved hw.Thanks</h1>"
        # Get the column names from the cursor description
    columns = [desc[0] for desc in cursor.description]

        # Create a DataFrame
    data = pd.DataFrame(rows, columns=columns)    
    selected_data = data[data['platform_id'].isin(platform_ids)]
    
    conn.commit()
    # Close connections
    cursor.close()
    conn.close()  
    
    #----------------------------------------------------------------------------------------------
    
    

    return render_template('reserve.html', columns=df.columns, df=selected_data, selected_data=selected_data)

def createFolder():
    
    # Change this to your desired directory path
    path=os.getcwd()  
    
    # Create the folder
    try:
        folder_path = os.path.join(path, 'database', 'Execution_Dump')
        os.makedirs(folder_path)
        print("Databse folder created")
    except:
        print("Failed to create database folder")

    
    #path = "C:/PCMDWD/database"  
    path=os.path.join(current_directory,'database')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Define the folder name using the timestamp
    folder_name = f"folder_{timestamp}"
    # Create the folder
    try:
        folder_path = os.path.join(folder_path, folder_name)
        os.makedirs(folder_path)
        print("Folder creaed for query_id dumps")
    except Exception as e:
        print("Failed to create folder for query_id dummps " )
        
    return folder_name    
def extract_string3(keyword, templates):
   
    for template in templates:
        if keyword.startswith(template):
            return keyword[len(template):]
    return keyword    
   
def extract_second_parts(original_list):
    second_parts_list = []

    for string in original_list:
        words = string.split('_')
        if len(words) > 1:
            second_parts_list.append(words[0])
            second_parts_list.append(words[1])
        else:
            second_parts_list.append(string)
    return second_parts_list

def send_2DPS_Data():
     list1=[2,4]
     excel_file_path=live_hw_sheet_path
     df = pd.read_excel(excel_file_path)
     df=df[df['DIMM Qty'].isin(list1)]
     return df     

def remove_parts(original_list, parts_to_remove):
    modified_list = []

    for string in original_list:
        modified_string = string
        for part in parts_to_remove:
            modified_string = modified_string.replace(part, '')

        modified_list.append(modified_string)

    return modified_list       
def fetchHwConfigArticleId(article_id):
    base_url="https://hsdes-api.intel.com/rest/article/"       
    url=base_url + str(article_id)   
    data=handler.get_article_data(url)['data']
    tag=data[0]["tag"]
    
    print("tag== ",tag)
    print("type== ",type(tag))
    if(tag==''):
        return send_2DPS_Data()
    keywords=tag.split(',')
    



    templates = {"DIMM_Vendor_", "DIMM_Size_","DIMM_Freq_","DIMM_Type_","DIMM_Rank_","DIMM_POP_","PCIE_Vendor_","CXL_","PCIE_Vendor_","PCIe_Speed_","PCI_Card_Slot_","RAS_CARD_","IFWI_Flasher_","Debug_","OS_"}


    # VendorDetails=["Hynix","Micron"]
    # VendorTemplate={"DIMM_Vendor_"}
    
    # DimmSizeDetails=[]
    # DimmSizeTemplate={"DIMM_size_"}
    
    # DimmFreqDetails=[]
    # DimmFreqTemplate={"DIMM_Freq_"}
    
    # DimmTypeDetails=[]
    # DimmTypeTemplate={"DIMM_Type_"}
    
    # DimmRankDetails=[]
    # DimmRankTemplate={"DIMM_rank_"}

    # PCIeDetails=[]
    # PCITemplate={"PCIe_"}
    
    # CXLDetails=[]   
    # CXLTemplate={"CXL_"}
    
    print("Keywords= ",keywords)
    try :
        result_list = [extract_string3(keyword, templates) for keyword in keywords]
        parts_to_remove = ["GB", "x2"] 
        print(result_list)

        modified_list = remove_parts(result_list, parts_to_remove)
        print(modified_list)
        result_list = extract_second_parts(modified_list)
        print(result_list)
        keywords=result_list
    except:
        keywords=[] 
    
    
    platform_ids_list =set()  # List to store platform IDs for the current row
        
    excel_file_path = live_hw_sheet_path  
    data_df=pd.read_excel(excel_file_path,sheet_name='Sheet2')      
    # Iterate over keywords
    # for keyword in keywords:    
    #     print("keyword=== ", keyword)
        
    #     # Iterate over rows in the data DataFrame
    #     for data_index, data_row in data_df.iterrows():
    #         # Check if the keyword is present in any cell of the current row
    #         #print("data_row== ", data_row)
    #         if any(keyword in str(cell) for cell in data_row):
    #             # Extract the "platform_id" from the current row
              
    #             platform_id = data_row['BMC IP']

    #             # Append the platform_id to the list
    #             platform_ids_list.add(platform_id)
                
    # filtered_df = data_df[data_df['BMC IP'].isin(platform_ids_list)]
    # print("platform_ids_list==",platform_ids_list )
    
   
    # Initialize an empty list to store matching platform_ids
    platform_ids_list = []
    if len(keywords)==0 :
        return data_df
    # Iterate over rows in the data DataFrame
    for keyword in keywords:
        print("keyword=== ", keyword)
        
        # Initialize an empty list to store matching platform_ids
        platform_ids_list = []
        
        # Iterate over rows in the data DataFrame
        for data_index, data_row in data_df.iterrows():
            # Check if the keyword is present in any cell of the current row
            if any(keyword.lower() in str(cell).lower() for cell in data_row):
                # Extract the "platform_id" from the current row
                platform_id = data_row['BMC IP']
                # Append the platform_id to the list
                platform_ids_list.append(platform_id)

        # Use the list to filter the DataFrame
        print("platform_ids_list= ",platform_ids_list)
        data_df = data_df[data_df['BMC IP'].isin(platform_ids_list)]
        print("data_df==",data_df )
# Now data_df contains only the rows where 'BMC IP' column has values matching any keyword



    print("filtered_df==",data_df )
    return data_df
    

def get_selected_data(selected_data):
    
    main_BMC_IP=set()
    for index,row in selected_data.iterrows():
        BMC_IPS=row['BMC_IP']
        BMC_IPS_list=str(BMC_IPS).split(', ')
        print("BMC_IPS_list= ",BMC_IPS_list)
        for ip in BMC_IPS_list:
            if(ip!='nan'):
                main_BMC_IP.add(ip)
        BMC_IPS_list=[]
    print("main_BMC_IP == ",main_BMC_IP)    
    excel_file_path=live_hw_sheet_path
    df1 = pd.read_excel(excel_file_path)

    filtered_df = df1[df1['BMC IP'].isin(main_BMC_IP)]
    return filtered_df

@app.route('/progress')
def start_task():
  
    #print("progress= ",session['progress'])   
    #print("count1= ",count1," progress== ",progress," total_ids= ",total_ids)
    progress=count1
    start_time = session.get('start_time', None)
    elapsed_time = round(time.time() - start_time,  2) if start_time else  0
    return jsonify({'progress': progress, 'elapsed_time': elapsed_time,'total_ids':total_ids})




@app.route('/progress1/<percent>')
def start_task1(percent):
    
    dimm_path=os.path.join(current_directory,'pcmd_app','json_data','dimm_output.json')
    bios_path=os.path.join(current_directory,'pcmd_app','json_data','biosVersion_output.json')
    pcie_path=os.path.join(current_directory,'pcmd_app','json_data','pcicxl_output.json')

    if(os.path.exists(dimm_path) and int(percent)==0):
        percent=25
    elif(os.path.exists(bios_path) and int(percent)==25):
        percent=50
    elif(os.path.exists(pcie_path) and int(percent)==50):
        percent=75
    elif( int(percent)==75):
        percent=100


 
    
   
    return jsonify({'progress': percent})

def change_mapping1():
   
  
    df1 = pd.read_excel("HW.xlsx")

    # Initialize an empty dictionary
    dict1 = {}

    # Iterate over rows in df1
    for index, row in df1.iterrows():
        article_id = row['id']
        BMCI_IPS = row['BMC_IP']
       
        BMCI_IP_list = str(BMCI_IPS).split(', ')
       
        #print("BMCI_IP_list == ",BMCI_IP_list)
        if(BMCI_IP_list[0]!='nan'):
            for ip in BMCI_IP_list:
                #print("ip== ",ip)
                if ip in dict1 :
                    dict1[ip].append(article_id)
                else:
                    dict1[ip] = [article_id]
                
    # Convert lists of IDs to comma-separated strings
    for key in dict1:
        ids = ", ".join(map(str, dict1[key]))  # Convert IDs to string before joining
        dict1[key] = ids

    data = [(key, value) for key, value in dict1.items()]

    # Create DataFrame from the list
    df2 = pd.DataFrame(data, columns=['BMC IP', 'Test Case / Article Ids'])
    # Create DataFrame df2 from dict1
    #print("dict1= ",dict1)
    # df2 = pd.DataFrame(dict1)  

    # df2.columns = ["BMC IP", "Matching Article ids"]

    # Print and save df2
    print("dict1=: ",dict1)
    print(df2)
    print("df1= ",df2)
   
    print("df1= ",df2) 
    #excel_file_path=f"C:\\PCMD\\database\\{folder_name}\\mapping.xlsx" 
    
    
    GNR_Data = pd.read_excel(live_hw_sheet_path)
    for index, row in df2.iterrows():
        value = row['BMC IP']
            
        host = GNR_Data.loc[GNR_Data['BMC IP'] == value, 'Host Name'].values[0]
        platform = GNR_Data.loc[GNR_Data['BMC IP'] == value, 'Platform ID'].values[0]
        
        # Assign values to corresponding rows in df2
        df2.at[index, 'Host Name'] = host
        df2.at[index, 'Platform ID'] = platform


    df2 = df2[["BMC IP","Host Name","Platform ID","Test Case / Article Ids"]]
    # relative_path = os.path.join('database', folder_name, 'rmapping.xlsx')
    # excel_file_path = os.path.join(current_directory, relative_path)
    df2.to_excel("rHW.xlsx", index=False)         



def change_mapping(folder_name,non_executable_testCases):
    current_directory=os.getcwd()
    relative_path = os.path.join('database', folder_name, 'mapping.xlsx')
    excel_file_path = os.path.join(current_directory, relative_path) 
    #excel_file_path=f"C:\\PCMD\\database\\{folder_name}\\mapping.xlsx"
    df1 = pd.read_excel(excel_file_path)

    # Initialize an empty dictionary
    dict1 = {}

    # Iterate over rows in df1
    for index, row in df1.iterrows():
        article_id = row['id']
        BMCI_IPS = row['BMC_IP']
       
        BMCI_IP_list = str(BMCI_IPS).split(', ')
       
        print("BMCI_IP_list == ",BMCI_IP_list)
        if(BMCI_IP_list[0]!='nan'):
            for ip in BMCI_IP_list:
                print("ip== ",ip)
                if ip in dict1 :
                    dict1[ip].append(article_id)
                else:
                    dict1[ip] = [article_id]
                
    # Convert lists of IDs to comma-separated strings
    #dictionary to show size
    size_dict={}
    for key in dict1:
        size_dict[key]=len(dict1[key])

    for key in dict1:
        ids = ", ".join(map(str, dict1[key]))  # Convert IDs to string before joining
        dict1[key] = ids 
    print("Non : ",non_executable_testCases)

    dict1["NO IP"]=", ".join(map(str, non_executable_testCases))
    data = [(key, value) for key, value in dict1.items()]

    # Create DataFrame from the list
    df2 = pd.DataFrame(data, columns=['BMC IP', 'Test Case / Article Ids'])
    # Create DataFrame df2 from dict1
    print("dict1= ",dict1)
    # df2 = pd.DataFrame(dict1)  

    # df2.columns = ["BMC IP", "Matching Article ids"]

    # Print and save df2
    print("dict1=: ",dict1)
    print(df2)
    print("df2= ",df2)

    #excel_file_path=f"C:\\PCMD\\database\\{folder_name}\\mapping.xlsx" 
    
    
    GNR_Data = pd.read_excel(live_hw_sheet_path)
    for index, row in df2.iterrows():
        value = row['BMC IP']
        if(value!="NO IP"):    
            host = GNR_Data.loc[GNR_Data['BMC IP'] == value, 'Host Name'].values[0]
            platform = GNR_Data.loc[GNR_Data['BMC IP'] == value, 'Platform ID'].values[0]
    
            print("ids== ",ids)
            
            # Assign values to corresponding rows in df2
            df2.at[index, 'Host Name'] = host
            df2.at[index, 'Platform ID'] = platform
        else:
            df2.at[index, 'Host Name'] = "NO host"
            df2.at[index, 'Platform ID'] = "NO platform"


    df2 = df2[["BMC IP","Host Name","Platform ID","Test Case / Article Ids"]]
    def add_size(ip):
        if(ip=="NO IP"): return f"Test cases Info_{len(non_executable_testCases)}"
        return f'Test cases Info_{size_dict[ip]}'

    # Apply the function to each row in the DataFrame
    df2["Test cases Info"] = df2["BMC IP"].apply(add_size)
    relative_path = os.path.join('database', folder_name, 'rmapping.xlsx')
    excel_file_path = os.path.join(current_directory, relative_path)
    statusList=[]
    GNRdf=pd.read_excel(live_hw_sheet_path)
    for index,row in df2.iterrows():
        hostName=row['Host Name'].strip()
        print("Seaching: ",hostName)
        if "baifwi" in hostName.lower():
            status= GNRdf.loc[GNRdf['Host Name'] == hostName, 'Platform Status'].iloc[0]

        if status=="Automated":
            statusList.append("Automated")
        else:
            statusList.append("Manual")

    df2['Platform Status']=statusList    
    df2.to_excel(excel_file_path, index=False)         
  
def ShowAutomatedData(option,folder_name,query_id):
    print("In show automated")
    if(option=="option2"):
        rautomatedExcelPath = os.path.join(current_directory,'database',folder_name,'rautomated.xlsx') 
        if os.path.exists(rautomatedExcelPath):
            return pd.read_excel(rautomatedExcelPath)
        dict1={}
        GNRSheet=pd.read_excel(live_hw_sheet_path)
        for index,row in GNRSheet.iterrows():
            status=row['Platform Status']
            print("status: ",status)
            if status=="Automated":
                #print("Found Automated Platorm: ",row['Host Name'])
                if len(row['Host Name'])>9:
                    dict1[row['Host Name'][:-1]]={}
                    dict1[row['Host Name'][:-1]]['count']=0
                    dict1[row['Host Name'][:-1]]['ArticleIds']=[]
                else:
                    dict1[row['Host Name']]={}
                    dict1[row['Host Name']]['count']=0
                    dict1[row['Host Name']]['ArticleIds']=[]
            else:
                pass
                #print("Not found platnfrom")

        df1 = pd.read_excel(os.path.join(current_directory, 'database', folder_name, 'rmapping.xlsx'))
        df2 = pd.read_csv(os.path.join(current_directory, 'database', folder_name, f"{query_id}.csv"))
        df3 = pd.read_excel(os.path.join(current_directory, 'database', folder_name, 'mapping.xlsx'))

        print("Before dict:1 ",dict1 )
        dict1['No Automated host']={}
        dict1['No Automated host']['count']=0
        dict1['No Automated host']['ArticleIds']=[]
        for index, row in df3.iterrows():
            articleid = row['id']
            corresponding_value = df2.loc[df2['id'] == int(articleid), 'automation_status'].iloc[0]
            corresponding_value_postSilicon=df2.loc[df2['id'] == int(articleid), 'post_silicon_automation_release_completed'].iloc[0]
            #print(f"For id{articleid} vlaue:{corresponding_value} postsilicon:{corresponding_value_postSilicon}")
            if corresponding_value == "In Production" and corresponding_value_postSilicon=="bios.birchstream_graniterapids-ap":
                #print("row['All Host Names']: ",row['All Host Names'])
                allHostNames=str(row['All Host Names']).split(', ')
                print(allHostNames)
                import sys
                MinAssignvalue=sys.maxsize
                MinAssignPlatform=""
                for hostName in allHostNames:
                    #print("lenght: ",len(hostName))
                    if hostName.strip()=="baifwi486":
                        print("We found baifwi486")
                    #print("looking for host name: ",hostName)
                    hostName=hostName.strip()
                    if hostName in dict1:
                        print("Host namae found: ",hostName," with count: ",dict1[hostName]['count'])
                        if dict1[hostName]['count'] < MinAssignvalue:
                            MinAssignvalue=dict1[hostName]['count']
                            MinAssignPlatform=hostName

                    else:
                        continue

                if MinAssignPlatform:
                    dict1[MinAssignPlatform]['count']+=1
                    dict1[MinAssignPlatform]['ArticleIds'].append(str(articleid))
                else:
                    dict1['No Automated host']['count']+=1
                    dict1['No Automated host']['ArticleIds'].append(str(articleid))

            #print("MinAssignPlatform: ",MinAssignPlatform)
        print("Automated dict1: ",dict1)
        print("df2\n",df2)

        for index,row in df1.iterrows():
            if row['Host Name'].strip() in dict1:
               
                row['Test cases Info']=f'Test cases Info_{len(dict1[row['Host Name'].strip()]['ArticleIds'])}'
                row['Test Case / Article Ids']=', '.join(dict1[row['Host Name'].strip()]['ArticleIds'])

            else:
                row['Test cases Info']="No Automated Test Case Found"
        Nolength=len( dict1['No Automated host']['ArticleIds'])
        new_row={
            "BMC IP":"No Automated IP",
            "Host Name":"No Automated host",
            "Platform ID": "No Automated Platform",
            "Test Case / Article Ids": ', '.join(dict1['No Automated host']['ArticleIds']),
            "Test cases Info": f"Test cases Info_{Nolength}",
            "Platform Status": "No Status"
        }
        df1 = df1._append(new_row, ignore_index=True)
        df1.to_excel(rautomatedExcelPath,index=False)     
                    
        # for index, row in df1.iterrows():
        #     articleids = str(row['Test Case / Article Ids']).split(', ')
        #     articleids = list(map(str.strip, articleids)) 
        #     automatedIds = []
        #     for articleid in articleids:
        #         #print("1article id: ",articleid)
        #         matching_rows = df2[df2['id'].astype(str)  == str(articleid)]
        #         if not matching_rows.empty:
        #             # corresponding_value = matching_rows['automation_status'].iloc[0]
        #             # corresponding_value_postSilicon= matching_rows['post_silicon_automation_release_completed'].iloc[0]
        #             corresponding_value = df2.loc[df2['id'] == int(articleid), 'automation_status'].iloc[0]
        #             corresponding_value_postSilicon=df2.loc[df2['id'] == int(articleid), 'post_silicon_automation_release_completed'].iloc[0]
        #             #print(f"For id{articleid} vlaue:{corresponding_value} postsilicon:{corresponding_value_postSilicon}")
        #             if corresponding_value == "In Production" and corresponding_value_postSilicon=="bios.birchstream_graniterapids-ap":
        #                 automatedIds.append(articleid)
        #     print("Length of Automated ids: ",len(automatedIds))
        #     if len(automatedIds) > 0:
        #         df1.at[index, 'Test cases Info'] = f'Test cases Info_{len(automatedIds)}'
        #     else:
        #         df1.at[index, 'Test cases Info'] = "No Automated Test Case Found"

        #     print("df1")
        #     print(df1)
   
    else:

        print("we are here")
        automatedExcelPath= os.path.join(current_directory,'database',folder_name,'automated.xlsx') 
        if os.path.exists(automatedExcelPath):
            return pd.read_excel(automatedExcelPath)
        AutoDictAssign={}
        df1=pd.read_excel(os.path.join(current_directory,'database',folder_name,'mapping.xlsx'))
        df2=pd.read_csv(os.path.join(current_directory,'database',folder_name,f"{query_id}.csv"))
        GNRdf=pd.read_excel(live_hw_sheet_path)
        automatedIds=[]
        df1['Platform Type']=""
        for index, row in df1.iterrows():
            articleid = row['id']
            allHostNames=str(row['All Host Names']).split(', ')
           
            import sys
            MinAssignvalue=sys.maxsize
            MinAssignPlatform=""
            for hostName in allHostNames:
                print("Hostname: ",hostName)
                status=""
                if "baifwi" in hostName:
                    status= GNRdf.loc[GNRdf['Host Name'] == hostName, 'Platform Status'].iloc[0]
                    print("HostName: ",status)
                if status!="Automated":
                    continue    
                if hostName not in AutoDictAssign:
                    AutoDictAssign[hostName]=1
                    MinAssignPlatform=hostName
                    break
                elif AutoDictAssign[hostName] < MinAssignvalue:
                    AutoDictAssign[hostName]+=1
                    MinAssignPlatform=hostName
            print("MinAssignPlatform: ",MinAssignPlatform)
            if MinAssignPlatform:
                BMCIP = GNRdf.loc[GNRdf['Host Name'] == hostName, 'BMC IP'].iloc[0]
                PlatformID = GNRdf.loc[GNRdf['Host Name'] == hostName, 'Platform ID'].iloc[0]
                df1.loc[df1['id'] == row['id'], 'Host Name'] =  MinAssignPlatform
                df1.loc[df1['id'] == row['id'], 'BMC_IP'] =  BMCIP
                df1.loc[df1['id'] == row['id'], 'Platform Ids'] =  PlatformID
                df1.loc[df1['id'] == row['id'], 'Platform Type'] =  "Automated"
            else:
                df1.loc[df1['id'] == row['id'], 'Platform Type'] =  "Manual"



            corresponding_value = df2.loc[df2['id'] == articleid, 'automation_status'].iloc[0]
            corresponding_value_postSilicon=df2.loc[df2['id'] == articleid, 'post_silicon_automation_release_completed'].iloc[0]
            if corresponding_value == "In Production"  and corresponding_value_postSilicon=="bios.birchstream_graniterapids-ap":
                automatedIds.append("In Production")
            else:
                automatedIds.append("Not Automatable")         
        df1['Automation Status'] = automatedIds     
        automatedExcelPath= os.path.join(current_directory,'database',folder_name,'automated.xlsx') 
        df1.to_excel(automatedExcelPath,index=False)   
        print("df1 Automation Status added")
        print(df1)
        return df1
    print("we are in show Automated function")
    print("outside Automation Status added")
    print(df1)
    return df1


@web.route('/AutomatedStatus')
def AutomatedStatus():
    folder_name = request.args.get('arg1')
   
    jsonPath=os.path.join(os.getcwd(),'pcmd_app','json_data','AutomatedData.json')

    with open(jsonPath, 'r') as file:
    
        jsonData = json.load(file)


   


    # Iterate through the keys and values of the outer object
    for key_outer, value_outer in jsonData.items():
        print("Key (Outer):", key_outer)
        
        # Iterate through the keys and values of the inner object
        for key_inner, value_inner in value_outer.items():
            print("   Key (Inner):", key_inner)
            print("   Value (Inner):", value_inner)

    return render_template('AutomatedStatus.html',jsonData=jsonData)

def trigger(ArtifactoryLink,Emails,Host_Name,ArticleIds):
    
        # import subprocess

    pass    
    # batch_file_path = "C:\\PCMD\\pcmd_app\\test.bat"
    # print("trying to call")
    # subprocess.call([batch_file_path])

      
        #subprocess.Popen(["python", "C:\\Users\\ahora\\Desktop\\Selenium\\trigger.py"],shell=True)
    # s=Service(ChromeDriverManager().install())
        
    # driver= webdriver.Edge(service=s)
    # driver.get("https://www.google.com/")
    # time.sleep(2)

    #automater.start(ArtifactoryLink,Emails,Host_Name,ArticleIds)
@web.route('/submitAutomated',methods=['GET','POST'])
def submitAutomated():
    requestData = request.json  # Get the JSON data from the request
    ArtifactoryLink = requestData.get('inputData1')  # Extract inputData1
    Emails = requestData.get('inputData2')  # Extract inputData2
    selectedRows = requestData.get('inputData3')
    print("selected: ",selectedRows)
    folder_name= requestData.get('inputData4')
    query_id =requestData.get('inputData5')
    radio_options =requestData.get('inputData6')
    
    print("radio_options: ",radio_options)
    current_datetime = datetime.now()
    articleIds=""
    dict1={}
    if radio_options=="option2":
        print('inside option2')
        mapping_df=pd.read_excel(os.path.join(current_directory,'database',folder_name,"rautomated.xlsx"))
        mapping_df.reset_index(drop=True, inplace=True)
        
        for i in selectedRows:
            # Access 'Test Case / Article Ids' column at specified row index using .iloc[]
            value_at_index = mapping_df.iloc[int(i)]['Test Case / Article Ids']
            print('value at index option2: ',value_at_index)
            # Append value to articleIds
            testcases=value_at_index.split(', ')
            df2=pd.read_csv(os.path.join(current_directory,'database',folder_name,f'{query_id}.csv'))


            articleIds=[]
            print("before len(articles: ) ",len(articleIds))
            for articleid in testcases:
                print("Looing for id: ",articleid)
                print("Query id: ",query_id)
                corresponding_value = df2.loc[df2['id'] == int(articleid), 'automation_status'].iloc[0]
                corresponding_value_postSilicon=df2.loc[df2['id'] == int(articleid), 'post_silicon_automation_release_completed'].iloc[0]
                
                if corresponding_value == "In Production"  and "bios.birchstream_graniterapids-ap" in str(corresponding_value_postSilicon):
                    
                    articleIds.append(articleid)
            print("after  len(articles: ) ",len(articleIds))
            articleIds=', '.join(articleIds)

            # if articleIds=="":
            #     articleIds = str(value_at_index)
            # else:
            #     articleIds=articleIds+", "+ str(value_at_index)
            Host_name=mapping_df.iloc[int(i)]['Host Name']
            dict1[Host_name]= articleIds
        
    else:
        print('inside option1')
        mapping_df=pd.read_excel(os.path.join(current_directory,'database',folder_name,"Automated.xlsx"))
        mapping_df.reset_index(drop=True, inplace=True)
        articleIds=[]
        for i in selectedRows:
            # Access 'Test Case / Article Ids' column at specified row index using .iloc[]
            value_at_index = mapping_df.iloc[int(i)]['id']
            # Append value to articleIds
            print('value at index option1: ',value_at_index)
            articleIds.append(str(value_at_index))
            #articleIds += str(value_at_index)
            Host_name=mapping_df.iloc[int(i)]['Host Name']
            if Host_name not in dict1:
                dict1[Host_name]=str(mapping_df.iloc[int(i)]['id'])
            else:
                dict1[Host_name]=dict1[Host_name]+", "+str(mapping_df.iloc[int(i)]['id'])
        
        articleIds=', '.join(articleIds)
    #Format the date and time in a user-friendly format
    formatted_datetime = current_datetime.strftime("%A, %d %B %Y %H:%M:%S")
    print('radio option: ',radio_options)
    print('dict1: ',dict1)
    jsonPath=os.path.join(os.getcwd(),'pcmd_app','json_data','AutomatedData.json')
    if os.path.exists(jsonPath):
        print("already exist")
    
        #-----adding new test Plan-------------------------
        with open(jsonPath, 'r') as file:
            AutomatedDict = json.load(file)

        last_test_plan=""
        i=1
        prevkey=""
        for key,value in AutomatedDict.items():
                print("key : ",key)  
                if prevkey=="" or prevkey!=key:
                    i=1
                nextTestPlanName=f"Test Plan {i}"
                prevkey=key
                for nextTestPlanName,val in value.items():
                    for key1,value1 in AutomatedDict[key][nextTestPlanName]['Tcd Config details'].items():
                            
                            ids=value1['Test Case / Article Ids']
                            status=value1['Trigger status']
                        
                          
                            ids=ids.split(', ')
                            i+=1
                            
                            for id1 in ids:
                                if(str(id1) in articleIds and status=="stored"):
                                    print("id1 : ",id1)
                                    print("id  : ",id)
                                    return jsonify({'message': 'Test Plan failed.'})
            
                    last_test_plan=nextTestPlanName

        nextTestPlanNo=last_test_plan.split(' ')[2]
        nextTestPlanName=f"Test Plan {int(nextTestPlanNo)+1}"
        print("nextTestPlanName: ",nextTestPlanName)
        if query_id not in AutomatedDict:
            AutomatedDict[query_id]={}
            nextTestPlanName=f"Test Plan 1"
        AutomatedDict[query_id][nextTestPlanName]={}
        AutomatedDict[query_id][nextTestPlanName]['Auto Trigger Inputs']={}
        AutomatedDict[query_id][nextTestPlanName]['Tcd Config details']={}
        
        AutomatedDict[query_id][nextTestPlanName]['Auto Trigger Inputs']['Artifactory Link']=ArtifactoryLink
        AutomatedDict[query_id][nextTestPlanName]['Auto Trigger Inputs']['Email List']=Emails
        AutomatedDict[query_id][nextTestPlanName]['Auto Trigger Inputs']['Time & Date']=formatted_datetime
        
        for Host_name,articleIds in dict1.items():
            AutomatedDict[query_id][nextTestPlanName]['Tcd Config details'][Host_name]={}
            AutomatedDict[query_id][nextTestPlanName]['Tcd Config details'][Host_name]['Test Case / Article Ids']=articleIds
            AutomatedDict[query_id][nextTestPlanName]['Tcd Config details'][Host_name]['Trigger status']="stored"
        # automation_thread = Thread(target=trigger,args=(ArtifactoryLink, Emails, Host_name, articleIds))
        # automation_thread.start()

        trigger(ArtifactoryLink,Emails,Host_name,articleIds)
    else:
        
        AutomatedDict={}
        AutomatedDict[query_id]={}
        AutomatedDict[query_id]['Test Plan 1']={}
        AutomatedDict[query_id]['Test Plan 1']['Auto Trigger Inputs']={}
        AutomatedDict[query_id]['Test Plan 1']['Tcd Config details']={}
        AutomatedDict[query_id]['Test Plan 1']['Auto Trigger Inputs']['Time & Date']=formatted_datetime
        
        AutomatedDict[query_id]['Test Plan 1']['Auto Trigger Inputs']['Artifactory Link']=ArtifactoryLink
        AutomatedDict[query_id]['Test Plan 1']['Auto Trigger Inputs']['Email List']=Emails
        
        for Host_name,articleIds in dict1.items():
            AutomatedDict[query_id]['Test Plan 1']['Tcd Config details'][Host_name]={}
            AutomatedDict[query_id]['Test Plan 1']['Tcd Config details'][Host_name]['Test Case / Article Ids']=articleIds
            AutomatedDict[query_id]['Test Plan 1']['Tcd Config details'][Host_name]['Trigger status']="stored"
        
        # automation_thread = Thread(target=trigger,args=(ArtifactoryLink, Emails, Host_name, articleIds))
        # automation_thread.start()
        trigger(ArtifactoryLink,Emails,Host_name,articleIds)
    print("Autoamted Dict: ",AutomatedDict)
    with open(jsonPath, 'w') as f:
        json.dump(AutomatedDict, f)

   

    
    return jsonify({'message': 'Data received successfully'})

@web.route('/pcmd_dashboard',methods=['GET','POST'])
@login_required
def pcmd_dashboard():
    form = request.form
    if request.method == 'POST':
        radio_options = request.form.get('radio_options') 
        radio_options1 = request.form.get('radio_options1')
        status = request.form.get('manual')

        query_id=""
        article_id=""

        try:
            query_id=request.form["queryIds"] 
        except:
            print("Query Id not found")

        try:
            article_id=request.form["articleId"] 
        except:
            print("Article Id not found")
    
        keyword=""   
        try : 
            keyword=request.form["keyword"] 
        except:
            print("Keyword not found") 
        
        if(query_id=="" and article_id=="" and keyword.strip()==""):
            flash('Please provide input..!!','info')
            return redirect(url_for('web.home'))
        
        TestCaseType=""
        try:
            TestCaseType =request.form["TestCaseType"]
        except:
            print("No selected data found")

        excecutable_test_cases=0
        total_test_cases=0
        if(keyword.strip()!="" and TestCaseType.strip()!=""):
            folder_name=request.form["folder_name"]
           
            if(radio_options=="option2" and TestCaseType=="Automated"):
                automateddf=ShowAutomatedData(radio_options,folder_name,query_id)
                excecutable_test_cases = len(automateddf[automateddf['Test cases Info'] != 'No Automated Test Case Found'])
                total_test_cases=automateddf.shape[0]
                df=automateddf
            elif(radio_options=="option1" and (TestCaseType=="Manual" or TestCaseType=="Automated")):
                automateddf=ShowAutomatedData(radio_options,folder_name,query_id)
                excecutable_test_cases = len(automateddf[automateddf['Automation Status'] == 'In Production'])
                total_test_cases=automateddf.shape[0]
                df=automateddf
            
            print(f" Inside query and aksing for automated")
            
            if TestCaseType=="Manual":
                if(radio_options=="option2"):
                    relative_path = os.path.join(os.getcwd(),'database', folder_name, 'rmapping.xlsx')
                    df=pd.read_excel(relative_path)
                    df = df[df['Platform Status'] == "Manual"]  
                
                else:
                    relative_path = os.path.join(os.getcwd(),'database', folder_name, 'mapping.xlsx')
                    df=pd.read_excel(relative_path)
                    df = df[df['Platform Status'] == "Manual"]  
                total_test_cases=df.shape[0]
                rmapping_df=pd.read_excel(os.path.join(os.getcwd(),'database',folder_name,'rmapping.xlsx'))
                excecutable_test_cases=0
                for index,row in rmapping_df.iterrows():
                    if((rmapping_df.shape[0]-1)!=index):
                        excecutable_test_cases=excecutable_test_cases+int((row['Test cases Info'].split('_'))[1])     
            if( TestCaseType=="All"):
            
           
                if(radio_options=="option2"):
                    relative_path = os.path.join(os.getcwd(),'database', folder_name, 'rmapping.xlsx')
                    df=pd.read_excel(relative_path)
                
                else:
                    relative_path = os.path.join(os.getcwd(),'database', folder_name, 'mapping.xlsx')
                    df=pd.read_excel(relative_path)
                total_test_cases=pd.read_excel(relative_path).shape[0]
                rmapping_df=pd.read_excel(os.path.join(os.getcwd(),'database',folder_name,'rmapping.xlsx'))
                excecutable_test_cases=0
                for index,row in rmapping_df.iterrows():
                    if((rmapping_df.shape[0]-1)!=index):
                        excecutable_test_cases=excecutable_test_cases+int((row['Test cases Info'].split('_'))[1])
            return render_template('pcmd_form2.html',columns=df.columns,df=df,non_reserved_data=df,Folder_name=folder_name,radio_options=radio_options,query_id=query_id,excecutable_test_cases=excecutable_test_cases,total_test_cases=total_test_cases,TestCaseType=TestCaseType)

           

        if(keyword.strip()!=""):
            folder_name=request.form["folder_name"]
            if(radio_options=="option2"):
                relative_path = os.path.join('database', folder_name, 'rmapping.xlsx')
            else:
                relative_path = os.path.join('database', folder_name, 'mapping.xlsx')
            total_test_cases=pd.read_excel(os.path.join(current_directory,'database',folder_name,'mapping.xlsx')).shape[0]
            rmapping_df=pd.read_excel(os.path.join(current_directory,'database',folder_name,'rmapping.xlsx'))
            excecutable_test_cases=0
            for index,row in rmapping_df.iterrows():
                if((rmapping_df.shape[0]-1)!=index):
                    excecutable_test_cases=excecutable_test_cases+int((row['Test cases Info'].split('_'))[1])
        
        
            excel_file_path = os.path.join(current_directory, relative_path)    
           
            df = pd.read_excel(excel_file_path)
            empty_frame=pd.DataFrame()
            return render_template('pcmd_form2.html',columns=df.columns,df=df,non_reserved_data=df,Folder_name=folder_name,radio_options=radio_options,query_id=query_id,excecutable_test_cases=excecutable_test_cases,total_test_cases=total_test_cases,TestCaseType=TestCaseType)


        if(query_id.strip()!=""):
            start_time=datetime.now()
            global dict1
            dict1={}
            #function to download data(.csv) ancd create basic mapping file
            folder_name =createFolder()

            # Fetching the hw from hsdes
            check_data(query_id,folder_name)


            non_executable_ids=UpdateMappingSheet(folder_name)
          
            option=0
            if(radio_options=="option2"):
               

                print("went to option2")
                change_mapping(folder_name,non_executable_ids)
                

                option=1
            
                # ConvertingToJson(folder_name)
                Converting_json(folder_name,option)
            
                total_test_cases=pd.read_excel(os.path.join(current_directory,'database',folder_name,'mapping.xlsx')).shape[0]
                rmapping_df=pd.read_excel(os.path.join(current_directory,'database',folder_name,'rmapping.xlsx'))
                excecutable_test_cases=0
                for index,row in rmapping_df.iterrows():
                    if((rmapping_df.shape[0]-1)!=index):
                        excecutable_test_cases=excecutable_test_cases+int((row['Test cases Info'].split('_'))[1])

                print("ratio : ",excecutable_test_cases,"/",total_test_cases)    
                relative_path = os.path.join('database', folder_name, 'mapping.json')
                json_path = os.path.join(current_directory, relative_path)
              
                with open(json_path,'r') as f:
                    supported_article_ids = json.load(f)

                relative_path = os.path.join('database', folder_name, 'rmapping.xlsx')
                excel_file_path = os.path.join(current_directory, relative_path)    
              
                df = pd.read_excel(excel_file_path)
                empty_frame=pd.DataFrame()
                end_time=datetime.now()
                print("Time taken for query id: ",end_time-start_time)
                #option2- config to tcd
                #option1 -tcd to config
                return render_template('pcmd_form2.html',columns=df.columns,df=df,non_reserved_data=df,supported_article_ids=supported_article_ids,Folder_name=folder_name,empty_frame=empty_frame,empty_columns=empty_frame.columns,radio_options=radio_options,query_id=query_id,total_test_cases=total_test_cases,excecutable_test_cases=excecutable_test_cases,TestCaseType=TestCaseType)
                
            
        
        elif(article_id.strip()!=""):
            non_reserved_data=fetchHwConfigArticleId(article_id)
         
        
            if  not non_reserved_data.empty:
                
                #flash('Successfully Updated.{}'.format(article_id),'success')
            
                df=pd.DataFrame(non_reserved_data)
                print("No of rows in df==  ",df.shape[0])
                table_html = df.to_html(classes='table table-striped', index=False)
        
                return render_template('pcmd_form1.html',columns=df.columns, df=df,non_reserved_data=table_html,article_id=article_id)
            else:
                print(non_reserved_data)
                flash('Not Found Any matching hw Config Data for.{}'.format(article_id),'danger')
        
    elif form.errors and len(form.errors)>0:
        for error in form.errors:
            for error_desc in form.errors[error]:
                flash(error_desc,'danger')
    flash('Please provide input..!!','info')            
    return redirect(url_for('web.home'))

@web.route('/updateBMCIPStatus',methods=['GET','POST'])
def updateBMCIPStatus():
    print("Inside updateBMCIPStatus")
    
    BMCIPpath=os.path.join(current_directory,'database','GNR.xlsx')
    print('BMCIPpath: ',BMCIPpath)
    BMCIPdf=pd.read_excel(BMCIPpath)
    result_dict = {}

    def is_pingable(ip):
        """Checks if an IP address is reachable using a single ping with a 1-second timeout."""
        param = '-n' if os.name == 'nt' else '-c'  # Use appropriate parameter for Windows vs. Unix-like systems
        command = ['ping', param, '1', '-w', '1', ip]  # Set 1-second timeout
        try:
            response = subprocess.run(command, stdout=subprocess.PIPE, timeout=2)  # Allow 2 seconds for completion
            return response.returncode == 0
        except subprocess.TimeoutExpired:
            return False  # Timeout occurred
        
    
    def login_with_timeout(ip):
        login_host = ip
        try:
            # Initialize the redfish client
            REDFISH_OBJ = redfish.redfish_client(
                base_url=login_host,
                username="root1",
                password="0penBmc1",
                default_prefix='/redfish/v1/',
                timeout=1
            )

            # Login to the service
            REDFISH_OBJ.login(auth="session")

            # Make the request
            System_response = REDFISH_OBJ.get("/redfish/v1/Systems")
            result_dict[login_host] = "success" if System_response else "Auth failed"
            

        except Exception as e:
            result_dict[login_host] = "Auth failed"
            print(f"Error processing {login_host}: {e}")

   

    working_ips_status=[]
    list1=BMCIPdf['BMC IP'].tolist()
    print(list1)
    # Replace with the IP you want to check
    for ip_address in list1:
        if(ip_address):
            if is_pingable(str(ip_address).strip()):
                #print(f"{ip_address} is reachable")
                working_ips_status.append("Reachable")
            else:
                working_ips_status.append("Not Reachable")
                # print(f"{ip_address} is not reachable")

   
    # BMCIPdf['BMC IP']=[elem for elem in list1 if elem]
    BMCIPdf['BMC IP Status']=working_ips_status
    working_ips = BMCIPdf[BMCIPdf['BMC IP Status'] == 'Reachable']['BMC IP'].tolist()
    print("Working IPssss:", working_ips)

    start_time = datetime.now()

    # Use ThreadPoolExecutor to parallelize the requests
    with ThreadPoolExecutor() as executor:
        executor.map(login_with_timeout, working_ips)

    end_time = datetime.now()

    print("Result time taken:", end_time - start_time)
    print(result_dict)

    for index, row in BMCIPdf.iterrows():
        ip = row['BMC IP']
        # Get the status from result_dict, default to 'Not Reachable' if not found
        status = result_dict.get(ip, 'Not Reachable')
        # Assign the status to the 'BMC IP Status' column
        BMCIPdf.at[index, 'BMC IP Status'] = status
    # Auth_status = [result_dict.get(ip, 'Not Reachable') for ip in BMCIPdf['BMC IP']]
    # BMCIPdf['BMC IP Status']=Auth_status
    print("Ip dataframe")
    print(BMCIPdf)
    BMCIPdf.to_excel(BMCIPpath,index=False,sheet_name='Sheet2')

    flash('BMC IP Status Updated', 'success')
    return redirect(url_for('web.updateSheet'))
    
from flask import send_file
@app.route('/download')
def download_file():
    current_directory = os.getcwd()  # Get the current working directory
    excel_file_path = os.path.join(current_directory, 'database', 'GNR.xlsx')  # Generate the file path
    return send_file(excel_file_path, as_attachment=True)


@app.route('/process_selected_checkboxes',methods=['POST'])
def process_selected_checkboxes():
    selected_rows = request.form.getlist('selected_rows[]')
   
    # Retrieve other form data if needed
    artifactory_link = request.form.get('artifactory_link')
    email_address = request.form.get('email_address')
    option=request.form.get('radio_options')
    query_id=request.form.get('queryIds')
    print("option selected: ",option)
    # Process other form data
    print("Selected rows:", selected_rows)
    print("artifactory_link:", artifactory_link)
    print("email_address:", email_address)
    # Add your processing logic here
    if(option=="option2" and len(selected_rows)==0):
        
        df1=pd.read_excel(os.path.join(current_directory,'database','folder_20240312_100213','mapping.xlsx'))
        df2=pd.read_csv(os.path.join(current_directory,'database','folder_20240312_100213',f'{query_id}.csv'))

        exdict = {}
        print("process_selected_checkboxes")
        for index, row in df1.iterrows():
            articleid = row['id']
            corresponding_value = df2.loc[df2['id'] == articleid, 'automation_status'].iloc[0]
            corresponding_value_postSilicon=df2.loc[df2['id'] == articleid, 'post_silicon_automation_release_completed'].iloc[0]
            if corresponding_value == "In Production"  and corresponding_value_postSilicon=="bios.birchstream_graniterapids-ap":
                host_name = row['Host Name']
                
                # Create a dictionary for the host name if it doesn't exist
                if host_name not in exdict:
                    exdict[host_name] = {'Test Cases': '', 'Test Cases Info': 'Test_case_Count 0'}
                
                # Get the previous string and count
                previous_string = exdict[host_name].get('Test Cases', '')
                test_cases_count = exdict[host_name].get('Test Cases Info', 'Test_case_Count 0')
                
                # Update the test cases count
                count = int(test_cases_count.split(' ')[1]) + 1
                test_cases_count = f"Test_case_Count {count}"
                
                # Append the new test case to the previous string
                new_string = str(articleid)  # You need to define new_string
                combined_string = ', '.join(filter(None, [previous_string, new_string]))
            
                # Update the dictionary with the combined string and count
                exdict[host_name]['Test Cases'] = combined_string
                exdict[host_name]['Test Cases Info'] = test_cases_count

        dff = pd.DataFrame.from_dict(exdict, orient='index')
        dff.reset_index(inplace=True)
        dff.rename(columns={'index': 'Platform Ids'}, inplace=True)
        return render_template('executableTestcases.html',df=dff,columns=dff.columns,option=option)

    elif(len(selected_rows)==0):
        df1=pd.read_excel(os.path.join(current_directory,'database','folder_20240312_100213','mapping.xlsx'))
        df2=pd.read_csv(os.path.join(current_directory,'database','folder_20240312_100213','16023370788.csv'))
    
        exdict={}
        for index,row in df1.iterrows():
            articleid=row['id']
        
            corresponding_value = df2.loc[df2['id'] == articleid, 'automation_status'].iloc[0]
            if(corresponding_value=="In Production"):
                exdict[articleid]={}
                exdict[articleid]['title']=row['title']
                exdict[articleid]['platforms']=row['Host Name']
        
        dff = pd.DataFrame.from_dict(exdict, orient='index')
        dff.reset_index(inplace=True)
        dff.rename(columns={'index': 'id'}, inplace=True)

   
        return render_template('executableTestcases.html',df=dff,columns=dff.columns,option=option)

        

    return redirect(url_for('web.TestCaseExecution'))
   

@app.route('/update', methods=['POST'])
def update():
    # Receive relevant data from the form
    cell_data = request.form.to_dict()
    num_keys = len(cell_data)

    df = pd.read_excel(master_sheet_path) 
    columns_name = [col.strip() for col in df.columns]

    rows=int(num_keys/len(columns_name))
    
    df1=pd.DataFrame(columns=columns_name)
    col_dict = {}
    for column_name in columns_name:
        col_dict[column_name] = ""
    
    I=0
    rows1 = [col_dict.copy() for i in range(rows)]
    df1 = pd.DataFrame(rows1)
    try:
        for cell_id, value in cell_data.items():
            split_result = cell_id.split('_', 1)
            row, col = split_result
            try:
                int_row = int(row)
                df1.at[int(int_row),col]=value
            except:
                continue
    except Exception as e:          
        print("Error:", e)

    os.remove(master_sheet_path)
    df1.to_excel(master_sheet_path, index=False, sheet_name="Sheet2")
    return redirect(url_for('web.updateSheet'))

@web.route('/updateSheet', methods=['GET', 'POST'])
@login_required
def updateSheet():
    df = pd.read_excel(master_sheet_path)
    return render_template('updateMaster.html', df=df)

@app.route('/get_blue_query')
def get_blue_query():
    # print("inside blue qeuery== ")
    blue_query_json_path=os.path.join(os.getcwd(),"pcmd_app","json_data","query.json")
    with open(blue_query_json_path, 'r') as file:
        data = json.load(file)
    # print("blue data== ",data)
    return data
@app.route('/get_data_cofig_tcs/<selected_id>')
def get_data_cofig_tcs(selected_id):
    selected_ids=selected_id.split(',')
    print("selected ids== ",selected_ids)
    folder_name=selected_ids[0]
    dict={}
    if len(selected_ids) > 1 and '.' in str(selected_ids[1]):
       selected_ids= selected_ids[1:]
    elif len(selected_ids) > 1:
        
        values_to_find = selected_ids[1:]
        df=pd.read_excel(os.path.join(current_directory,'database',folder_name,'mapping.xlsx'))
        # Find the corresponding values from column2 based on values from column1
        selected_ids=[]
       
        for index,row in df.iterrows():
            if str(row['id']) in values_to_find:
                temp=str(row['BMC_IP'])
                print("temp: ",temp)
                selected_ids.append(temp)
                print("id is present congrats")
        
        
        print("selectedids== ",selected_ids)
        GNR_data=pd.read_excel(live_hw_sheet_path)
        GNR_data=GNR_data[GNR_data['BMC IP'].isin(selected_ids)]
    
        print("columns== ",GNR_data.columns)
        return GNR_data.to_json()



    dict={}
   
    mapping_sheet=os.path.join(current_directory,'database',folder_name,'rmapping.xlsx')
    mp_df=pd.read_excel(mapping_sheet)
   
    for i in range(len(selected_ids)):
        filtered_df = mp_df[mp_df['BMC IP'] == selected_ids[i]]
        if not filtered_df.empty:
            selected_value = filtered_df.iloc[0]['Test Case / Article Ids']
            selected_values=str(selected_value) .split(', ')
            print("Selected values:", selected_values)
            dict[selected_ids[i]]=selected_values
        else:
            print("No rows match the condition for selected_id:", selected_ids[i])

            #print('ip = ',ip," selected_values ",selected_values)
  
    GNR_data=pd.read_excel(live_hw_sheet_path)
   
    GNR_data=GNR_data[GNR_data['BMC IP'].isin(selected_ids)]
   
    GNR_data.insert(0,'Test Case /Article Ids','')
 
    for key, value in dict.items():
        
        GNR_data.loc[GNR_data['BMC IP'] == key, 'Test Case /Article Ids'] = ", ".join(value)
    test_case_ids = GNR_data.pop('Test Case /Article Ids')
    GNR_data.insert(0, 'Test Case /Article Ids', test_case_ids)
  
    
    # print("columns== ",GNR_data.columns)
    return GNR_data.to_json()


@web.route('/show_hw',methods=['GET','POST'])
@login_required
def show_hw():
    wanted_path = get_latest_path(os.path.join(os.getcwd(),"database","Latest_Hardware_Data"))
    print("Wanted path", wanted_path)
    #excel_file_path = live_hw_sheet_path 
    excel_file_path = os.path.join(wanted_path, "GNR.xlsx") 
    print("exce_file_path==",excel_file_path)
    df=pd.read_excel(excel_file_path,engine="openpyxl") 
    selected_project = request.form.get('selected_project')
    print("selected Project: ",selected_project)
    # for columns,row in df.iterrows():
    #     print(row['BMC IP'])
    #     print(row['Bios Version'])
    #     if(str(row['Bios Version'])=='nan'):
    #         print("Empty")
    table_html = df.to_html(classes='table table-striped', index=False)
    return render_template('show_hw.html',columns=df.columns, df=df,non_reserved_data=table_html,selected_project=selected_project,wanted_path=wanted_path)


@web.route('/')
@login_required
def home():
   
    
    count1=0
    all_projects = None
    staled = False

    all_projects =  get_all_projects()
    all_projects.sort(key=lambda tup:tup[-1])

    all_users_tuple = get_all_saved_users()
    all_users = user_list_to_dictionary(all_users_tuple)
    increase_hits(request.remote_addr)
  
    with open(app_constants.SUPPORTED_PROJECTS_FILE,"r")as f:
        supported_projects = json.load(f)    
    # print("supported_projects= ",supported_projects)    
    with open(app_constants.REPO_STATS_FILE,"r")as f:
        repo_stats = json.load(f)
    return render_template('new_home.html',all_projects=all_projects,all_users = all_users,is_admin = current_user.is_admin,is_home=True,statistics_data = get_statistics(),repo_stats=repo_stats,supported_projects=supported_projects)


@web.route('/TestCaseExecution',methods=['GET','POST'])
def TestCaseExecution():
    print("Inside TestcaseExecution")
    df1=pd.read_excel(os.path.join(current_directory,'database','folder_20240312_100213','mapping.xlsx'))
    df2=pd.read_csv(os.path.join(current_directory,'database','folder_20240312_100213','16023370788.csv'))

    exdict = {}

    for index, row in df1.iterrows():
        articleid = row['id']
        corresponding_value = df2.loc[df2['id'] == articleid, 'automation_status'].iloc[0]
        corresponding_value_postSilicon=df2.loc[df2['id'] == articleid, 'post_silicon_automation_release_completed'].iloc[0]
        if "bios.birchstream_graniterapids-ap" in corresponding_value_postSilicon.split(','):
            host_name = row['Host Name']
            
            # Create a dictionary for the host name if it doesn't exist
            if host_name not in exdict:
                exdict[host_name] = {'Test Cases': '', 'Test Cases Info': 'Test_case_Count 0'}
            
            # Get the previous string and count
            previous_string = exdict[host_name].get('Test Cases', '')
            test_cases_count = exdict[host_name].get('Test Cases Info', 'Test_case_Count 0')
            
            # Update the test cases count
            count = int(test_cases_count.split(' ')[1]) + 1
            test_cases_count = f"Test_case_Count {count}"
            
            # Append the new test case to the previous string
            new_string = str(articleid)  # You need to define new_string
            combined_string = ', '.join(filter(None, [previous_string, new_string]))
        
            # Update the dictionary with the combined string and count
            exdict[host_name]['Test Cases'] = combined_string
            exdict[host_name]['Test Cases Info'] = test_cases_count

    dff = pd.DataFrame.from_dict(exdict, orient='index')
    dff.reset_index(inplace=True)
    dff.rename(columns={'index': 'Platform Ids'}, inplace=True)

   
    return render_template('executableTestcases.html',df=dff,columns=dff.columns,option="option2")


@web.route('/add_project',methods=['GET','POST'])
@login_required
def new_project():
    if not current_user.is_admin:
        flash("You shouldn't be here...","warning")
        return redirect(url_for('web.home'))
    form = NewProject(request.form)
    if request.method == 'POST' and form.validate():
        fields_list = clean_rec_project_data(request.form)
        status = insert_new_project(fields_list)
        if status:
            return redirect(url_for('web.home'))
        else:
            flash("Error occured while saving new project... Please try again or contact admin...","warning")
    return render_template('add_project.html',form=form)




@web.route('/profile_img/<filename>')
@login_required
def get_user_profile_image(filename='user.png'):
    return send_from_directory(app.config["UPLOAD_PROFILE_IMAGE_FOLDER"], filename)

@web.route('/profile')
@login_required
def profile():
    if request.method=='GET':
        all_projects =  get_all_projects()
        all_projects.sort(key=lambda tup:tup[-1])
        user_projects = []
        if current_user.is_admin:
            user_projects = all_projects
        else:
            for project in all_projects:
                if project[1] ==  current_user.email:
                    user_projects.append(project)
        return render_template('profile.html',user_projects = user_projects,form = NewProject(request.form))
    else:
        pass

@web.route('/edit_project',methods=['POST'])
@login_required
def edit_project():
    form = NewProject(request.form)
    if request.method == 'POST' and form.validate():
        fields_list = clean_rec_project_data(request.form)
        fields_list.append(request.form["id"])
        status = update_project(fields_list)
        if status:
            flash('Successfully Updated.','success')
        else:
            flash('Error while updating details. Please try again or contact admin...','danger')
    elif form.errors and len(form.errors)>0:
        for error in form.errors:
            for error_desc in form.errors[error]:
                flash(error_desc,'danger')
    return redirect(url_for('web.profile'))

@web.route('/update_repo',methods=['POST'])
@login_required
def ajax_update_repo():
    
    #return redfish_bmc_usage_v2.start()
    #Nirmal EDIT
    return updater.start()
    
@web.route('/get_time_to_update')
@login_required 
def get_time_to_update():
    excel_file_path = os.path.join(os.getcwd(), 'database', 'GNR.xlsx')
    #return jsonify({"size":pd.read_excel( os.path.join(os.getcwd(),'database','GNR.xlsx')).shape[0]})
    try:
        df = pd.read_excel(excel_file_path, engine='openpyxl')
        file_size = df.shape[0] if not df.empty else 0
        return jsonify({"size": file_size})
    except Exception as e:
        return jsonify({"error": str(e)})
