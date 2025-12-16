# Third Party Modules
import validators as val

# User-defined modules
import modules.database as db

def get_and_validate_input_email(email_input):
    """Gets and Validates the input Email"""

    if val.email(email_input):
        return True
    if email_input == '':
        print("The email field can't be empty.")
    else:
        print(f"'{email_input}' is not a valid a valid email.")
        return False

def get_and_validate_input_number(contact_num_input):
    """Gets and Validates the input Email"""
    contact_num_input = str(contact_num_input)
    if len(contact_num_input) == len(range(10)):
        return True
    elif len(contact_num_input) != len(range(10)):
        print("Contact number should be 10 integers long.")
        return False

def get_and_validate_input_name(name_input):
    """Gets and Validates the input Name"""

    already_existing_names_list = generate_list_of_already_used_names()
    
    name_input = f"{name_input.strip().lower()}"

    if name_input in already_existing_names_list: # checks if the user name already exists
        print(f"Contact by name '{name_input}' already exists.")
        return False

    if len(name_input) > 50:
        print("Length of Name should be under 50 characters.")
        return False

    if len(name_input) == 0:
        print("Name is required.")
        return False

    elif (name_input not in already_existing_names_list) and \
    (len(name_input) < 50) and (len(name_input) != 0):
        """Exit loop when name_input is not in already_existing_names_list 
        and length of the name_input is less then 50 and can't be empty"""
        return True
    
# A utility function
def generate_list_of_already_used_names():
    """Generates a list of already used names"""

    conn = db.connect_db()

    cur = conn.cursor()
    cur.execute("select name from contacts")
    contacts_data = cur.fetchall()

    contact_names_list = []
    for contact_names in contacts_data:
        for contact_name in contact_names:
            contact_names_list.append(contact_name.lower())
    
    conn.close()

    return contact_names_list


if __name__ == '__main__':
    get_and_validate_input_name()
