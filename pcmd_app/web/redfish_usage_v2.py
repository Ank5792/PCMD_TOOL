
from datetime import datetime
# import pcmd_app.web.app_constants as app_constants
# import pcmd_app.web.redfish_usage  as redfish_bmc_usage
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

import pandas as pd
import redfish
import os
# import psycopg2
# import jsonify
import subprocess
#import configparser
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
# from functools import partial
os.environ["HTTPS_PROXY"] = "http://child-prc.intel.com:913"
os.environ["HTTP_PROXY"] = "http://child-prc.intel.com:913"
# dict_dimm={}
# dict_pci={}
# dict_cpu={}
# dict_bios={} 

master_sheet_path = os.path.join(os.getcwd(), 'database', 'Master_Sheet', 'master_sheet.xlsx')
update_folder = os.path.join(os.getcwd(), 'database', 'Latest_Hardware_Data')

# def getDimmData(login_host):
#     if(result_dict[login_host]=="failed"): return
#     # Create a Redfish object
#     print("logiHost= ",login_host)
#     REDFISH_OBJ = redfish.redfish_client(base_url=login_host, username="root1", password="0penBmc1", default_prefix='/redfish/v1/')

#     # Login to the service
#     REDFISH_OBJ.login(auth="session")

#     DIMM_response = REDFISH_OBJ.get("/redfish/v1/Systems/system/Memory")
#     CPU_response = REDFISH_OBJ.get("/redfish/v1/Systems/system/Processors")

#     memory_data = pd.json_normalize(DIMM_response.dict)
#     cpu_data = pd.json_normalize(CPU_response.dict)

#     displaydata=["Location.PartLocation.ServiceLabel","Manufacturer","BaseModuleType","MemoryDeviceType","RankCount","CapacityMiB","OperatingSpeedMhz","MemoryType","SerialNumber","PartNumber","Status.State"]
#     member_count=int(memory_data['Members@odata.count'][0])
#     cpu_count = int(cpu_data['Members@odata.count'][0])
#     print(member_count,type(member_count))
#     print("member_count== ",member_count)
#     print("cpu count== ",cpu_count)
    
#     # Iterate through the DIMM info and collect the data
#     dimm_data = []
#     CPU_data = []
#     df_list = []
#     CPU_data_list = []

#     dimm_members = memory_data["Members"]
#     cpu_members = cpu_data["Members"]
#     for i in range(member_count):
#         dimm_id = f"/redfish/v1/Systems/system/Memory/dimm"
#         dimm_url = dimm_members[0][i]['@odata.id']
#         dimm_data.append({'ID': dimm_id, 'URL': dimm_url})
#         print(dimm_members[0][i],dimm_url )
#         DIMM_response = REDFISH_OBJ.get(dimm_url)

        
#         df = pd.json_normalize(DIMM_response.dict)  
#         df_list.append(df)
#     result_dimm_df = pd.concat(df_list, ignore_index=True)
  
#     for i in range(cpu_count):
#         cpu_id = f"/redfish/v1/Systems/system/Memory/dimm",i
#         cpu_url = cpu_members[0][i]['@odata.id']
#         CPU_data.append({'ID': cpu_id, 'URL': cpu_url})
#         # print(cpu_members[0][i],cpu_url )
#         cpu_response = REDFISH_OBJ.get(cpu_url)

        
#         cpu_df = pd.json_normalize(cpu_response.dict)
#         CPU_data_list.append(cpu_df)

        

#     result_cpu_df = pd.concat(CPU_data_list, ignore_index=True)
#     print("result_cpu_df\n")
#     print(result_cpu_df)
#     CPU_display_data = ["Socket","Model","MaxSpeedMHz","Version","TotalCores","TotalThreads","ProcessorId.Step","Status.State"]
#     try :
#         print(result_cpu_df[CPU_display_data])
#         print(result_dimm_df)
#     except:
#         print("data not found")   
#         # return result_dimm_df,result_cpu_df
   
