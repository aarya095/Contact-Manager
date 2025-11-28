<h1>🗂️ Contact Manager (CLI)</h1>

<p>
  A command-line Contact Manager built in Python, designed for simple and efficient CRUD operations.  
  The application functions through an indexed menu system—select an operation by entering its corresponding number.
</p>

<h2>📌 Navigate</h2>
<ul>
  <li><a href="#features">Features</a></li>
  <li><a href="#cli-preview">CLI Preview</a></li>
  <li><a href="#database">Database Schema</a></li>
  <li><a href="#validation-and-utilities">Validation and Utilities</a></li>
  <li><a href="#project-structure">Project Structure</a></li>
  <li><a href="#usage">Usage</a></li>
  <li><a href="#requirements">Requirements</a></li>
  <li><a href="#author">Author</a></li>
</ul>

<h2>Features</h2>

<h3>Available Operations</h3>
<ol>
  <li>
    ➕ <b>Create Contact</b><br>
    Adds a new contact. User is prompted for required fields.
  </li>
  <li>
    ✏️ <b>Update Contact</b><br>
    Modifies an existing contact. Requires an existing contact name.
  </li>
  <li>
    👁️ <b>View Contact</b><br>
    Displays all stored contacts in order.
  </li>
  <li>
    ❌ <b>Delete Contact</b><br>
    Permanently removes a contact. Requires the contact index.
  </li>
  <li>
    🔍 <b>Search Contact</b><br>
    Allows searching by name using regex-based lookup.
  </li>
  <li>
    💾 <b>Export Contacts</b><br>
    Exports all contact data to <code>contacts_data.json</code>.
  </li>
  <li>
    ℹ️ <b>Help</b><br>
    Displays the application's manual.
  </li>
  <li>
    🚪 <b>Exit</b><br>
    Closes the application.
  </li>
</ol>

<h3>📝 Instructions</h3>
<ul>
  <li>Enter only integer indices.</li>
  <li>Invalid inputs trigger an error message; re-enter a valid number.</li>
  <li>Follow on-screen prompts for each operation.</li>
</ul>

<hr>

<h2>CLI Preview</h2>
<p>Introductory Message</p>
<img width="600" alt="Intro Message" src="https://github.com/user-attachments/assets/f6b08f30-2cbc-4f38-80a3-75a505861d90" />
<p>Create Entry Demo</p>
<img width="420" alt="Create Entry" src="https://github.com/user-attachments/assets/8116044a-5c08-47f3-a698-c8a727e5544a" />
<p>View Entry Demo</p>
<img width="330" alt="View Entry" src="https://github.com/user-attachments/assets/a886447a-918f-447c-a134-1404a315c6bd" />
<p>Update Entry Demo</p>
<img width="420" alt="Update Entry" src="https://github.com/user-attachments/assets/6bc5f74b-5861-4398-93f4-11a78001af01" />
<p>Delete Entry Demo</p>
<img width="440" alt="Delete Entry" src="https://github.com/user-attachments/assets/f763535b-fd50-4214-a09e-2b12b2e934bf" />
<p>Search Demo</p>
<img width="410" alt="Search Entry" src="https://github.com/user-attachments/assets/32efdd7a-783f-4213-a037-d694bf2b7065" />
<p>Exporting to JSON</p>
<img width="505" height="100" alt="Export JSON" src="https://github.com/user-attachments/assets/f5eb7eb4-6072-47f6-ab93-d3f120a94ffd" />
<pre>[{"Name": "india", "Contact Number": "1231231231", "Email": "india@qwe.qwe"}, 
  {"Name": "kirti", "Contact Number": "6784566544", "Email": "kirti@gotmail.com"}, 
  {"Name": "aditi", "Contact Number": "9874560984", "Email": "aditi@email.com"}]</pre>

<hr>

<h2>Database</h2>

<p>
  The application uses <b>SQLite3</b> for storage.  
</p>
<p>Schema:</p>
<pre>
[(0, 'name', 'TEXT', 0, None, 0),
 (1, 'contact_number', 'INT', 0, None, 0),
 (2, 'email', 'TEXT', 0, None, 0)]
</pre>

<p>
  The <b>contact number</b> and <b>email</b> fields are stored in encrypted form using 🔑 <b>Fernet</b> from the <code>cryptography</code> package.
  Their keys are stored in a <code>.env</code> file and loaded using <code>python-dotenv</code>.
</p>

<hr>

<h2>Validation and Utilities</h2>
<ul>
  <li>📧 <b>Email Validation:</b> Implemented using the <code>validators</code> package.</li>
  <li>💾 <b>Exporting:</b> Performed via the <code>json</code> module and standard file operations.</li>
  <li>🔎 <b>Search:</b> Uses the <code>re</code> module with <code>search()</code> and <code>IGNORECASE</code>.</li>
  <li>⚙️ <b>CRUD:</b> Full create, read, update, delete functionality is implemented.</li>
</ul>

<hr>

<h2>Project Structure</h2>
<pre>
contacts_data.db
contacts_data.json
requirements.txt
main.py
modules/
├── __init__.py
├── database.py
├── encryption.py
├── get_and_validate_user_input.py
└── operations.py
</pre>

<ul>
  <li>🗄️ <b>database.py</b> — Handles SQLite3 connection and queries.</li>
  <li>🔐 <b>encryption.py</b> — Encrypts and decrypts email & contact number.</li>
  <li>📝 <b>get_and_validate_user_input.py</b> — Input validation functions.</li>
  <li>⚙️ <b>operations.py</b> — Implements CRUD, search, export, and help functions.</li>
  <li>▶️ <b>main.py</b> — Runs the application.</li>
</ul>

<hr>

<h2>Usage</h2>
<p>Run the application:</p>
<pre>
python main.py
</pre>

<hr>

<h2>Requirements</h2>
<ul>
  <li>🐍 Python 3.x</li>
  <li>🔑 cryptography==46.0.3</li>
  <li>📧 validators==0.35.0</li>
  <li>📝 dotenv==0.9.9</li>
</ul>

<hr>

<h2>Author</h2>
<p>
<b>Aarya Sarfare</b><br>
IT Engineering student | Building in Full Stack Development and Cybersecurity
</p>
