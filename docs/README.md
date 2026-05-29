# 🗂️ Contact Manager API

FastAPI-based contact manager API with PostgreSQL, featuring CRUD operation and encrypted data handling.

## 🚧 Project Status: In Progress

## 📌 Navigate

- [`Features`](#features)
- [`Architecture`](#architecture)
- [`Tech Stack`](#tech-stack)
- [`Project Structure`](#project-structure)
- [`Setup Instructions`](#setup-instructions)
- [`Project Evolution`](#project-evolution)

## Features
- 🗂️ CRUD API
    - Create Contact: Adds a new contact
        - `POST /contacts`
    - Get a single contact: Retrieves the contact number of a single contact by name
        - `GET /contacts/{contact_id}`
    - Get all contacts data: Retrieves all the encrypted contact numbers from the Database, decrypts them all, and returns them
        - `GET /contacts`
    - Update contact entry: Updates an existing contact in the database, updates the encryption key
        - `PUT /contacts/{contact_id}`
    - Delete contact entry: Deletes an existing contact in the database, cleans the encryption key
        - `DELETE /contacts/{contact_id}`
- 🔐 Encryption
    - Contact numbers are encrypted using Fernet (symmetric encryption)
    - Key securely stored in .env file
    - Keys are generated, updated, and deleted as per the operation
- ⚙️ Architecture
    - Database layer
    - Service layer
    - Endpoint layer
- 📄 API Documentation
    - Documented using Bruno (local-first API client)
- 🌿 Git Workflow
    - Feature-based branching
    - Separate branches for debugging and enhancements
- 📜 Logging
    - Used python's in-built logging module for adding logging to my codebase
    - Logs capture key events across all layers
- 🧪 Testing
    - Used PyTest and FastAPI's TestClient to test all CRUD endpoints
    - Added unit tests for encryption and decryption utility functions
    - Verified API responses, status codes, and encrypted data handling

## Architecture

![Architecture Diagram](/docs/Diagrams/Data%20flow%20diagram.png)

## Tech Stack

- Programming Language: Python
- Web Framework: FastAPI
- Database: PostgreSQL and SQLite (development/testing)
- ORM: SQLAlchemy
- Validation: Pydantic
- Encryption: Fernet (cryptography)
- Testing: PyTest, FastAPI TestClient
- Logging: Python logging module
- API Testing & Documentation: Bruno
- Version Control: Git

## Project Structure
    
    .
    ├── Dockerfile
    ├── alembic
    ├── app
    │   ├── database
    │   │   ├── database.py
    │   │   ├── db_operations.py
    │   │   └── models.py
    │   ├── exceptions.py
    │   ├── logging_config.py
    │   ├── main.py
    │   ├── routes.py
    │   ├── schemas.py
    │   └── services
    │       ├── encryption.py
    │       └── operations.py
    ├── config
    │   └── config.py
    ├── docs
    │   ├── Contact Manager API testing
    │   ├── Diagrams
    │   └── README.md
    ├── requirements.txt
    ├── test.db
    └── tests
        ├── test_api.py
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
- `pip install -r requirements.txt`

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

After converting the app into an API, I first implemented a unique encryption key for each contact, with keys stored in the `.env` file. However, while preparing to Dockerize the app, I realized this approach wasn’t practical. I then simplified the design to use a single master encryption key stored in `.env`.

The per-contact encryption implementation is available in the `feature/per-contact-env-keys` branch:
https://github.com/aarya095/Contact-Manager/tree/feature/per-contact-env-keys

<hr>

<p>

<b>Author: Aarya Sarfare</b>
</p>
