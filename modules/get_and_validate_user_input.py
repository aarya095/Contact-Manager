import validators as val
import modules.database as db

def get_and_validate_input_email():
    """Gets and Validates the input Email"""
    
    while True:
        email_input = input("Enter Email: ")
        if val.email(email_input):
            break
        if email_input == '':
            print("The email field can't be empty.")
        else:
            print(f"'{email_input}' is not a valid a valid email.")
    return email_input

def get_and_validate_input_number():
    """Gets and Validates the input Email"""

    while True:
        try:
            contact_num_input = int(input("Enter Contact Number: "))
            contact_num_input = str(contact_num_input)
            if len(contact_num_input) == len(range(10)):
                break
            elif len(contact_num_input) != len(range(10)):
                print("Contact number should be 10 integers long.")
        except ValueError:
            print("Please provide an integer.")
    contact_num_input = int(contact_num_input)
    return contact_num_input

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

def get_and_validate_input_name():
    """Gets and Validates the input Name"""

    already_existing_names_list = generate_list_of_already_used_names()
    
    while True:
        #Keeps looping till the below conitions are satisfied
        name_input = input("Enter Name: ").strip().lower()

        if name_input in already_existing_names_list: # checks if the user name already exists
            print(f"Contact by name '{name_input}' already exists.")

        if len(name_input) > 50:
            print("Length of Name should be under 50 characters.")

        if len(name_input) == 0:
            print("Name is required.")

        elif (name_input not in already_existing_names_list) and \
        (len(name_input) < 50) and (len(name_input) != 0):
            """Exit loop when name_input is not in already_existing_names_list 
            and length of the name_input is less then 50 and can't be empty"""
            break

    return name_input
        
def get_and_validate_input_operation():
    """Gets and Validates the input operation"""
    user_operation_choice_validation = [0,1,2,3,4,5,7]
    while True:
        try:
            user_choice = int(input("Select the operation by index: "))
            if user_choice in user_operation_choice_validation:
                break
            if user_choice not in user_operation_choice_validation:
                print("Please input either 0, 1, 2, 3, 4, 5 or 7.")

        except ValueError:
            print("Invalid Input! Please provide an integer.")

    return user_choice

if __name__ == '__main__':
    get_and_validate_input_name()
