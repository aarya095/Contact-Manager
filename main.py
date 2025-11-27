import modules.crud_operations as crud

def main():
    """Main function"""
    print("\nWelcome To Contant Manager!\n")

    while True:

        print("------------------------")
        print("\n1. Create Contact \n2. Update Contact")
        print("3. View Contact \n4. Delete Contact")
        print("Enter 0 to exit.\n")
        operation_input = int(input("Select the operation you want to perform: "))

        if operation_input == 0:
            break
        elif operation_input == 1:
            crud.create_contact()
        elif operation_input == 2:
            crud.update_contact()
        elif operation_input == 3:
            crud.view_contact()
        elif operation_input == 4:
            crud.delete_contact()

    print("\nThanks for using Contant Manager!\n")

if __name__ == '__main__':
    main()