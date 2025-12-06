# Built-in Modules
import sqlite3

def connect_db():
    """Connects to the SQLite3 database"""

    conn = sqlite3.connect("contacts_data.db")
    return conn

if __name__ == '__main__':
    """Using the below to execute queries in the database"""

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("pragma table_info(contacts)")
    #cur.execute("alter table keys rename column token TO encrypted_contact_number")
    #cur.execute("delete from contacts")
    #cur.execute("select * from contacts")
    data = cur.fetchall()
    print(data)
    #cur.execute("delete from keys")
    #conn.commit()
    conn.close()