# Built-in Modules
import subprocess
from pathlib import Path

from app.database.database import env_file_path
from dotenv import dotenv_values
from dotenv import set_key, unset_key

def stores_contact_num_key_in_env_file(key: bytes, name: str):
    """Stores the Contact Number key in the .env file"""

    # Turning to upper case to maintain the format
    name_of_key = f"KEY_OF_{name.upper()}"
    
    """decoding the key as would store along 
    with the 'b' as prefix in the database"""
    key_str = key.decode('utf-8') 
    set_key(
        dotenv_path = env_file_path, 
        key_to_set = name_of_key, 
        value_to_set = key_str
        )

def retrieve_contact_num_key_from_env_file(name: str) -> bytes:
    """Retrieves the Contact Number key from the .env file"""

    name_of_key = f"KEY_OF_{name.upper()}"
    dict_of_keys = dotenv_values(env_file_path)

    for key,value in dict_of_keys.items():
        
        if key == name_of_key:
            key_for_contact_number = value
            break
    # encoding the key as decrypt() function expects a bytes object
    key_for_contact_number = key_for_contact_number.encode('utf-8')

    return key_for_contact_number

def deletes_contact_num_key_in_env_file(name: str):
    """Deletes the Contact Number key in the 
    .env file which is no longer required"""

    name_of_key_to_delete = f"KEY_OF_{name.upper()}"
    unset_key(
        dotenv_path = env_file_path, 
        key_to_unset = name_of_key_to_delete
        )
    