#     Json_dimm_data=result_dimm_df.to_json(orient="records")
#     dict_dimm[login_host]=json.loads(Json_dimm_data)
#     try:
#         #Json_cpu_data=result_cpu_df[CPU_display_data].to_json(orient="records")
#         Json_cpu_data=result_cpu_df.to_json(orient="records")
#         dict_cpu[login_host]=json.loads(Json_cpu_data)
#     except:
#         print("Did not found the cpu data")

# def readBMCIP():
#         excel_file_path = 'C:\FEAST\pcmd_db\GNR.xlsx'
#         df=pd.read_excel(excel_file_path,sheet_name='Sheet2')
          
#         BMC_Ip_list=df['BMC IP'].to_list()
#         print("BMC IP List=== ",BMC_Ip_list )
#         start_time=datetime.now()
#         try:
#             with ThreadPoolExecutor(max_workers=200) as executer:
#                 executer.map(getDimmData,BMC_Ip_list)
            
#             end_time=datetime.now()    
#             print("finished Dimm and cpu details in seconds",end_time-start_time)
#         except Exception as e:
#             print("Data Error as : ",e)
      
#         json_file_path_dimm = 'C:/FEAST/feast_app/json_data/dimm_output.json'
#         json_file_path_cpu = 'C:/FEAST/feast_app/json_data/cpu_output.json'

#         # Open the file in write mode and use json.dump() to write the dictionary to the file
#         with open(json_file_path_dimm, 'w') as json_file:
#             json.dump(dict_dimm, json_file)
#         with open(json_file_path_cpu, 'w') as json_file:
#             json.dump(dict_cpu, json_file)
                
#         # excel_file_path = 'C:\FEAST\pcmd_db\GNR.xlsx'
#         # df=pd.read_excel(excel_file_path,sheet_name='Sheet2')
#         # # login_host="10.190.255.236"
#         # login_account="root1"
#         # login_password="0penBmc1"
       
#         # # excel_file_path='C:\FEAST\pcmd_db\GNR.xlsx'
#         # # sheet_name="Sheet1"
#         # # df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
#         # column_name="BMC IP"
#         # dict_dimm={}
#         # dict_cpu={}
       
#         # if column_name in df.columns:
#         #     # Iterate over the values in the specified column
#         #     try:
#         #         for value in df[column_name]:
#         #             print(value)
                    
                    
                        
#         #             try:
#         #                 dimm_dataframe,cpu_dataframe=getDimmData(str(value),login_account,login_password)
#         #                 json_data_dimm = dimm_dataframe.to_json(orient='records', default_handler=str)
#         #                 dict_dimm[value]= json.loads(json_data_dimm)
#         #                 if not cpu_dataframe.empty:
#         #                     json_data_cpu = cpu_dataframe.to_json(orient='records', default_handler=str)
#         #                     dict_cpu[value]=json.loads(json_data_cpu)
#         #             except:
#         #                 print("Didn't find data for ip = ",value)
                    
                   
#         #     except Exception as e:
#         #         print("pass = ",value)                    
               
#         #     json_file_path_dimm = 'C:/FEAST/feast_app/json_data/dimm_output.json'
#         #     json_file_path_cpu = 'C:/FEAST/feast_app/json_data/cpu_output.json'

#         #     # Open the file in write mode and use json.dump() to write the dictionary to the file
#         #     with open(json_file_path_dimm, 'w') as json_file:
#         #         json.dump(dict_dimm, json_file)
#         #     with open(json_file_path_cpu, 'w') as json_file:
#         #         json.dump(dict_cpu, json_file)
#         # else:
#         #     print(f"Column '{column_name}' not found in the DataFrame.")

# def readPCICXL(ip):
#     # Create a Redfish object
#     if(result_dict[ip]=="failed"): return
#     print("checking pci data for ip == ",ip)
#     login_host=ip
#     try:
#         REDFISH_OBJ = redfish.redfish_client(base_url=login_host, username="root1", password="0penBmc1", default_prefix='/redfish/v1/')

#         # Login to the service
#         REDFISH_OBJ.login(auth="session")
        
#         PCIe_response = REDFISH_OBJ.get("/redfish/v1/Systems/system/PCIeDevices")
#     except Exception as e:
#         print("IP==",ip,"Error: ",e)    
    
