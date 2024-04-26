import json
import os


path_folder = "C:\PCMD\instance"
with open (os.path.join(path_folder,"statistics.json") ,"r") as f:
    data=json.load(f)

data["today_hits"] =0
data["today_unique_hits"] =0

with open(os.path.join(path_folder,"statistics.json") ,"w") as f:
    json.dump(data,f)

with open("daily_ip_texts.txt","w") as f:
    f.write("")
