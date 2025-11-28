import re
import subprocess
import modules.database as db
import modules.get_and_validate_user_input as get_and_validate
import modules.encryption as en

def create_contact():
    """Creates an entry of contact"""
    name_input = get_and_validate.get_and_validate_input_name()
    contact_num_input = get_and_validate.get_and_validate_input_number()
    email_input = get_and_validate.get_and_validate_input_email()
    null1 ='NULL'
    null2 ='NULL'
    conn = db.connect_db()
    cur = conn.cursor()

    cur.execute("insert into contacts VALUES (?,?,?)", \
                (name_input,null1, null2))
    conn.commit()
    conn.close()
    # Encrypts and stores the contact number in the db and its key in the .env file
    contact_num_input = str(contact_num_input)
    contact_num_input = contact_num_input.encode('utf-8')
    encrypted_contact_number, contact_num_key = en.encrypt(contact_num_input)
    en.stores_encrypted_contact_num_in_db(encrypted_contact_number, name_input)
    en.stores_contact_num_key_in_env_file(contact_num_key, name_input)

    # Encrypts and stores the email in the db and its key in the .env file
    email_input = email_input.encode('utf-8')
    encrypted_email, email_key = en.encrypt(email_input)
    en.stores_encrypted_email_in_db(encrypted_email, name_input)
    en.stores_email_key_in_env_file(email_key, name_input)

    print(f"Contact for {name_input} created successfully!")

def view_contact():
    """View existing contacts"""

    conn = db.connect_db()
    cur = conn.cursor()

    cur.execute("select * from contacts")
    contacts_data = cur.fetchall()
    
    index = 1
    for contact_data in contacts_data:

        original_contact_num = en.recreate_original_contact_num(contact_data[0])
        original_email = en.recreate_original_email(contact_data[0])

        print(f"\n({index})", end='')
        print(f" Name: {contact_data[0].title()}")
        print(f"    Contact Number: {original_contact_num}")
        print(f"    Email: {original_email}")
        index += 1
    conn.close()
    already_existing_names_list = get_and_validate.generate_list_of_already_used_names()
    if len(already_existing_names_list) == 0:
        print("No Entries!")

def update_contact():
    """Updates the contact information"""
    conn = db.connect_db() # connects to database
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

    conn = db.connect_db() # connects to database
    cur = conn.cursor()

    cur.execute("update contacts set name = ? where name = ?", \
                (name_input, update_name_input))
    conn.commit()
    conn.close()
    # Encrypts and stores the contact number in the db and its key in the .env file
    contact_num_input = str(contact_num_input)
    contact_num_input = contact_num_input.encode('utf-8')
    encrypted_contact_number, contact_num_key = en.encrypt(contact_num_input)
    en.stores_encrypted_contact_num_in_db(encrypted_contact_number, name_input)
    en.stores_contact_num_key_in_env_file(contact_num_key, name_input)

    # Encrypts and stores the email in the db and its key in the .env file
    email_input = email_input.encode('utf-8')
    encrypted_email, email_key = en.encrypt(email_input)
    en.stores_encrypted_email_in_db(encrypted_email, name_input)
    en.stores_email_key_in_env_file(email_key, name_input)

    print(f"Contact for {name_input} updated successfully!")
    conn.close()

def delete_contact():
    """Deletes the contact entry"""
    conn = db.connect_db() # connects to database
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
            print("Error! Enter a name which is already in the list!")

    cur.execute("delete from contacts where name = ?", (name_input,))
    conn.commit()

    # Removing the keys from .env file 
    name_of_email_key = f"KEY_OF_EMAIL_{name_input.upper()}"
    name_of_key = f"KEY_OF_{name_input.upper()}"
    command_to_remove_email_key = f"dotenv unset {name_of_email_key}"
    command_to_remove_key = f"dotenv unset {name_of_key}"
    res1 = subprocess.run(command_to_remove_email_key, shell=True, capture_output=True)
    res1 = subprocess.run(command_to_remove_key, shell=True, capture_output=True)

    print(f"\nContact for '{name_input}' deleted successfully!")
    conn.close()

def search_name():
    """Search operation to search for a specific name 
    from the list of already existing names and get the contact information"""

    already_existing_names_list = get_and_validate.generate_list_of_already_used_names()
    if len(already_existing_names_list) == 0:
        print("No Entries!")
    else:
        user_input_for_search = input("Enter the name you want to search: ")

        matched_cases_list = [] # list to store the names where input has matched 
        for name in already_existing_names_list:
            # Loops through the already_existing_names_list and matching using re.search function
            match_case = re.search(user_input_for_search, name, re.IGNORECASE) # Ignoring upper/lower case for better chances       
            if match_case:
                matched_cases_list.append(name)
            if match_case == None:
                pass
        if matched_cases_list == []:
            print("No matches found.")

        conn = db.connect_db()
        cur = conn.cursor()

        for name in matched_cases_list:

            cur.execute("select * from contacts where name = ?",(name,))
            contact_data = cur.fetchone()
            
            original_contact_num = en.recreate_original_contact_num(contact_data[0])
            original_email = en.recreate_original_email(contact_data[0])

            print("\nResults:")
            print(f"\nName: {contact_data[0]}")
            print(f"Contact Number: {original_contact_num}")
            print(f"Email: {original_email}")

        conn.close()
        
if __name__ == '__main__':
    search_name()