# Third Party Modules
from colorama import Fore, Style

# Local Modules
import modules.operations as op
import modules.get_and_validate_user_input as get_and_validate

def main():
    """Main function"""

    print(Fore.LIGHTGREEN_EX)


    while True:
        
        print(Fore.LIGHTCYAN_EX, Style.BRIGHT + "------------------------\n")
        print("1. Create Contact \n2. Update Contact")
        print("3. View Contact \n4. Delete Contact \n5. Search Contact")
        print("Enter 0 to exit | Enter 6 to export data | Enter 7 for help.\n")

        operation_input = get_and_validate.get_and_validate_input_operation()

        # Checks User input and performs the task
        if operation_input == 0:
            break

        elif operation_input == 1:
            op.create_contact()

        elif operation_input == 2:
            op.update_contact()

        elif operation_input == 3:
            op.view_contact()

        elif operation_input == 4:
            op.delete_contact()

        elif operation_input == 5:
            op.search_name()

        elif operation_input == 6:
            op.export_contacts_data()

        elif operation_input == 7:
            op.help()

    print("\n------------------------", end="")

    print(Fore.LIGHTGREEN_EX)
    print("╔═╗┌─┐┌─┐┬  ┬┌─┐┌─┐┌┬┐┬┌─┐┌┐┌  ╔═╗┬  ┌─┐┌─┐┌─┐┌┬┐")
    print("╠═╣├─┘├─┘│  ││  ├─┤ │ ││ ││││  ║  │  │ │└─┐├┤  ││")
    print("╩ ╩┴  ┴  ┴─┘┴└─┘┴ ┴ ┴ ┴└─┘┘└┘  ╚═╝┴─┘└─┘└─┘└─┘─┴┘\n")

if __name__ == '__main__':
    main()