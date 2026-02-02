import psycopg
from dotenv import dotenv_values

config = dotenv_values(".env")

def connect_db():
    """Connects to the PostgreSQL database"""
    conn = psycopg.connect(dbname = config['DB_NAME'], user=config['DB_USER'], password=config['DB_PASS'])
    return conn

def create_contacts_table():
    """To create the contacts table"""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("CREATE TABLE contacts (contact_id SERIAL PRIMARY KEY, name VARCHAR (240) NOT NULL, number VARCHAR (240) NOT NULL, email VARCHAR (240) NULL);")
    conn.commit()
    cur.close()
    conn.close()

def view_contacts_table() -> list:
    """To extract all the data from the contacts table"""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("select * from contacts")
    
    contacts_data = cur.fetchall()
    print(contacts_data)

    cur.close()
    conn.close()

    return contacts_data

def create_contact_entry_in_db(name, encrypted_number, encrypted_email):
    """Creates an database entry of contact"""
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("insert into contacts (name, number, email) VALUES (%s, %s, %s);", \
                (name, encrypted_number, encrypted_email))    

    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    """Using the below to execute queries in the database"""
    #view_contacts_table()
    conn = connect_db()
    cur = conn.cursor()
    #cur.execute("delete from contacts where name='Vikas';")
    #cur.execute("ALTER TABLE contacts ADD COLUMN number BYTEA;")
    #data = cur.fetchall()
    #my_tuple = data[0]
    #print(my_tuple[0]) 

    #print(type(my_tuple[0]))
    conn.commit()
    cur.close()
    conn.close()