#     pcie_data=pd.json_normalize(PCIe_response.dict)

   
#     PCIedisplaydata=["@odata.id","Id","Manufacturer","PCIeInterface.PCIeType","Status.State"]
    
#     pcie_count= int(pcie_data['Members@odata.count'][0])
#     print("pcie_count= ",pcie_count)
 
    

#     PCIe_data=[]

#     PCIe_data_list = []

#     pcie_members=pcie_data["Members"]

#     for i in range(pcie_count):
       
      
        
#         pcie_url = pcie_members[0][i]['@odata.id']
        
#         PCIe_data.append({'ID': pcie_url, 'URL': pcie_url})
#         #print(pcie_members[0][i],pcie_url )
#         pcie_response = REDFISH_OBJ.get(pcie_url)

        
#         pcie_df = pd.json_normalize(pcie_response.dict)
#         PCIe_data_list.append(pcie_df)
#     result_df = pd.concat(PCIe_data_list, ignore_index=True)
   
#     check_list = ['Gen5','Gen4','Gen3','Gen2']
#     New_df = result_df[result_df['PCIeInterface.PCIeType'].isin(check_list)]

#     pcie_gen5_list=[]
#     pcie_list=[]
#     for value in New_df["@odata.id"]:
#         pcie_gen5_url=value+"/PCIeFunctions"
#         pcie_list.append({'ID': value, 'URL': pcie_gen5_url})
#         #print(pcie_members[0][i],pcie_gen5_url )
#         pcie_gen5_response = REDFISH_OBJ.get(pcie_gen5_url)
#         pcie_gen5_df = pd.json_normalize(pcie_gen5_response.dict)
#         pcie_gen5_list.append(pcie_gen5_df)
    
#     #print('pcie_gen5_list= ',pcie_gen5_list)  
#     result_df = pd.concat(pcie_gen5_list, ignore_index=True)
    
    
#     pcie_final_list=[]
#     count=result_df.shape[0]
   
#     i=0
#     for index, row in result_df.iterrows():    
#         value = row['@odata.id']    
#         pcie_final_url=value+"/"+str(i)
      
#         #print("pcie_final_url= ",pcie_final_url," index= ",index)
#         pcie_final_response = REDFISH_OBJ.get(pcie_final_url)
#         pcie_final_df = pd.json_normalize(pcie_final_response.dict)
#         pcie_final_list.append(pcie_final_df)
        
#     result_final_df = pd.concat(pcie_final_list, ignore_index=True)
#     Finaledisplaydata=["@odata.id","DeviceClass","DeviceId","VendorId","Name"]
   
#     merged_df = pd.concat([result_df, result_final_df[['DeviceClass', 'DeviceId']]], axis=1)
   
    
    
#     new_columns_df1 = result_final_df[['DeviceClass', 'DeviceId','VendorId']]
#     New_df.reset_index(drop=True, inplace=True)
#     # Concatenate df2 and the extracted columns from df1
#     concatenated_df = pd.concat([New_df[PCIedisplaydata], new_columns_df1], axis=1)
#     concatenated_df = concatenated_df[['@odata.id','Id','PCIeInterface.PCIeType','DeviceClass','Manufacturer','DeviceId','VendorId','Status.State']]
#     concatenated_df1=concatenated_df
    
    
#     check_list = ['MemoryController','NetworkController','MassStorageController']
#     concatenated_df = concatenated_df[concatenated_df['DeviceClass'].isin(check_list)]

   
#     # dict1={}
#     # dict1['0xa808']="Samsung_M.2_Device"
#     # dict1['0x01e0']="CXL-Astera_Leo_Type3"
#     # dict1['0xc001']="CXL-Montage_Type3"
#     # dict1['0x1021']="Mellanox_CX7_100GbE_2_port"
    
#     config=configparser.ConfigParser()
#     config_file_path="feast_app/config_data/config.ini"
#     config.read(config_file_path)
#     dict=config["dict1"]
#     # print("dict= ",dict)
#     # New column data
#     PCI_card_data = []
#     for value in concatenated_df['DeviceId']:
#         if value in dict:
#             PCI_card_data.append(str(dict[value]))
#         else:
#             PCI_card_data.append("None")
            
    
    
