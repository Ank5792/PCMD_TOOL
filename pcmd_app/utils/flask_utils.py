from ldap3 import Connection, Server
from cryptography.hazmat.primitives.asymmetric import rsa,padding
from cryptography.hazmat.primitives import serialization,hashes
from cryptography.hazmat.backends import default_backend
from pcmd_app import app
from base64 import b64decode
import json
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
import os
from datetime import datetime

def rsa_decrypt(rec_pass):
    rsa_key = RSA.import_key(app.config["RSA_PRIV"])
    cipher = PKCS1_v1_5.new(rsa_key)
    aes_key = cipher.decrypt(b64decode(rec_pass),None)
    return aes_key.decode()

def check_empty_field(field):
    if field in ["","na","None",None]:
        return " "
    return field

def try_login(email, password):     
    c = Connection(Server(host="ldaps://corpadssl.intel.com", port=3269), user=email, password=password, raise_exceptions=True,auto_bind=True)
    c.unbind()

def user_list_to_dictionary(user_list):
    user_dic = {}
    for user_tuple in user_list:
        user_dic[user_tuple[0]] = [user_tuple[1],user_tuple[2]]
    return user_dic

def clean_rec_project_data(rec_dic):
    owner = rec_dic['owner']
    short_description = rec_dic['short_description']
    description = rec_dic['description']
    tool_name  = rec_dic['tool_name']
    current_status   = rec_dic['current_status']
    working_links  = rec_dic['working_links']
    jira_link = check_empty_field(rec_dic['jira_link'])
    ags_link  = check_empty_field(rec_dic['ags_link'])
    wiki_link  = check_empty_field(rec_dic['wiki_link'])
    current_devs = rec_dic['current_devs']
    working_links = working_links.split(';')
    working_links = [i.strip() for i in working_links]
    current_devs = current_devs.split(';')
    current_devs = [i.strip() for i in current_devs]
    fields_list = [owner,short_description,description,current_status,' ',wiki_link,jira_link,ags_link,working_links,current_devs,tool_name]
    return fields_list


def get_statistics():
    user_data=None
    with open(app.config["STATISTICS_JSON"],'r') as f:
        user_data = json.load(f)
    return user_data


def increase_hits(new_add):
    with open(app.config["STATISTICS_JSON"],'r') as f:
        user_data = json.load(f)

    with open(app.config["DAILY_IP_TEXTS"],"r") as f:
        data=f.read()
    if len(data)<1 or new_add not in data:
        data=data+";"+str(new_add)
        user_data.update({"today_unique_hits":user_data['today_unique_hits']+1})
        with open(app.config["DAILY_IP_TEXTS"],'w') as f:
            f.write(data)

    user_data.update({"total_hits":user_data['total_hits']+1})
    user_data.update({"today_hits":user_data['today_hits']+1})
    
    with open(app.config["STATISTICS_JSON"],"w") as f:
        json.dump(user_data,f)

def get_latest_path(folder_path):
    folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    folders.sort(key=lambda x: datetime.strptime(x, "%Y%m%d%H%M%S"), reverse=True)

    file_name = "GNR.xlsx"

    for folder in folders:
        path = os.path.join(folder_path, folder)
        files_list = []
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path):
                files_list.append(file)
        if file_name in files_list:
            return path