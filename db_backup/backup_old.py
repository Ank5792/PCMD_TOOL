import subprocess
import sys
import os
from datetime import datetime

# Add the path to the instance folder to sys.path
instance_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'instance'))
sys.path.append(instance_path)

# Import configuration variables from app_configs.py
from app_configs import DB_USER, PSQL_DB, PROJECTS_TABLE, USERS_TABLE, DB_PASS

# Set the PostgreSQL password as an environment variable
os.environ["PGPASSWORD"] = DB_PASS

# List of tables to backup
tables_to_backup = [PROJECTS_TABLE, USERS_TABLE]

# Get the current date and time
current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Loop through the tables and perform backups
for table in tables_to_backup:
    if not os.path.exists(table):
        os.mkdir(table)
    backup_file = f"{table}//{table}_backup_{current_datetime}.sql"
    
    # Define the pg_dump command
    command = [
        'pg_dump',
        '-U', DB_USER,
        '-d', PSQL_DB,
        '-t', table,
        '-f', backup_file
    ]

    # Execute the command
    subprocess.run(command, check=True)

# Remove the PGPASSWORD environment variable
del os.environ["PGPASSWORD"]