#     # Specify the position after which you want to insert the new column
#     insert_after_column = 'PCIeInterface.PCIeType'
    
#     # Find the index of the specified column
#     insert_after_index = concatenated_df.columns.get_loc(insert_after_column)
    
#     # Insert the new column after the specified column
#     concatenated_df.insert(insert_after_index + 1, 'PCI Card Name', PCI_card_data)
#     print('Master Data')
#     # print(concatenated_df)
   
   
#     json_data_cpu_pci = concatenated_df.to_json(orient='records', default_handler=str)
#     #dict_pci[ip]= json.loads(json_data_cpu_pci)
#     dict_pci[login_host]=json.loads(json_data_cpu_pci)
#     return json.loads(json_data_cpu_pci)
#     # json_file_path_pcicxl = 'C:/FEAST/feast_app/json_data/pcicxl_output.json'

#     # # Open the file in write mode and use json.dump() to write the dictionary to the file
#     # with open(json_file_path_pcicxl, 'w') as json_file:
#     #     json.dump(dict_pci, json_file)
    
# def send_rank(dimm_part_number,dimm_rank_number):
       
#     config=configparser.ConfigParser()
#     config_file_path="feast_app/config_data/config.ini"
#     config.read(config_file_path)
#     dict=config["dict2"]


#     final_list=[]
#     rank_list=set()
#     for vendor, card in dimm_part_number.items():
#         bits = dict[vendor].split(',')  # Corrected this line
#         rank = dimm_rank_number[vendor]
        
#         # rank_list = [str(element) + "Rx" for element in rank_list]
#         print("bits ", bits, " rank == ", rank,"card== ",card)
#         r = ""
#         for bit in bits:
#             print("r== ",r)
#             r = r + card[int(bit) - 1]
           
#         rank_list.add(f'{rank}Rx{r}')
#         print("rank list= ", rank_list)
#     return " ".join(rank_list)


# def updateSheetForBMCIP(ip):     
#     excel_file_path = 'C:\FEAST\pcmd_db\GNR.xlsx'  
#     df=pd.read_excel(excel_file_path,sheet_name='Sheet2')  
#     df.loc[df['BMC IP'] == ip, 'DIMM Location'] = "Dimm info"
#     json_file_path_cpu = "C:/FEAST/feast_app/json_data/cpu_output.json"
  
#     with open(json_file_path_cpu, 'r') as json_file:
#         json_data_cpu = json.load(json_file)
#     cpu_count=0
#     enabled_cpus=0
#     try:     
#         BMC_IP_data_cpu=json_data_cpu[ip]        
#         cpu_count=len(BMC_IP_data_cpu)
#         for i in range(cpu_count):
#             if str(BMC_IP_data_cpu[i]['Status.State'])=='Enabled':
#                 enabled_cpus=enabled_cpus+1
#     except:
#         print("No Cpu Details found")    
    
#     try :        
#         model=BMC_IP_data_cpu[0]['Model']
#     except:
#         model=""
#     print(cpu_count)
    
#     df.loc[df['BMC IP'] == ip, 'Si Qty'] = str(enabled_cpus)+"S"
#     df.loc[df['BMC IP'] == ip, 'QDF'] = str(model)
    
#     json_file_path_dimm = "C:/FEAST/feast_app/json_data/dimm_output.json"
  
#     with open(json_file_path_dimm, 'r') as json_file:
#         json_data_dimm = json.load(json_file)
#     BMC_IP_data_dimm=json_data_dimm[ip]
    
