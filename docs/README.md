# 🗂️ Contact Manager API

An Contact Manager API built in Python using FastAPI, designed for simple and efficient CRUD operations.

## 🚧 Project Status: In Progress

## 📌 Navigate

- [`Features`](#features)
- [`Tech Stack`](#tech-stack)
- [`Project Structure`](#project-structure)
- [`Setup Instructions`](#setup-instructions)
- [`Project Evolution`](#project-evolution)

## Features

- Create Contact: Adds a new contact
- Get a single contact: Retrieves the contact number of a single contact by name
- Get all contacts data: Retrieves all the encrypted contact numbers from the Database, decrypts them all, and returns them

## Tech Stack

- Programming Language: Python
- Web Framework: FastAPI
- Database: PostgreSQL and SQLite for development
- ORM: SQLAlchemy

## Project Structure
    
    .
    ├── app
    │   ├── database
    │   │   ├── database.py
    │   │   ├── db_operations.py
    │   │   ├── models.py
    │   ├── __init__.py
    │   ├── main.py
    │   ├── routes.py
    │   ├── schemas.py
    │   └── services
    │       ├── encryption.py
    │       ├── file_operations.py
    │       ├── operations.py
    ├── docs
    │   ├── Contact Manager API testing
    │   │   ├── Create Contact.yml
    │   │   ├── Get a single contact entry by name.yml
    │   │   └── opencollection.yml
    │   ├── contact_manager_design.drawio
    │   ├── README.md
    │   └── requirements.txt
    └── tests
        └── test_encryption.py


## Setup Instructions

1. Clone the repository:   
- `git clone https://github.com/aarya095/Contact-Manager.git`    
- `cd Contact-Manager`

2. Create a virtual environment:    
- `python -m venv venv`    
- `source venv/bin/activate`   # Linux/macOS    
- `venv\Scripts\activate`      # Windows    

3. Install dependencies:    
- `pip install -r docs/requirements.txt`

5. Run the server:    
- `uvicorn app.main:app --reload`

6. Open in browser:    
- http://127.0.0.1:8000/docs

## Project Evolution

This project originally started as a CLI-based Contact Manager application.

You can find the CLI version in the `cli` branch:
https://github.com/aarya095/Contact-Manager/tree/menu-driven-cli

<hr>

<p>

<b>Author: Aarya Sarfare</b>
</p>
