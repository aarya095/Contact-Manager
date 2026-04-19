# 🗂️ Contact Manager API

A Contact Manager API built in Python using FastAPI.

## 🚧 Project Status: In Progress

## 📌 Navigate

- [`Features`](#features)
- [`Tech Stack`](#tech-stack)
- [`Project Structure`](#project-structure)
- [`Setup Instructions`](#setup-instructions)
- [`Project Evolution`](#project-evolution)

## Features
- CRUD API
    - Create Contact: Adds a new contact
        - `POST /contacts`
    - Get a single contact: Retrieves the contact number of a single contact by name
        - `GET /contacts/{name}`
    - Get all contacts data: Retrieves all the encrypted contact numbers from the Database, decrypts them all, and returns them
        - `GET /contacts`
    - Update contact entry: Updates an existing contact in the database, updates the encryption key
        - `PUT /contacts/`
    - Delete contact entry: Deletes an existing contact in the database, cleans the encryption key
        - `DELETE /contacts/`
- 🔐 Field-Level Encryption
    - Contact numbers are encrypted using Fernet (symmetric encryption)
    - Key securely stored in .env file
    - Keys are generated, updated, and deleted as per the operation
- ⚙️ Architecture
    - Database layer
    - Business logic layer
    - API layer
- 📄 API Documentation
    - Documented using Bruno (local-first API client)
- 🌿 Git Workflow
    - Feature-based branching
    - Separate branches for debugging and enhancements 

## Tech Stack

- Programming Language: Python
- Web Framework: FastAPI
- Database: PostgreSQL and SQLite for development/testing
- ORM: SQLAlchemy
- Encryption: Fernet (cryptography)
- Validation: Pydantic
- Version Control: Git
- API Testing: Bruno

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
    │   │   ├── Get all contacts stored in the database.yml
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

4. Create `.env.dev` file:
- add `DATABASE_URL = 'sqlite:///dev.db'`

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