#     dimm_freq=set()
#     dimm_size=set()
#     dimm_rank=set()
    
   
#     dimm_vendor=set()
#     dimm_MD_type=set()
#     dimm_part_number={}
#     dimm_rank_number={}
#     dimm_qty=len(BMC_IP_data_dimm)
#     dimm_enabled=0
#     for i in range(dimm_qty):
#         if str(BMC_IP_data_dimm[i]['Status.State'])=='Enabled':
#             dimm_enabled=dimm_enabled+1
#             dimm_freq.add(BMC_IP_data_dimm[i]['OperatingSpeedMhz'])
#             dimm_size.add(BMC_IP_data_dimm[i]['CapacityMiB'])
#             dimm_rank.add(BMC_IP_data_dimm[i]['RankCount'])
#             dimm_vendor.add(BMC_IP_data_dimm[i]['Manufacturer'])
#             if BMC_IP_data_dimm[i]['Manufacturer'] not in dimm_part_number:
#                     dimm_part_number[BMC_IP_data_dimm[i]['Manufacturer']]=""
#             dimm_part_number[BMC_IP_data_dimm[i]['Manufacturer']]=BMC_IP_data_dimm[i]['PartNumber']
#             if BMC_IP_data_dimm[i]['Manufacturer'] not in dimm_rank_number:
#                 dimm_rank_number[BMC_IP_data_dimm[i]['Manufacturer']]=""
#             dimm_rank_number[BMC_IP_data_dimm[i]['Manufacturer']]=BMC_IP_data_dimm[i]['RankCount']
#             dimm_MD_type.add(BMC_IP_data_dimm[i]['MemoryDeviceType']+" "+BMC_IP_data_dimm[i]['BaseModuleType'])
        
#     print("dimm_part_number = ",dimm_part_number)
#     print("dimm_rank_number = ",dimm_rank_number)
#     dimm_size = {int(element // 1024) for element in dimm_size}   
     
#     modified_set = {str(item) + 'R' for item in dimm_rank}  
#     dimm_rank=modified_set  
#     dimm_freq_str = ' '.join(map(str, dimm_freq))
#     dimm_size = ' '.join(map(str, dimm_size))
#     dimm_rank =  send_rank(dimm_part_number,dimm_rank_number)
#     print("dimm_rank == ",dimm_rank)
#     dimm_vendor = ' '.join(map(str, dimm_vendor))
#     dimm_MD_type = ' '.join(map(str, dimm_MD_type))
#     dimm_freq_str+=" (Mhz)"  
#     # dimm_size+=" (Gb)" 
#     print("dimm_size== ",dimm_size)
    
#     df.loc[df['BMC IP'] == ip, 'DIMM Freq'] = dimm_freq_str
#     df.loc[df['BMC IP'] == ip, 'DIMM Size/Capacity (Gb)'] = dimm_size
#     df.loc[df['BMC IP'] == ip, 'DIMM Rank/W'] = dimm_rank
#     df.loc[df['BMC IP'] == ip, 'DIMM Manufacturer/Vendor'] = dimm_vendor
#     df.loc[df['BMC IP'] == ip, 'DIMM Type'] = dimm_MD_type
#     df.loc[df['BMC IP'] == ip, 'DIMM Qty'] = dimm_enabled
    
          
#     df.to_excel(excel_file_path,sheet_name='Sheet2',index=False,float_format='%.0f')
    
# def extract_string3(keyword, templates):
#     for template in templates:
#         if keyword.startswith(template):
#             return keyword[len(template):]
#     return None

# def updateSheetForPCI(ip):
#     excel_file_path = 'C:\FEAST\pcmd_db\GNR.xlsx'  
#     df=pd.read_excel(excel_file_path,sheet_name='Sheet2')  
#     json_file_path_pci = "C:/FEAST/feast_app/json_data/pcicxl_output.json"
  
#     with open(json_file_path_pci, 'r') as json_file:
#         json_data_pci = json.load(json_file)
        
#     BMC_IP_data_PCI=json_data_pci[ip]
    
#     pci_count=len(BMC_IP_data_PCI)
    
    
  
    
#     PCIeType=set()
#     PCI_Card_Name=set() 
    
#     PCIe_MassStorage=set()
#     PCIe_MemoryController=set()
#     PCIe_NetworkController=set()
    
#     for i in range(pci_count):
      
#         PCIeType.add(BMC_IP_data_PCI[i]['PCIeInterface.PCIeType'])
#         PCI_Card_Name.add(BMC_IP_data_PCI[i]['PCI Card Name'])
#         #Manufacturer.add(BMC_IP_data_PCI[i]['Manufacturer'])
#         if BMC_IP_data_PCI[i]['DeviceClass']=="MassStorageController":
#             PCIe_MassStorage.add(BMC_IP_data_PCI[i]['PCI Card Name'])
#         elif BMC_IP_data_PCI[i]['DeviceClass']=="MemoryController":
#             PCIe_MemoryController.add(BMC_IP_data_PCI[i]['PCI Card Name'])
#         elif BMC_IP_data_PCI[i]['DeviceClass']=="NetworkController":
#             PCIe_NetworkController.add(BMC_IP_data_PCI[i]['PCI Card Name'])
            
    
            
