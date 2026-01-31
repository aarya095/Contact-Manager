# Built-in Modules
import sqlite3

def connect_db():
    """Connects to the SQLite3 database"""
    conn = sqlite3.connect("contacts_data.db")
    return conn

def create_contacts_table():
    """To create the contacts table"""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("CREATE TABLE contacts (    name TEXT,    contact_number INT,    email TEXT);")
    conn.close()
    #cur.execute("pragma table_info(contacts)")

def view_contacts_table():
    """To view the contacts table"""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("select * from contacts")
    data = cur.fetchall()
    print(data)
    conn.close()

if __name__ == '__main__':
    """Using the below to execute queries in the database"""
    pass