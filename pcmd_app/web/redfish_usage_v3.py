import subprocess
import os
import pandas as pd
import redfish
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from datetime import datetime

# BMCIPpath=os.path.join(os.getcwd(),'database','BMC_IP.xlsx')
# print('BMCIPpath: ',BMCIPpath)
# BMCIPdf=pd.read_excel(BMCIPpath)
# print("BMC IP Df")
# print(BMCIPdf)
# result_dict = {}

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
        result_dict[login_host] = "success" if System_response else "failed"

    except Exception as e:
        result_dict[login_host] = "failed"
        print(f"Error processing {login_host}: {e}")



# working_ips_status=[]
# list1=BMCIPdf['BMC IP'].tolist()
# print(list1)
# # Replace with the IP you want to check
# for ip_address in list1:
#     if(ip_address):
#         if is_pingable(ip_address.strip()):
#             #print(f"{ip_address} is reachable")
#             working_ips_status.append("Reachable")
#         else:
#             working_ips_status.append("not Reachable")
#             # print(f"{ip_address} is not reachable")


# BMCIPdf['BMC IP']=[elem for elem in list1 if elem]
# BMCIPdf['BMC_Status']=working_ips_status
# working_ips = BMCIPdf[BMCIPdf['BMC_Status'] == 'Reachable']['BMC IP'].tolist()
# print("Working IPs:", working_ips)

# start_time = datetime.now()

# # Use ThreadPoolExecutor to parallelize the requests
# with ThreadPoolExecutor(max_workers=150) as executor:
#     executor.map(login_with_timeout, working_ips)

# end_time = datetime.now()

# print("Result time taken:", end_time - start_time)
# print(result_dict)


# Auth_status = [result_dict.get(ip, 'Not Found') for ip in BMCIPdf['BMC IP']]
# BMCIPdf['BMC_Login']=Auth_status
# print("Ip dataframe")
# print(BMCIPdf)
# BMCIPdf.to_excel("status.xlsx",index=False)


def ping_bmc_ip(ip):
    """Checks if an IP address is reachable using a single ping with a 1-second timeout."""
    param = '-n' if os.name == 'nt' else '-c'  # Use appropriate parameter for Windows vs. Unix-like systems
    command = ['ping', param, '1', '-w', '1', ip]  # Set 1-second timeout
    try:
        response = subprocess.run(command, stdout=subprocess.PIPE, timeout=2)  # Allow 2 seconds for completion
        return True
    except subprocess.TimeoutExpired:
        return False  # Timeout occurred
    

def authenticate(host_IP):
    try:
        # Initialize the redfish client
        REDFISH_OBJ = redfish.redfish_client(
            base_url=host_IP,
            username="root1",
            password="0penBmc1",
            default_prefix='/redfish/v1/',
            timeout=1
        )

        # Login to the service
        REDFISH_OBJ.login(auth="session")

        # Make the request
        System_response = REDFISH_OBJ.get("/redfish/v1/Systems")
        if System_response:
            return True
        else:
            return False
    except Exception as e:
        return False


def start_updates():
    # delete this file path later
    master_sheet_path = r"C:\\PCMD\\database\\Master_Sheet\\master_sheet.xlsx"
    data = pd.read_excel(master_sheet_path)
    excel_column_names = data.columns.tolist()

    columns_required = ["HW ID","Site","Platform ID","Project Name","Host Name","BMC IP","BMC IP Status","Platform Status","QDF","Bios Version","Si Qty",
                        "DIMM Freq","DIMM Size/Capacity (Gb)","DIMM Rank/W","DIMM Manufacturer/Vendor","DIMM Type","DIMM Qty","DIMM Location","PCIe_Speed",
                        "PCIe_Card_Details","CXL_Card","Storage_Device","PCIe_Location","IFWI flashing Tool","Debug Tools","OS Configured","KVM",
                        "PDU/Power Splitter","Usage","Reserved","ReservedBy	Time","Date","Execution team"]
    all_columns = excel_column_names + [col for col in columns_required if col not in excel_column_names]

    
    updated_DF = pd.DataFrame(columns=all_columns)
    updated_DF[excel_column_names] = data[excel_column_names]
    updated_DF["BMC IP Status"] = "Unknown Failure"
    for index, row in updated_DF.iterrows():
        try:
            if ping_bmc_ip(row["BMC IP"]):
                print("pingable")
                updated_DF.at[index, "BMC IP Status"] = "Pingable"
                if authenticate("https://"+str(row["BMC IP"])):
                    print("authentic")
                    updated_DF.at[index, "BMC IP Status"] = "Authentication Successful"
                else:
                    print("not authentic")
            else:
                print("not ping")
        except:
            print("mottttttttttttt")
            continue
    print(updated_DF)

#start_updates()