#     # templates=['CXL-']      
      
#     # PCI_Card_Name_final = [extract_string3(keyword, templates) for keyword in pci_card_Name1]      
   
                
#     PCIeType_str = ' '.join(map(str, PCIeType))
#     # PCI_Card_Name_str = ' '.join(map(str, PCI_Card_Name_final))
#     # Manufacturer_str = '\n'.join(map(str, Manufacturer))
#     PCIe_NetworkController_str='\n'.join(map(str, PCIe_NetworkController))
#     PCIe_MassStorage_str='\n'.join(map(str, PCIe_MassStorage))
#     PCIe_MemoryController_str='\n'.join(map(str, PCIe_MemoryController))
#     PCIE_Info="PCIe Info"
      
#     df.loc[df['BMC IP'] == ip, 'PCIe_Speed'] = PCIeType_str
#     df.loc[df['BMC IP'] == ip, 'PCIe_Card_Details'] = PCIe_NetworkController_str
#     df.loc[df['BMC IP'] == ip, 'CXL_Card'] = PCIe_MemoryController_str
#     # # df.loc[df['BMC IP'] == ip, 'CXL_Vendor'] = PCI_Card_Name_str
#     df.loc[df['BMC IP'] == ip, 'Storage_Device'] = PCIe_MassStorage_str
#     df.loc[df['BMC IP'] == ip, 'PCIe_Location'] = PCIE_Info

    
#     df.to_excel(excel_file_path,sheet_name='Sheet2',index=False)
    
#     # PCIe_Speed=set()
#     # PCIe_Vendor=set()
#     # CXL_Vendor			
#     # PCIe_Card Details
#     # CXL_Card
            
# def updateSheetForBiosVersion(ip):
#     excel_file_path = 'C:\FEAST\pcmd_db\GNR.xlsx'  
#     df=pd.read_excel(excel_file_path,sheet_name='Sheet2')  
#     json_file_path_bios = "C:/FEAST/feast_app/json_data/biosVersion_output.json"
  
#     with open(json_file_path_bios, 'r') as json_file:
#         json_data_bios = json.load(json_file)
#     try:
#         BMC_IP_data_bios=json_data_bios[ip]
#         df.loc[df['BMC IP'] == ip, 'Bios Version'] = BMC_IP_data_bios
#     except:
#         df.loc[df['BMC IP'] == ip, 'Bios Version'] = ""
#     print("update GNR ",df['Bios Version'])
#     os.remove(excel_file_path)
    
#     df.to_excel(excel_file_path,sheet_name='Sheet2',index=False)   
#     return df           


# def is_host_reachable(ip_address):
#     try:
#         # Run the ping command with a timeout of 2 seconds
#         subprocess.run(['ping', '-c', '1', '-W', '2', ip_address], check=True, stdout=subprocess.PIPE)
#         return True  # If the ping is successful, return True
#     except subprocess.CalledProcessError:
#         return False  #    
# def Updatesheet():
#     username='root1'
#     password='0penBmc1'

 
         
#     excel_file_path = 'C:\FEAST\pcmd_db\GNR.xlsx'  
#     df=pd.read_excel(excel_file_path,sheet_name='Sheet2') 
#     dict_pci={} 
#     print("result dict",result_dict)
#     column_name="BMC IP"
#     if column_name in df.columns:
#         for value in df[column_name]:
#                 print("For Ip: ",value," dict value: ",result_dict[value])
#             # if is_host_reachable(value):
#                 try :
#                     if(result_dict[value]=="success"):
#                         try:
#                             updateSheetForBMCIP(value)
#                             df.loc[df['BMC IP'] == value, 'BMC IP Status'] = "Success"
#                         except:
#                             print("Not Found Dimm data")
#                         try:
#                             updateSheetForPCI(value)
#                             df.loc[df['BMC IP'] == value, 'BMC IP Status'] = "Success"
#                         except:
#                             print("Not found PCIE data")
#                         try:
#                             updateSheetForBiosVersion(value)
#                             df.loc[df['BMC IP'] == value, 'BMC IP Status'] = "Success"
#                         except:
#                             print("Not found Bios Data")
#                     else:
#                        print("we are here")
                      
