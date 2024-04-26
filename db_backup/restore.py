import os
import sqlparse
from datetime import datetime
import psycopg2
from psycopg2 import sql
from io import StringIO
import re


# PostgreSQL database connection parameters
db_params = {
    "dbname": "feast_db",
    "user": "postgres",    
    "host": "localhost",
    "password": "sonalnirmal",
    "port": 5432
    
}

# Specify the main directory path
main_directory = "all_data"

subfolders = [os.path.join(main_directory, folder) for folder in os.listdir(main_directory) if os.path.isdir(os.path.join(main_directory, folder))]

def extract_timestamp(folder_name):
    try:
        timestamp_str = folder_name.split('_')[0]        
        return timestamp_str
    except ValueError:
        return None

max1=""

def get_latest_folder(subfolders):
    global max1
    for folder in subfolders:
        res=extract_timestamp(os.path.basename(folder))
        if res>max1:
            max1=res
            get_folder=folder
    
    return get_folder

res=get_latest_folder(subfolders)

# List SQL files inside the latest timestamp folder
sql_files = [os.path.join(res, file) for file in os.listdir(res) if file.endswith(".sql")]

# Establish a connection to the PostgreSQL database
connection = psycopg2.connect(**db_params)
# Create a cursor object to interact with the database
cursor = connection.cursor()

# Read the SQL script from the file
for sql_file in sql_files:

    print(f"Executing SQL file: {sql_file}")
    with open(sql_file, 'r') as f:
            sql_script = f.read()
            statements = re.split(r";\s*\n", sql_script)
            print(statements)
            for statement in statements:
                # Check if the statement is a COPY command
            
                if "COPY" in statement and "FROM stdin" in statement:
                    # Extract table and column details from the COPY command
                    copy_table_columns = re.search(r"COPY (.*) FROM stdin", statement).group(1)
                    table_name, columns = copy_table_columns.split("(", 1)               
                    
                    # Use copy_from() to execute the COPY command
                    copy_data = re.search(r"FROM stdin;\n(.*)\n\\\.", sql_script, re.DOTALL).group(1)
                    print(copy_data)
                    data_file = StringIO(copy_data)                
                    list1=table_name.split(".")
                    schema=list1[0]
                    table=list1[1]                
                    #cursor.execute("SET search_path = public")
                    copy_query = f"COPY {schema}.{table} FROM STDIN"
                    cursor.copy_expert(copy_query, data_file)
                    #cursor.copy_from(data_file,table_name.strip(), columns=[col.strip() for col in columns], null="")

                elif(statement[0].isdigit() or not statement.strip()):
                    continue
                elif(statement):
                    # Execute the statement normally for non-COPY commands
                    try:

                        print(statement)
                        cursor.execute(statement)
                        
                    except:
                        pass
            #cursor.execute(sql.SQL(sql_script))
                connection.commit()
    print("SQL script executed successfully!")

# Commit the changes (if the script includes data modifications)

connection.close()
cursor.close()

    




        
        

    




