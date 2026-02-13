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
    cur.execute("CREATE TABLE contacts (contact_id SERIAL PRIMARY KEY, name VARCHAR (240) NOT NULL, number BYTEA NOT NULL, email BYTEA NULL);")
    conn.commit()
    cur.close()
    conn.close()

def view_contacts_table() -> list:
    """To extract all the data from the contacts table"""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("select * from contacts")
    
    contacts_data = cur.fetchall()
    #print(contacts_data)

    cur.close()
    conn.close()

    return contacts_data

def get_users() -> list:

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("select name from contacts")
    
    users = cur.fetchall()
    #print(contacts_data)

    cur.close()
    conn.close()

    list_of_users = []
    for user_tuple in users:
        list_of_users.append(user_tuple[0])
    
    return list_of_users

def create_contact_entry_in_db(name, encrypted_number, encrypted_email):
    """Creates an database entry of contact"""
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("insert into contacts (name, email, number) VALUES (%s, %s, %s);", \
                (name, encrypted_number, encrypted_email))    

    conn.commit()
    cur.close()
    conn.close()

def get_encrypted_contact_data_from_db(name: str) -> tuple:
    """Retrieves the encrypted_email from the sqlite3 db"""

    conn = connect_db()

    cur = conn.cursor()
    cur.execute("select number , email from contacts where name = %s", (name,))
    encrypted_contact_data = cur.fetchone()

    cur.close()
    conn.close()

    return encrypted_contact_data

if __name__ == '__main__':
    """Using the below to execute queries in the database"""

    #list_of_users = get_users()
    #print(list_of_users)
    encrypted_contact_data = get_encrypted_contact_data_from_db("Aarya")
    print(encrypted_contact_data)

"""    contacts_data = view_contacts_table()
    print(contacts_data)
    contacts_data = contacts_data[0]
    
    from app import encryption as en
    key_for_contact_number = en.retrieve_contact_num_key_from_env_file("aarya")
    key_for_email = en.retrieve_email_key_from_env_file("aarya")

    print(contacts_data)
    print(key_for_contact_number)
    encrypted_contact_data = contacts_data[2]
    original_data = en.decrypt(encrypted_contact_data=encrypted_contact_data, key=key_for_contact_number)
    print(type(original_data))
    original_data = int.from_bytes(original_data,'big')
    print(original_data)"""


"""    conn = connect_db()
    cur = conn.cursor()
    #cur.execute("delete from contacts;")
    #cur.execute("ALTER TABLE contacts ADD CONSTRAINT contacts_name_unique UNIQUE ();")
    #cur.execute("ALTER TABLE contacts ADD COLUMN number BYTEA;")
    #data = cur.fetchall()
    #my_tuple = data[0]
    #print(my_tuple[0]) 

    #print(type(my_tuple[0]))
    conn.commit()
    cur.close()
    conn.close()"""