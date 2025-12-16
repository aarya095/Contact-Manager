# Built-in Modules
import re
import subprocess
import json

# Third Party Modules
import click

# User-defined modules
import modules.database as db
import modules.get_and_validate_user_input as get_and_validate
import modules.encryption as en

@click.group()
def cli():
    pass

@cli.command()
@click.argument('name_input')
@click.argument('contact_num_input', type = int)
@click.argument('email_input')
def create_contact(name_input, contact_num_input, email_input):
    """Creates an entry of contact"""

    name_input = name_input.strip().lower()
    
    if get_and_validate.get_and_validate_input_name(name_input) == False or \
    get_and_validate.get_and_validate_input_number(contact_num_input) == False or \
    get_and_validate.get_and_validate_input_email(email_input) == False:
        exit()

    else:
        null1 ='NULL'
        
        conn = db.connect_db()
        
        # First name is stored in the db, as the contact num and email after being \
        # encrypted would be stored into db taking the name as the reference
        cur = conn.cursor()
        cur.execute("insert into contacts VALUES (?,?,?)", \
                    (name_input,null1, null1))
        conn.commit()
        
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
        
        conn.close()
        click.echo(f"Contact for {name_input} created successfully!")

@cli.command()
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
        click.echo(f" Name: {contact_data[0].title()}")
        click.echo(f"    Contact Number: {original_contact_num}")
        click.echo(f"    Email: {original_email}")
        index += 1

    conn.close()

    # Checks for the already existing names in the database
    already_existing_names_list = get_and_validate.generate_list_of_already_used_names()
    if len(already_existing_names_list) == 0:
        click.echo("No Entries!")

def update_contact():
    """Updates the contact information"""

    conn = db.connect_db()

    cur = conn.cursor()
    cur.execute("select * from contacts")
    contacts_data = cur.fetchall()

    index = 1
    for contact_data in contacts_data:
        print(f"\n({index})", end='')
        click.echo(f" Name: {contact_data[0]}")
        index += 1

    # Checks if the name is already existing in the list or not
    already_existing_names_list = get_and_validate.generate_list_of_already_used_names()
    while True:
        update_name_input = input("\nEnter contact name you want to update? \n").lower().strip()
        if update_name_input in already_existing_names_list:
            break
        elif update_name_input not in already_existing_names_list:
            click.echo("Error! Enter a name which is already in the list!")

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
    en.stores_encrypted_contact_num_in_db(encrypted_contact_number, name_input)
    en.stores_contact_num_key_in_env_file(contact_num_key, name_input)

    # Encrypts and stores the email in the db and its key in the .env file
    email_input = email_input.encode('utf-8')
    encrypted_email, email_key = en.encrypt(email_input)
    en.stores_encrypted_email_in_db(encrypted_email, name_input)
    en.stores_email_key_in_env_file(email_key, name_input)

    # Removing the keys from .env file 
    remove_unwanted_env_entries(update_name_input)

    click.echo(f"Contact for {name_input} updated successfully!")
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
        click.echo(f" Name: {contact_data[0]}")
        index += 1

    # Checks if the name is already existing in the list or not
    already_existing_names_list = get_and_validate.generate_list_of_already_used_names()
    while True:
        name_input = input("\nEnter contact name you want to delete? \n").lower().strip()
        if name_input in already_existing_names_list:
            break
        elif name_input not in already_existing_names_list:
            click.echo("Error! Enter a name which already exists!")

    cur.execute("delete from contacts where name = ?", (name_input,))
    conn.commit()

    # Removing the keys from .env file 
    remove_unwanted_env_entries(name_input)

    click.echo(f"\nContact for '{name_input}' deleted successfully!")
    conn.close()

def search_name():
    """Search operation to search for a specific name 
    from the list of already existing names and get the contact information"""

    already_existing_names_list = get_and_validate.generate_list_of_already_used_names()
    if len(already_existing_names_list) == 0:
        click.echo("No Entries!")
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
            click.echo("No matches found.")

        conn = db.connect_db()
        cur = conn.cursor()

        for name in matched_cases_list:

            cur.execute("select * from contacts where name = ?",(name,))
            contact_data = cur.fetchone()
            
            original_contact_num = en.recreate_original_contact_num(contact_data[0])
            original_email = en.recreate_original_email(contact_data[0])

            click.echo("\nResults:")
            click.echo(f"\nName: {contact_data[0].title()}")
            click.echo(f"Contact Number: {original_contact_num}")
            click.echo(f"Email: {original_email}")

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
        click.echo("No Entries!")

    with open('contacts_data.json','w') as f:
        json.dump(contacts_data_json, f)
    click.echo("\nData exported to contacts.json file successfully!")
        
def help():
    """Provides the user manual"""

    click.echo("\n=== APPLICATION MANUAL ===")
    click.echo("This CLI application operates by selecting an option number.")
    click.echo("Each operation is assigned an index. Enter the index to execute it.")
    click.echo()
    click.echo("AVAILABLE OPERATIONS:")
    click.echo("1. Create Contact")
    click.echo("   Use this option to add a new contact. You will be prompted for required fields.")
    click.echo()
    click.echo("2. Update Contact")
    click.echo("   Use this to modify an existing contact. You must enter an existing contact name.")
    click.echo()
    click.echo("3. View Contact")
    click.echo("   Lists every stored contact in order.")
    click.echo()
    click.echo("4. Delete Contact")
    click.echo("   Removes a contact permanently. Requires the contact index.")
    click.echo()
    click.echo("5. Search Contact")
    click.echo("   Allows searching by name.")
    click.echo()
    click.echo("6. Export Contacts")
    click.echo("   Exports all the contact information to contacts_data.json file.")
    click.echo()
    click.echo("7. Help")
    click.echo("   Displays this manual.")
    click.echo()
    click.echo("0. Exit")
    click.echo("   Closes the application.")
    click.echo()
    click.echo("INSTRUCTIONS:")
    click.echo("- Enter only integer indices.")
    click.echo("- Invalid inputs will trigger an error message; re-enter a valid number.")
    click.echo("- Follow on-screen prompts for each operation.")

if __name__ == '__main__':
    search_name()