#                 except Exception as e:
#                     print("No data for : ",e)
#             # else :
#             #     print("Not reachable== ",value)  
           
#     else:
#             print(f"Column '{column_name}' not found in the DataFrame.")
#     # df.to_excel(excel_file_path,index=False)
# def readpci():
#     excel_file_path = 'C:\FEAST\pcmd_db\GNR.xlsx'
#     df=pd.read_excel(excel_file_path,sheet_name='Sheet2')
        
#     BMC_Ip_list=df['BMC IP'].to_list()
#     print("BMC IP List=== ",BMC_Ip_list )
#     start_time=datetime.now()
#     try:
#        with ThreadPoolExecutor(max_workers=200) as executor:
#             results = executor.map(readPCICXL, BMC_Ip_list)
            
#             end_time=datetime.now()    
#             print("finished Pcie details in seconds",end_time-start_time)
#     except Exception as e:
#         print("Data Error as : ",e)
    
#     json_file_path_pcicxl = 'C:/FEAST/feast_app/json_data/pcicxl_output.json'
#     with open(json_file_path_pcicxl, 'w') as json_file:
#         json.dump(dict_pci, json_file) 



    
    
    
    
    
    
    
    
    
    
#     # excel_file_path = 'C:\FEAST\pcmd_db\GNR.xlsx'  
#     # df=pd.read_excel(excel_file_path,sheet_name='Sheet2') 
#     # dict_pci={} 
#     # column_name="BMC IP"
#     # if column_name in df.columns:
#     #     for value in df[column_name]:
#     #         # if is_host_reachable(value):
#     #         try :
#     #             data=readPCICXL(value)
#     #             print("current  value== ",value," type= ",type(value))
#     #             dict_pci[value]=data  
#     #             print("current data == ",dict_pci)
#     #         except Exception as e:
#     #             print("Not got data= ",value) 
#     #         # else :
#     #         #     print("Not reachable== ",value)  
#     #     json_file_path_pcicxl = 'C:/FEAST/feast_app/json_data/pcicxl_output.json'

#     #     # Open the file in write mode and use json.dump() to write the dictionary to the file
#     #     with open(json_file_path_pcicxl, 'w') as json_file:
#     #         json.dump(dict_pci, json_file)      
#     # else:
#     #         print(f"Column '{column_name}' not found in the DataFrame.")

# def readBiosVersion(result_dict,ip):
#     if(result_dict=="failed"): return
#     print("checking Bios data for ip == ",ip)
#     login_host=ip
#     try:
#         REDFISH_OBJ = redfish.redfish_client(base_url=login_host, username="root1", password="0penBmc1", default_prefix='/redfish/v1/',timeout=2)

#         # Login to the service
#         REDFISH_OBJ.login(auth="session")
    
#         System_response = REDFISH_OBJ.get("/redfish/v1/Systems/system")
        
    
#         System_data=pd.json_normalize(System_response.dict)

    
#         bios_version= System_data['BiosVersion'][0]
#         print("Bios version ::",bios_version)
#         dict_bios[ip]=str(bios_version) 
#         return bios_version
#     except Exception as e:
#         print("Bios not found ",e )
   
# def readBios(result_dict):
#     excel_file_path = 'C:\FEAST\pcmd_db\GNR.xlsx'  
#     df=pd.read_excel(excel_file_path,sheet_name='Sheet2') 
#     BMC_ip_list=[]
#     print("In read Bios")
#     for column,row in df.iterrows():
#             BMC_ip_list.append(row['BMC IP'])
   
