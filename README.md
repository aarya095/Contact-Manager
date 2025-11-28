<h1>Contact Manager (CLI)</h1>

<p>
  A command-line Contact Manager built in Python, designed for simple and efficient CRUD operations.  
  The application functions through an indexed menu system—select an operation by entering its corresponding number.
</p>

<h2>Features</h2>

<h3>Available Operations</h3>
<ol>
  <li>
    <b>Create Contact</b><br>
    Adds a new contact. User is prompted for required fields.
  </li>
  <li>
    <b>Update Contact</b><br>
    Modifies an existing contact. Requires an existing contact name.
  </li>
  <li>
    <b>View Contact</b><br>
    Displays all stored contacts in order.
  </li>
  <li>
    <b>Delete Contact</b><br>
    Permanently removes a contact. Requires the contact index.
  </li>
  <li>
    <b>Search Contact</b><br>
    Allows searching by name using regex-based lookup.
  </li>
  <li>
    <b>Export Contacts</b><br>
    Exports all contact data to <code>contacts_data.json</code>.
  </li>
  <li>
    <b>Help</b><br>
    Displays the application's manual.
  </li>
  <li>
    <b>Exit</b><br>
    Closes the application.
  </li>
</ol>

<h3>Instructions</h3>
<ul>
  <li>Enter only integer indices.</li>
  <li>Invalid inputs trigger an error message; re-enter a valid number.</li>
  <li>Follow on-screen prompts for each operation.</li>
</ul>

<hr>

<h2>CLI Preview</h2>
<p>Introductory Message</p>
<img width="600" alt="Screenshot_20251128_163608" src="https://github.com/user-attachments/assets/f6b08f30-2cbc-4f38-80a3-75a505861d90" />
<p>Create Entry Demo</p>
<img width="420" alt="Screenshot_20251128_164322" src="https://github.com/user-attachments/assets/8116044a-5c08-47f3-a698-c8a727e5544a" />
<p>View Entry Demo</p>
<img width="330" alt="Screenshot_20251128_164736" src="https://github.com/user-attachments/assets/a886447a-918f-447c-a134-1404a315c6bd" />
<p>Update Entry Demo</p>
<img width="420" alt="Screenshot_20251128_164918" src="https://github.com/user-attachments/assets/6bc5f74b-5861-4398-93f4-11a78001af01" />
<p>Delete Entry Demo</p>
<img width="440" alt="Screenshot_20251128_165028" src="https://github.com/user-attachments/assets/f763535b-fd50-4214-a09e-2b12b2e934bf" />
<p>Search Demo</p>
<img width="410" alt="Screenshot_20251128_165139" src="https://github.com/user-attachments/assets/32efdd7a-783f-4213-a037-d694bf2b7065" />
<p>Exporting to json</p>
<img width="505" height="100" alt="Screenshot_20251128_165233" src="https://github.com/user-attachments/assets/f5eb7eb4-6072-47f6-ab93-d3f120a94ffd" />
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
  The <b>contact number</b> and <b>email</b> fields are stored in encrypted form using <b>Fernet</b> from the <code>cryptography</code> package.
  Their keys are stored in a <code>.env</code> file and loaded using <code>python-dotenv</code>.
</p>

<hr>

<h2>Validation and Utilities</h2>

<ul>
  <li><b>Email Validation:</b> Implemented using the <code>validators</code> package.</li>
  <li><b>Exporting:</b> Performed via the <code>json</code> module and standard file operations.</li>
  <li><b>Search:</b> Uses the <code>re</code> module with the <code>search()</code> function and <code>IGNORECASE</code>.</li>
  <li><b>CRUD:</b> Full create, read, update, delete functionality is implemented.</li>
</ul>

<hr>

<h2>Project Structure</h2>

<ul>
  <li>
    <b>database.py</b><br>
    Handles SQLite3 connection and database queries.
  </li>
  <li>
    <b>get_and_validate_user_input.py</b><br>
    Contains input validation functions used across the application.
  </li>
  <li>
    <b>encryption.py</b><br>
    Provides encryption and decryption for email and contact number.
  </li>
  <li>
    <b>operations.py</b><br>
    Implements all CRUD operations, search, export, and help functionality.
  </li>
  <li>
    <b>main.py</b><br>
    Runs the entire application coherently.
  </li>
</ul>

<hr>

<h2>Usage</h2>
<p>
  Run the application:
</p>

<pre>
python main.py
</pre>

<hr>

<h2>Requirements</h2>
<ul>
  <li>Python 3.x</li>
</ul>

<hr>

<h2>Author</h2>
<p>
<b>Aarya</b><br>
IT Engineering student | Building in Full Stack Development and Cybersecurity
</p>
