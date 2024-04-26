import streamlit as st
import pandas as pd
from collections import defaultdict
from bs4 import BeautifulSoup
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
import datetime
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder


handler = HsdesApiHandler(r"C:\Users\tkawale\AppData\Local\Programs\Python\Python311\Lib\site-packages\certifi\cacert.pem")  # Instantiate the HsdesApiHandler class

os.environ["HTTPS_PROXY"] = "http://child-prc.intel.com:913"
os.environ["HTTP_PROXY"] = "http://child-prc.intel.com:913"

# Load user credentials from CSV file
@st.cache_data
def load_user_credentials():
    return pd.read_csv("users_security_tokens.csv")

# Login check function
def check_login(user_id, token):
    credentials = load_user_credentials()
    user_record = credentials.loc[credentials['UserID'] == user_id]
    if not user_record.empty and user_record.iloc[0]['SecurityToken'] == token:
        return True
    else:
        return False

def is_query_or_article_valid(query, type = "query"):
    pattern=r"^\d+$"
    return bool(re.match(pattern,query))

def update_reservation_state():
    st.session_state["reserve_screen"] = "True"
    return

def reset():
    st.session_state["reserve_screen"] = "False"


# Function to identify HW requirements
def identify_hw_requirement(article_id_to_find, data, data1, data2):
    if article_id_to_find == 0:
        st.info("Please enter a valid Test Case ID!")
        return

    title = ""
    filtered_df = data1[data1["test_case_definition.id"] == article_id_to_find]
    if not filtered_df.empty:
        corresponding_title = filtered_df["title"].iloc[0]
        title = corresponding_title
        st.write(f"Title for Article ID {article_id_to_find}: {corresponding_title}")
    else:
        st.write(f"No matching record found for Article ID {article_id_to_find}")

    keywords = title.split('_')
    keys = [keyword for keyword in keywords if ' ' not in keyword]
    for key in keys:
        mask = data.apply(lambda row: row.astype(str).str.contains(key, case=False, na=False).any(), axis=1)
        if mask.any():
            data = data[mask]
    
    filtered_df = data2[data2["Article Id"] == article_id_to_find]
    HW_requirement = filtered_df["config HW Mapping(hsdes)"].iloc[0]
    keys = HW_requirement.split(' ')
    hw = data.columns
    finalkeys = [key for key in keys for hw1 in hw if hw1.find(key) != -1]

    for key in finalkeys:
        mask = data.apply(lambda row: row.astype(str).str.contains(key, case=False, na=False).any(), axis=1)
        if mask.any():
            data = data[mask]

    # After identifying the HW requirement, filter the dataframe to show only non-reserved items
    if 'Reserved' in data.columns:
        non_reserved_data = data[data['Reserved'] == False]
    else:
        st.error("The 'Reserved' column is not present in the dataset.")
        return

    st.dataframe(non_reserved_data)
        
    reserve_btn = st.sidebar.button("Reserve", on_click=update_reservation_state)

def reserve_hardware_in_db(platform_id_to_reserve, user_id):
    try:
        # Load the GNR.xlsx file
        gnr_data = pd.read_excel("GNR.xlsx", engine="openpyxl")
        # Find the row with the matching Platform ID
        row_to_update = gnr_data.loc[gnr_data['Platform ID'] == platform_id_to_reserve]
        
        if not row_to_update.empty:
            # Update the 'Reserved', 'ReservedBy', and 'Date' columns
            gnr_data.loc[row_to_update.index, 'Reserved'] = True
            gnr_data.loc[row_to_update.index, 'ReservedBy'] = user_id
            gnr_data.loc[row_to_update.index, 'Date'] = datetime.datetime.now().strftime("%Y-%m-%d")

            # Save the updated DataFrame back to the GNR.xlsx file
            gnr_data.to_excel("GNR.xlsx", index=False, engine="openpyxl")

            # Update session state with the success message
            st.session_state['reservation_made'] = True
            st.markdown(f"Successfully reserved **{platform_id_to_reserve}**")
            return True
        else:
            st.write("Platform ID not found.")
            return False
    except FileNotFoundError as fnf_error:
        st.write(f"File not found: {fnf_error}")
        return False
    except Exception as e:
        st.write(f"An error occurred: {e}")
        return False

