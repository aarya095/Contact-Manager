import psycopg
from dotenv import dotenv_values

config = dotenv_values(".env")

def connect_db():
    """Connects to the SQLite3 database"""
    conn = psycopg.connect(dbname = config['DB_NAME'], user=config['DB_USER'], password=config['DB_PASS'])
    return conn

def create_contacts_table():
    """To create the contacts table"""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("CREATE TABLE contacts (contact_id SERIAL PRIMARY KEY, name VARCHAR (240) NOT NULL, number INTEGER NOT NULL, email VARCHAR (240) NULL);")
    conn.commit()
    cur.close()
    conn.close()

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
    view_contacts_table()