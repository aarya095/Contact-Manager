# Built-in Modules
import subprocess

from dotenv import dotenv_values

def stores_contact_num_key_in_env_file(key: bytes, name: str):
    """Stores the Contact Number key in the .env file"""

    name_of_key = f"KEY_OF_{name.upper()}" # Turning to upper case to maintain the format
    
    # decoding the key as would store along with the 'b' as prefix in the database
    key_str = key.decode('utf-8') 
    command = f"dotenv set {name_of_key} {key_str}"
    res = subprocess.run(command, shell=True, capture_output=True)

def retrieve_contact_num_key_from_env_file(name: str):
    """Retrieves the Contact Number key from the .env file"""

    name_of_key = f"KEY_OF_{name.upper()}"
    dict_of_keys = dotenv_values(".env")

    for key,value in dict_of_keys.items():
        
        if key == name_of_key:
            key_for_contact_number = value
            break
    # encoding the key as decrypt() function expects a bytes object
    key_for_contact_number = key_for_contact_number.encode('utf-8')

    return key_for_contact_number