#     print("BMC IP List : ",BMC_ip_list)
#     partial_func = partial(readBiosVersion, result_dict)
#     with ThreadPoolExecutor() as executer:
#         executer.map(partial_func,BMC_ip_list)
#     # excel_file_path = 'C:\FEAST\pcmd_db\GNR.xlsx'  
#     # df=pd.read_excel(excel_file_path,sheet_name='Sheet2') 
#     # dict_bios={} 
#     # column_name="BMC IP"
#     # if column_name in df.columns:
#     #     for value in df[column_name]:
#     #         # if is_host_reachable(value):
#     #             try:
#     #                 if(result_dict[value]=="success"):
#     #                     print("checking value  value== ",value)
#     #                     bios_version=readBiosVersion(value)
#     #                     dict_bios[value]=bios_version
#     #             except:
#     #                 print("Systtem not available == ",value)
#     #         # else :
#     #         #     print("Not reachable== ",value)  
#     json_file_path_bios = 'C:/FEAST/feast_app/json_data/biosVersion_output.json'

#         # Open the file in write mode and use json.dump() to write the dictionary to the file
#     with open(json_file_path_bios, 'w') as json_file:
#         json.dump(dict_bios, json_file)      


# result_dict = {}
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

# def startTestingIps():
#     live_hw_sheet_path="C:\FEAST\pcmd_db\GNR.xlsx"

#     df=pd.read_excel(live_hw_sheet_path)
#     working_ips_status=[]
#     not_working_ips=[]
#     # Replace with the IP you want to check
#     for column,row in df.iterrows():
#         Ip_adress=row['BMC IP']
        
#         if is_pingable(Ip_adress):   
#             working_ips_status.append("Reachable")
#         else:
#             print("added ",Ip_adress)
#             working_ips_status.append("Not Reachable")

#     df['BMC IP Status']=working_ips_status
#     working_ips = df[df['BMC IP Status'] == 'Reachable']['BMC IP'].tolist()
#     print("Working IPs:", working_ips)

  

#     start_time = datetime.now()
#     with ThreadPoolExecutor(max_workers=150) as executor:
#         executor.map(login_with_timeout, working_ips)
#     end_time = datetime.now()

#     print("Result time taken:", end_time - start_time)
  


#     for index, row in df.iterrows():
#         ip = row['BMC IP']
#         # Get the status from result_dict, default to 'Not Reachable' if not found
#         status = result_dict.get(ip, 'Not Reachable')
#         # Assign the status to the 'BMC IP Status' column
#         df.at[index, 'BMC IP Status'] = status

#     print("Status Updated")
#     df.to_excel(live_hw_sheet_path,index=False,sheet_name='Sheet2')    
#     return result_dict
# # startTestingIps()    




# readBMCIP()
# readpci()
# readBios()
# Updatesheet()

# config=configparser.ConfigParser()
# config_file_path="feast_app/config_data/config.ini"
# config.read(config_file_path)
# dict=config["dict1"]
# print("dict= ",dict['0xa808'])

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
                updated_DF.at[index, "BMC IP Status"] = "Pingable"
                if authenticate("https://"+str(row["BMC IP"])):
                    print("authentic")
                    updated_DF.at[index, "BMC IP Status"] = "Authentication Successful"
        except:
            print("mottttttttttttt")
            continue
    print(updated_DF)



# def start():
#     try:
#         with open(app_constants.REPO_STATS_FILE,"r") as f:
#             stat_data = json.load(f)
#         time_diff=1
#         try:
#             last_modified_at = datetime.strptime(stat_data["last_refreshed_at"],"%a, %Y-%m-%d, %H:%M:%S")
#             time_diff = (datetime.now() - last_modified_at).total_seconds()
#         except:
#             pass
#         if time_diff<120:
#             return {"error":"Last Refresh was only 2 minutes ago, please wait..."}
        
#         #Logic to update database
#         start_updates()
        
#         updated_at =datetime.now().strftime("%a, %Y-%m-%d, %H:%M:%S")
#         stat_data.update({"last_refreshed_at":updated_at})
#         with open(app_constants.REPO_STATS_FILE,"w") as f:
#             json.dump(stat_data,f)
            
#         return {"last_modified_at":updated_at}
#     except Exception as e:
#         print(e)
#         return {"error":"Error Occured while refreshing. Please contact Team."}
    
start_updates()