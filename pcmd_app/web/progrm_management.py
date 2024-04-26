import streamlit as st
import pandas as pd
import base64
import re
from hsdes_api_handler import HsdesApiHandler
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit.components.v1 as components
import footer_update
import re


st.title('FIV Project Mgmt. Dashboard')

st.markdown("""
This app performs extraction of HW required for all the respective test cases present under test case
definition or test plan!!
* **Python libraries:** base64,pandas,streamlit
* **Data source:** [hsdes database source ](https://hsdes.intel.com/appstore/community/#/1504412278?queryId=15011919807).
            """)

footer_update.footer()

st.sidebar.header('User Input Features')
handler = HsdesApiHandler(r"C:\Users\ahora\AppData\Local\Programs\Python\Python311\Lib\site-packages\certifi\cacert.pem")  # Instantiate the HsdesApiHandler class

os.environ["HTTPS_PROXY"] = "http://child-prc.intel.com:913"
os.environ["HTTP_PROXY"] = "http://child-prc.intel.com:913"

def is_query_valid(query):
    pattern=r"^\d+$"
    return bool(re.match(pattern,query))

def user_input():
    with st.sidebar.form(key="form_page",clear_on_submit=True):
        query_id=st.text_input("Enter the queryid",placeholder="Query Id")
        input_valid=is_query_valid(query_id)
        submit_button=st.form_submit_button(label="Submit")
        if submit_button:
            if input_valid:
                st.sidebar.success(f"Data submitted! You entered: {query_id}")
                return query_id
            else:
                st.error("Invalid input. Please enter digits only.")



def extract_data(query_id):
    st.write(query_id)    
    filename = f"{query_id}.csv"
    if os.path.exists(filename):
        df = pd.read_csv(filename)
    else:
        data = handler.run_query_by_id(query_id)['data']
        df = pd.DataFrame(data)
        df.to_csv(filename,index=False) 
        #df['cleaned_description'] = df['description'].apply(handler.remove_html_tags)
        #df['combined_description_title'] = df['title'].astype(str) + df['cleaned_description'].astype(str)
        #df.to_csv(filename, index=False)
    return df


def fetch_hw_req(df):
    count=0
    dict1={}
    base_url="https://hsdes-api.intel.com/rest/article/"
    pattern1=r"(H.W|hw|HW).*?(<*?<\/.*>)"
    pattern2='((H.W|HW|hw).*?)(?:(SW|S.W|sw))'
    
    for index in range(len(df.index)):
        count=count+1
        if(count==6):
            break              
        article_id=df.iat[index,0]
        st.write(f"Processing article id : {article_id} and index: {index}")
        dict1[str(article_id)]=[]
        url=base_url + str(article_id)   
        data=handler.get_article_data(url)['data']
        tag=data[0]["tag"]
        if(tag is not None):
            dict1[str(article_id)].append(tag.split(","))
        else:

            str1=data[0]["central_firmware.test_case_definition.pre_condition"]
            str2=data[0]["description"]
            str3=data[0]["test_case_definition.test_steps"]
            str1=re.sub('\s+',' ',str1)
            str2=re.sub('\s+',' ',str2)
            str3=re.sub('\s+',' ',str3)
                
            
            
            if re.findall(pattern2,str1) and len(handler.remove_html_tags((re.findall(pattern2,str1))[0][0]))>5:
                dict1[str(article_id)].append(handler.remove_html_tags((re.findall(pattern2,str1))[0][0]))
                
            elif re.findall(pattern1,str1):
                dict1[str(article_id)].append(handler.remove_html_tags((re.findall(pattern1,str1))[0][1]))

            elif re.findall(pattern2,str2) and len(handler.remove_html_tags((re.findall(pattern2,str2))[0][0]))>5:
                dict1[str(article_id)].append(handler.remove_html_tags((re.findall(pattern2,str2))[0][0]))  

            elif re.findall(pattern1,str2):
                dict1[str(article_id)].append(handler.remove_html_tags((re.findall(pattern1,str2))[0][1]))

            elif re.findall(pattern2,str3) and len(handler.remove_html_tags((re.findall(pattern2,str3))[0][0]))>5:
                dict1[str(article_id)].append(handler.remove_html_tags((re.findall(pattern2,str3))[0][0]))  
            elif re.findall(pattern1,str3):
                dict1[str(article_id)].append(handler.remove_html_tags((re.findall(pattern1,str3))[0][1]))

            if not dict1[str(article_id)]:
                dict1[str(article_id)].append("HW required: None")        


    
    #st.write(dict1)
    df1=pd.DataFrame(dict1)
    df1=df1.T
    df1.reset_index(inplace=True)
    df1.index=np.arange(1,len(df1)+1)
    df1.columns=["article_id","HW reqd"]
    st.write(df1)

    #st.write(f"pre_condition data :{str1}")
    #st.write(f"description data :{str2}")
    #st.write(f"test_steps data :{str3}")    
    

def check_data():
    
    query_id=user_input()
    if(query_id):
        df=extract_data(query_id)         
        st.subheader(f"Test cases for the given query id :{query_id}")
        st.write('Data Dimension: ' + str(df.shape[0]) + ' rows and ' + str(df.shape[1]) + ' columns.')
        st.dataframe(df) 
        fetch_hw_req(df)
                           
           

    else:
        pass


check_data()
        







            

            
            

