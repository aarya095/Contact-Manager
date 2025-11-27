import modules.database as db

def create_contact():
    """Creates an entry of contact"""
    name_input = input("Enter Name: ")
    contact_num_input = int(input("Enter Contact Number: "))
    email_input = input("Enter Email: ")

    conn = db.connect_db()
    cur = conn.cursor()

    cur.execute("insert into contacts VALUES (?,?,?)", \
                (name_input, contact_num_input, email_input))
    conn.commit()
    print(f"Contact for {name_input} created successfully!")
    conn.close()

def view_contact():
    """View existing contacts"""
    conn = db.connect_db()
    cur = conn.cursor()

    cur.execute("select * from contacts")
    contacts_data = cur.fetchall()
    
    index = 1
    for contact_data in contacts_data:
        print(f"\n({index})", end='')
        print(f" Name: {contact_data[0]}")
        print(f"    Contact Number: {contact_data[1]}")
        print(f"    Email: {contact_data[2]}")
        index += 1
    conn.close()

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
    update_name_input = input("\nEnter contact name you want to update? \n").lower().strip()

    name_input = input("Enter Name: ")
    contact_num_input = int(input("Enter Contact Number: "))
    email_input = input("Enter Email: ")

    cur.execute("update contacts set name = ?, contact_number = ?, " \
                "email = ? where name = ?", (name_input, contact_num_input, 
                                              email_input, update_name_input)) 

    conn.commit()
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

    name_input = input("\nWhose contact entry you want to delete? \n").lower().strip()

    cur.execute("delete from contacts where name = ?", (name_input,))
    conn.commit()

    print(f"\nContact for index '{name_input}' deleted successfully!")
    conn.close()

if __name__ == '__main__':
    delete_contact()
    view_contact()