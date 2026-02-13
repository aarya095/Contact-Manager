# Built-in Modules
import re
import subprocess
import json

# User-defined modules
import app.database.database as db
import app.get_and_validate_user_input as get_and_validate
import app.encryption as en
import app.file_operations as file_ops

def create_contact(name: str, number: int, email: str = None) -> str | bytes:
    """Creates an entry of contact"""
    
    list_of_users = db.get_users()
    if name not in list_of_users:
         
        encrypted_contact_number, contact_num_key = en.encrypt(number)
        file_ops.stores_contact_num_key_in_env_file(contact_num_key, name)

        if email != None:
            encrypted_email, email_key = en.encrypt(email)
            file_ops.stores_email_key_in_env_file(email_key, name)
        else:
            encrypted_email = email

        db.create_contact_entry_in_db(name, encrypted_contact_number, encrypted_email)
    else:
        print("User already exists")
    
    # print(f"Contact for {name_input} created successfully!")

def get_single_contact_data(name: str):
    """Gets a single contact data about a person from its name"""
    #Retrieves the contact number and decrypts it via its key in .env file
    key_for_contact_num = file_ops.retrieve_contact_num_key_from_env_file(name)
    key_for_email = file_ops.retrieve_email_key_from_env_file(name)

    encrypted_contact_data = db.get_encrypted_contact_data_from_db(name)
    encrypted_contact_num = encrypted_contact_data[1]
    encrypted_contact_email = encrypted_contact_data[0]
    
    original_contact_num_bytes = en.decrypt(encrypted_contact_num, key_for_contact_num)
    original_contact_num = int.from_bytes(original_contact_num_bytes, 'big') 

    if key_for_email != None:
        original_email_bytes = en.decrypt(encrypted_contact_email, key_for_email)
        original_email = original_email_bytes.decode('utf-8') 
    else: 
        original_email = None
    
    return original_contact_num, original_email

def view_contact():
    """View existing contacts"""

    conn = db.connect_db()

    cur = conn.cursor()
    cur.execute("select * from contacts")
    contacts_data = cur.fetchall()
    
    index = 1
    for contact_data in contacts_data:

        key_for_contact_num = file_ops.retrieve_contact_num_key_from_env_file(name)
        key_for_email = file_ops.retrieve_email_key_from_env_file(name)

        encrypted_contact_data = db.get_encrypted_contact_data_from_db(name)
        encrypted_contact_num = encrypted_contact_data[1]
        encrypted_contact_email = encrypted_contact_data[0]
        
        original_contact_num_bytes = en.decrypt(encrypted_contact_num, key_for_contact_num)
        original_contact_num = int.from_bytes(original_contact_num_bytes, 'big') 

        index += 1

    conn.close()

    # Checks for the already existing names in the database
    already_existing_names_list = get_and_validate.generate_list_of_already_used_names()
    if len(already_existing_names_list) == 0:
        print("No Entries!")

def update_contact():
    """Updates the contact information"""

    conn = db.connect_db()

    cur = conn.cursor()
    cur.execute("select * from contacts")
    contacts_data = cur.fetchall()

    index = 1
    for contact_data in contacts_data:
        print(f"\n({index})", end='')
        print(f" Name: {contact_data[0]}")
        index += 1

    # Checks if the name is already existing in the list or not
    already_existing_names_list = get_and_validate.generate_list_of_already_used_names()
    while True:
        update_name_input = input("\nEnter contact name you want to update? \n").lower().strip()
        if update_name_input in already_existing_names_list:
            break
        elif update_name_input not in already_existing_names_list:
            print("Error! Enter a name which is already in the list!")

    name_input = get_and_validate.get_and_validate_input_name()
    contact_num_input = get_and_validate.get_and_validate_input_number()
    email_input = get_and_validate.get_and_validate_input_email()

    conn = db.connect_db()

    cur = conn.cursor()
    cur.execute("update contacts set name = ? where name = ?", \
                (name_input, update_name_input))
    conn.commit()
    conn.close()

    # Encrypts and stores the contact number in the db and its key in the .env file
    contact_num_input = str(contact_num_input)
    contact_num_input = contact_num_input.encode('utf-8')
    encrypted_contact_number, contact_num_key = en.encrypt(contact_num_input)
    db.stores_encrypted_contact_num_in_db(encrypted_contact_number, name_input)
    db.stores_contact_num_key_in_env_file(contact_num_key, name_input)

    # Encrypts and stores the email in the db and its key in the .env file
    email_input = email_input.encode('utf-8')

    # Removing the keys from .env file 
    remove_unwanted_env_entries(update_name_input)

    print(f"Contact for {name_input} updated successfully!")
    conn.close()

def delete_contact():
    """Deletes the contact entry"""

    conn = db.connect_db() 

    cur = conn.cursor()
    cur.execute("select * from contacts")
    contacts_data = cur.fetchall()
    
    index = 1
    for contact_data in contacts_data:
        print(f"\n({index})", end='')
        print(f" Name: {contact_data[0]}")
        index += 1

    # Checks if the name is already existing in the list or not
    already_existing_names_list = get_and_validate.generate_list_of_already_used_names()
    while True:
        name_input = input("\nEnter contact name you want to delete? \n").lower().strip()
        if name_input in already_existing_names_list:
            break
        elif name_input not in already_existing_names_list:
            print("Error! Enter a name which already exists!")

    cur.execute("delete from contacts where name = ?", (name_input,))
    conn.commit()

    # Removing the keys from .env file 
    remove_unwanted_env_entries(name_input)

    print(f"\nContact for '{name_input}' deleted successfully!")
    conn.close()

def remove_unwanted_env_entries(name_input):
    """Removing the keys from .env file""" 

    name_of_email_key = f"KEY_OF_EMAIL_{name_input.upper()}"
    name_of_key = f"KEY_OF_{name_input.upper()}"
    
    command_to_remove_email_key = f"dotenv unset {name_of_email_key}"
    command_to_remove_key = f"dotenv unset {name_of_key}"
    
    res1 = subprocess.run(command_to_remove_email_key, shell=True, capture_output=True)
    res1 = subprocess.run(command_to_remove_key, shell=True, capture_output=True)

def export_contacts_data():
    """Exports all the data to a json file"""

    contacts_data_json = [] # list which will contain all the contacts info
    
    conn = db.connect_db()
    cur = conn.cursor()
    cur.execute("select * from contacts")
    contacts_data = cur.fetchall()

    for contact_data in contacts_data:
        #Loop for adding data to contacts_data_json
        original_contact_num = en.recreate_original_contact_num(contact_data[0])
        original_email = en.recreate_original_email(contact_data[0])

        contacts_data_json.append({'Name': contact_data[0],
                                   'Contact Number': original_contact_num,
                                   'Email': original_email})

    conn.close()

    already_existing_names_list = get_and_validate.generate_list_of_already_used_names()
    if len(already_existing_names_list) == 0:
        print("No Entries!")

    with open('contacts_data.json','w') as f:
        json.dump(contacts_data_json, f)
    print("\nData exported to contacts.json file successfully!")
        

if __name__ == '__main__':
    #create_contact("Umeko",934234235)
    original_contact_num, original_email = get_single_contact_data("Umeko")
    print(original_contact_num, original_email)