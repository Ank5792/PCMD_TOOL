import psycopg2
from pcmd_app import app
def get_db_connection():
    conn = psycopg2.connect(host="localhost",database=app.config["PSQL_DB"],user=app.config["DB_USER"],password=app.config["DB_PASS"])
    return conn


def get_user_from_db(key,value):
    user = None
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT * FROM {app.config['USERS_TABLE']} WHERE {key} = '{value}';")
        user = cursor.fetchone()
    conn.close()
    return user

def get_all_saved_users():
    users = None
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT email,idsid,profile_img_name FROM {app.config['USERS_TABLE']} ;")
        users = cursor.fetchall()
    conn.close()
    return users
    

def insert_new_user(email,nickname):
    insert_suc = False
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute(f"INSERT INTO {app.config['USERS_TABLE']} (email,idsid) VALUES ('{email}','{nickname}');")
        if cursor.rowcount == 1:
            insert_suc= True
    conn.commit()
    conn.close()
    return insert_suc

def get_all_projects():
    cur_projects = None
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT * FROM {app.config['PROJECTS_TABLE']} ;")
        cur_projects = cursor.fetchall()
    conn.close()
    return cur_projects

def insert_new_project(fields_tuple):
    insert_suc = False
    insert_query = f"INSERT INTO {app.config['PROJECTS_TABLE']} (owner,short_description,description,current_status,image_path,wiki_link,jira_link,ags_link,tool_links,tool_devs,tool_name) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute(insert_query,fields_tuple)
        if cursor.rowcount == 1:
            insert_suc= True
    conn.commit()
    conn.close()
    return insert_suc

def update_project(fields_tuple):
    update_suc = False
    update_query =  f"UPDATE {app.config['PROJECTS_TABLE']} SET owner=%s,short_description=%s,description=%s,current_status=%s,image_path=%s,wiki_link=%s,jira_link=%s,ags_link=%s,tool_links=%s,tool_devs=%s,tool_name=%s WHERE project_id = %s;"
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute(update_query,fields_tuple)
        if cursor.rowcount == 1:
            update_suc= True
    conn.commit()
    conn.close()
    return update_suc
