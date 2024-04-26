import testAutomation as automater
import sched
import time
import os
import json
from threading import Thread
# Create a scheduler object
scheduler = sched.scheduler(time.time, time.sleep)
def trigger(ArtifactoryLink, Emails, Host_name, articleIds,data_dict,QueryId,testPlan):
    status=automater.start(ArtifactoryLink, Emails, Host_name, articleIds,QueryId,testPlan)
    print("Execution status: ",status)
    data_dict[QueryId][testPlan]["Tcd Config details"][Host_name]=status
def my_function():
    print("This function is running every second.")
    jsonPath="C:\\FEAST\\feast_app\\json_data\\AutomatedData.json"
    if os.path.exists(jsonPath):
        print("PathExist")
        with open(jsonPath, 'r') as file:
            data_dict = json.load(file)
        
        print("DataDict: ",data_dict)
        AvailableToExecute=False
        for QueryId,QueryItems in data_dict.items():
            for testPlan,testPlanItems in QueryItems.items():
                ArtifactoryLink=testPlanItems['Auto Trigger Inputs']['Artifactory Link']
                Emails=testPlanItems['Auto Trigger Inputs']['Email List']
                for hostName,hostNameItems in testPlanItems["Tcd Config details"].items():
              
                    if hostNameItems["Trigger status"]=="stored":
                        automation_thread = Thread(target=trigger,args=(ArtifactoryLink,Emails,hostName,hostNameItems['Test Case / Article Ids'],data_dict,QueryId,testPlan))
                        automation_thread.start()
                        hostNameItems["Trigger status"]="In Progess"
                        AvailableToExecute=True
        with open(jsonPath, 'w') as json_file:
            json.dump(data_dict, json_file)
        if not AvailableToExecute:
            print("Not found Any executable tescases")
    else:
        print("Path Not Found")

    # Schedule the function to run again after 1 second
    scheduler.enter(1, 1, my_function)

# Schedule the function to run initially
scheduler.enter(0, 1, my_function)

# Run the scheduler
scheduler.run()


#username_field.send_keys("nsonal")
#password_field.send_keys("IN@let$2024")