import subprocess
import sys
import psycopg2
import os
#from datetime import datetime
import shutil
import datetime

# Add the path to the instance folder to sys.path
instance_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'instance'))
sys.path.append(instance_path)

# Import configuration variables from app_configs.py
from app_configs import DB_USER, PSQL_DB, DB_PASS


def delete_old_folders(folder_path, days_threshold):
    today = datetime.datetime.now()
    
    for folder_name in os.listdir(folder_path):
        folder_date_str = folder_name.split('_')[0]
        
        try:
            folder_date = datetime.datetime.strptime(folder_date_str, '%Y-%m-%d')
        except ValueError:
            continue
        
        days_difference = (today - folder_date).days
        
        if days_difference > days_threshold:
            folder_to_delete = os.path.join(folder_path, folder_name)
            shutil.rmtree(folder_to_delete)
            print(f"Deleted folder: {folder_name}")


def tables_dict():
    # database connection details
    db_name = PSQL_DB
    db_user = DB_USER
    db_host = "localhost"
    db_port = "5432"
    # Set the PostgreSQL password as an environment variable
    os.environ["PGPASSWORD"] = DB_PASS
    psql_command = [
        "C:\\Program Files\\PostgreSQL\\15\\bin\\psql.exe",
        "-d", db_name,
        "-U", db_user,
        "-h", db_host,
        "-p", db_port,
        "-c", "\d"  # \dt is the psql command to list tables
    ]

    # Execute the psql command and capture the output
    output = subprocess.run(psql_command, stdout=subprocess.PIPE, text=True).stdout

    # Remove unnecessary lines and split the output into lines
    lines = output.strip().split("\n")[3:-1]

    # Initialize an empty dictionary
    relation_dict = {}
    # Process each line
    for line in lines:
        parts = line.split("|")
        schema = parts[0].strip()
        name = parts[1].strip()
        rel_type = parts[2].strip()
        relation_dict[name] = rel_type

    # Print the resulting dictionary
    del os.environ["PGPASSWORD"]
    #print(relation_dict)
    return relation_dict

def backup_table_data(tables_to_backup):
    
    os.environ["PGPASSWORD"] = DB_PASS

    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    db_folder = os.path.join(os.getcwd(), "all_data", current_datetime)
    if not os.path.exists(db_folder):
        os.mkdir(db_folder)

    for key, value in tables_to_backup.items():
        backup_file = f"{db_folder}\{key}_{value}.sql"
        print(backup_file)
        
        # Define the pg_dump command
        command = [
            'C:\\Program Files\\PostgreSQL\\15\\bin\\pg_dump.exe',
            '-U', DB_USER,
            '-d', PSQL_DB,
            '-t', key,
            '-f', backup_file
        ]

        # Execute the command
        subprocess.run(command, check=True)

    del os.environ["PGPASSWORD"]

def main():
    # getting list of all the tables available
    tables_to_backup = tables_dict()

    # backing up all the tables
    backup_table_data(tables_to_backup)

    all_data_path = os.path.join(os.getcwd(), "all_data")
    days_threshold = 20
    delete_old_folders(all_data_path, days_threshold)

if __name__ == "__main__":
    main()