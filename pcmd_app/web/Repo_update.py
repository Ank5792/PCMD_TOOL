
from datetime import datetime 
import json
import shutil
import pcmd_app.web.app_constants as app_constants
import pcmd_app.web.temp  as redfish_bmc_usage
from concurrent.futures import ThreadPoolExecutor 
from datetime import datetime
import redfish
import subprocess
import os
import pandas as pd

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email import encoders

live_hw_sheet_path=os.path.join(os.getcwd(),'database','GNR.xlsx')
master_sheet=os.path.join(app_constants.DATABASE_PATH,'Master_Sheet','master_sheet.xlsx')
live_hw_sheet_path=""

def mail():
  
    strFrom='tejas.kawale@intel.com'
 
    # file = open("C:\\Knobdiff\\recipients.txt","r+")
    recipients="tejas.kawale@intel.com"
    cc = "tejas.kawale@intel.com,ankita.hora@intel.com"
    #prakash.arumugam@intel.com,vinay1.kumar@intel.com,nirmal.sonal@intel.com,gauri.verma@intel.com
    # c = cc.read()
    # strTo=recipients
    # strCC=c
    # print("c== ",c)
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = "PCMD Tool Platform Status"
    msgRoot['From'] = strFrom
    
    msgRoot['To']=recipients
    msgRoot['Cc']=cc
    # for i in cc:
    #     msgRoot['Cc']+=i
    msgRoot.preamble = 'This is a multi-part message in MIME format.'

    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)
    df=pd.read_excel(live_hw_sheet_path, engine='openpyxl')
    columnNames=["BMC IP","Host Name","BMC IP Status"]
    df=df[columnNames]
    html_content = df.to_html()
    msgText = MIMEText(
                f'Hi all,\nFollowing table show the platform status of all the available platforms of PCMD TOOL.\nBelow is the Platform Status Table:\n{df}\n Thanks,\nPCMD Team'
            
                )
    msgAlternative.attach(msgText)
   

    smtp = smtplib.SMTP('smtpauth.intel.com', 587)
    smtp.starttls()
    smtp.login("tejas.kawale@intel.com","Prati@937")
    print("recipients: ",recipients)
    print("cc: ",cc)
    smtp.sendmail(strFrom, recipients.split(",") + cc.split(","), msgRoot.as_string())
    smtp.quit()
    print('Email sent')

def update_data(update_details_list, update_path):
    print("update_details_list== ",update_details_list)

    if(update_details_list=="DimmDetails"):
        print("DimmDetails here")
        redfish_bmc_usage.readBMCIP(update_path)
    elif(update_details_list=="BiosVersionDetails"):
        print("BiosVersionDetails here")
       
    elif(update_details_list=="PCIeDetails here"):    
        print("PCIeDetails")

def file_handler():

    data = pd.read_excel(os.path.join(app_constants.DATABASE_PATH, "Master_Sheet", "master_sheet.xlsx"), engine='openpyxl')
    excel_column_names = data.columns.tolist()
    columns_required = ["HW ID","Site","Platform ID","Project Name","Host Name","BMC IP","BMC IP Status","Platform Status","QDF","Bios Version","Si Qty",
                        "DIMM Freq","DIMM Size/Capacity (Gb)","DIMM Rank/W","DIMM Manufacturer/Vendor","DIMM Type","DIMM Qty","DIMM Location","PCIe_Speed",
                        "PCIe_Card_Details","CXL_Card","Storage_Device","PCIe_Location","IFWI flashing Tool","Debug Tools","OS Configured","KVM",
                        "PDU/Power Splitter","Usage","Reserved","ReservedBy	Time","Date","Execution team"]
    all_columns = excel_column_names + [col for col in columns_required if col not in excel_column_names]

    
    updated_DF = pd.DataFrame(columns=all_columns)
    updated_DF[excel_column_names] = data[excel_column_names]
    updated_DF["BMC IP Status"] = "Unknown Failure"

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    folder_name = f"{timestamp}"
    hw_data_path = os.path.join(app_constants.DATABASE_PATH,"Latest_Hardware_Data",folder_name)
    if not os.path.exists(hw_data_path):
        os.makedirs(hw_data_path)
    final_hw_data_path = os.path.join(hw_data_path, "GNR.xlsx")

    updated_DF.to_excel(final_hw_data_path,index=False)
    return hw_data_path
     
def UpdateHwConfigdatabase():
    update_path = file_handler()
    
    # dimm_path=os.path.join(os.getcwd(),"pcmd_app","json_data","dimm_output.json")
    # bios_path=os.path.join(os.getcwd(),"pcmd_app","json_data","biosVersion_output.json")
    # cpu_path=os.path.join(os.getcwd(),"pcmd_app","json_data","cpu_output.json")
    # pcie_path=os.path.join(os.getcwd(),"pcmd_app","json_data","pcicxl_output.json")

    # if os.path.exists(dimm_path):
    #     os.remove(dimm_path)
    # if os.path.exists(bios_path):
    #     os.remove(bios_path)
    # if os.path.exists(cpu_path):
    #     os.remove(cpu_path)
    # if os.path.exists(pcie_path):
    #     os.remove(pcie_path)

    result_dict=redfish_bmc_usage.startTestingIps(update_path)  
    print("result dict repo_update",result_dict)
    start_time=datetime.now()
    update_details_list=["DimmDetails","BiosVersionDetails","PCIeDetails"]
    #update_details_list=["DimmDetails","BiosVersionDetails","PCIeDetails"]
    redfish_bmc_usage.readBios(update_path,result_dict)
    redfish_bmc_usage.readpci(update_path)
    with ThreadPoolExecutor () as executer:
        executer.map(update_data, update_details_list, update_path)
  
  
    
    redfish_bmc_usage.Updatesheet()
    mail()
    end_time=datetime.now()
    print("Total Time taken to Update:: ",end_time-start_time)
    

    print("database Upated")
def start():
    try:
        with open(app_constants.REPO_STATS_FILE,"r") as f:
            stat_data = json.load(f)
        time_diff=1
        try:
            last_modified_at = datetime.strptime(stat_data["last_refreshed_at"],"%a, %Y-%m-%d, %H:%M:%S")
            time_diff = (datetime.now() - last_modified_at).total_seconds()
        except:
            pass
        if time_diff<120:
            return {"error":"Last Refresh was only 2 minutes ago, please wait..."}
        
        #Logic to update database
        print("Starting update of the datasheet.")
        UpdateHwConfigdatabase()
        
        updated_at =datetime.now().strftime("%a, %Y-%m-%d, %H:%M:%S")
        stat_data.update({"last_refreshed_at":updated_at})
        with open(app_constants.REPO_STATS_FILE,"w") as f:
            json.dump(stat_data,f)
            
        return {"last_modified_at":updated_at}
    except Exception as e:
        print(e)
        return {"error":"Error Occured while refreshing. Please contact Team."}
    
# if __name__=='__main__':
#     start()
