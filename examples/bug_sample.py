# Sample buggy Python code to demonstrate BharatCLI code review
import sqlite3

def get_user_data(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # Security Bug: Direct string formatting SQL Injection
    query = f"SELECT * FROM users WHERE id = '{user_id}'"
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows

def parse_config(config_dict):
    # Bug: Unhandled KeyError if 'timeout' missing
    timeout = config_dict['settings']['network']['timeout']
    
    # Bug: Unclosed file descriptor
    f = open("log.txt", "w")
    f.write(f"Config timeout is {timeout}")
    
    return timeout