# Define your reserve_platform function here
def reserve_platform():
    st.title("Reserve platform")
    st.markdown("Please enter the ID of the platform you wish to reserve.")

    with st.form(key="reserve_platform_form"):
        platform_id = st.text_input("Platform ID", "")
        submit = st.form_submit_button("Reserve")

    if submit:
        st.session_state["reserve_screen"] = "True"
        if platform_id:
            reserve_status = reserve_hardware_in_db(platform_id, st.session_state["user_id"])
            if reserve_status:
                st.session_state['platform_reserved'] = True
                st.session_state['platform_id'] = platform_id
                st.success(f"Platform {platform_id} reserved successfully.")
                home = st.button("Home", on_click=reset)
        else:
            st.error("Please enter a valid Platform ID.")

def user_input():
    with st.sidebar.form(key="form_page", clear_on_submit=False):
        st.sidebar.header('Enter article ID or query ID as needed')
        query_id = st.text_input("Enter the Query ID (Optional)", placeholder="Query Id")
        article_id = st.text_input("Enter the Article ID (Optional)", placeholder="Article Id")
        program_name = st.text_input("Enter the Program Name", placeholder="Program Name")
        
        query_input_valid = is_query_or_article_valid(query_id, "query") if query_id else True
        article_input_valid = is_query_or_article_valid(article_id, "article") if article_id else True
        
        # Check that only one of either query_id or article_id is entered
        if query_id and article_id:
            st.error("Please enter only a Query ID or an Article ID, not both.")
            return None

        submit_button = st.form_submit_button(label="Submit")
        
        if submit_button:
            if (query_id or article_id) and (query_input_valid and article_input_valid):
                st.sidebar.success(f"Data submitted!")
                return query_id, article_id, program_name
            else:
                st.error("Invalid input. Please enter digits only for Query ID or Article ID, and ensure only one is entered.")
                return None


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
    dict1={}
    base_url="https://hsdes-api.intel.com/rest/article/"
    pattern1=r"(H.W|hw|HW).*?(<*?<\/.*>)"
    pattern2='((H.W|HW|hw).*?)(?:(SW|S.W|sw))'
    
    for index in range(len(df.index)):              
        article_id=df.iat[index,0]
        st.write(f"Processing article id : {article_id} and index: {index}")
        dict1[str(article_id)]=[]
        url=base_url + str(article_id)   
        data=handler.get_article_data(url)['data']
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
    

def main_app():
    """ if "reserve_screen" in st.session_state and st.session_state["reserve_screen"] == "True":
        st.session_state["reserve_screen"] = "False" """
    
    st.title('FIV Project Mgmt. Dashboard')
    st.markdown(f"Welcome, **{st.session_state['user_id']}**!")
    footer_update.footer()

    user_inputs = user_input()  # Collect user input
    # If user_input() returns None, stop processing further
    if user_inputs is None:
        st.warning("Please enter valid input to proceed.")
        return  # Exit the function early

    query_id, article_id, program_name = user_inputs  # Unpack the returned tuple

    # Handle case when Query ID is provided
    if query_id:
        df = extract_data(query_id)
        if df is not None:
            st.subheader(f"Test cases for the given query id :{query_id}")
            st.write('Data Dimension: ' + str(df.shape[0]) + ' rows and ' + str(df.shape[1]) + ' columns.')
            st.dataframe(df) 
            fetch_hw_req(df)
    
    # Handle case when Article ID is provided
    if article_id:
        # Load the required data files for hardware requirements
        data = pd.read_excel("GNR.xlsx", engine="openpyxl", header=0)
        data1 = pd.read_excel("DF.xlsx", engine="openpyxl", header=0)
        data2 = pd.read_excel("mapping.xlsx", engine="openpyxl", header=0)

        # Call the new function to identify HW requirement
        identify_hw_requirement(int(article_id), data, data1, data2)

    # If neither Query ID nor Article ID is provided, display a message
    if not query_id and not article_id:
        st.info("Please enter either a Query ID or an Article ID to proceed.")
   

# User login screen
def login_screen():
    st.sidebar.header("User Login")  # Set the sidebar header to "User Login"
    user_id = st.sidebar.text_input("User ID", "")
    token = st.sidebar.text_input("Token", "")
    if st.sidebar.button("Login"):
        if check_login(user_id, token):
            st.session_state['logged_in'] = True  # Set session state to logged in
            st.session_state['user_id'] = user_id # Set session state with user ID
            st.rerun()  # Rerun the app to update the view
        else:
            st.sidebar.error("Invalid user ID or token.")

# Check if already logged in, otherwise show login

if "reserve_screen" not in st.session_state:
    st.session_state["reserve_screen"] = "False"

if 'reserve_screen' in st.session_state and st.session_state['reserve_screen']=="True":
    reserve_platform()
elif 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    login_screen()
else:
    main_app()
