window.onload = function () {
    loadContacts();

    document.getElementById("create-form")
        .onsubmit = createContact;
};


/*
|--------------------------------------------------------------------------
| Create Contact
|--------------------------------------------------------------------------
*/

async function createContact(event) {

    event.preventDefault();

    const name =
        document.getElementById("name").value;

    const phone =
        document.getElementById("phone").value;

    const response = await fetch("/contacts", {
        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            contact_name: name,
            contact_number: Number(phone)
        })
    });

    if (response.ok) {

        alert("Contact created successfully");

        document.getElementById("name").value = "";
        document.getElementById("phone").value = "";

        loadContacts();

    } else {

        alert("Failed to create contact");
    }
}


/*
|--------------------------------------------------------------------------
| Load All Contacts
|--------------------------------------------------------------------------
*/

async function loadContacts() {

    const response =
        await fetch("/contacts");

    if (!response.ok) {

        alert("Failed to load contacts");
        return;
    }

    const contacts =
        await response.json();

    const tableBody =
        document.getElementById("contacts-body");

    tableBody.innerHTML = "";

    for (let i = 0; i < contacts.length; i++) {

        const contact = contacts[i];

        tableBody.innerHTML +=
            "<tr>" +
                "<td>" + contact.contact_id + "</td>" +
                "<td>" + contact.contact_name + "</td>" +
                "<td>" + contact.contact_number + "</td>" +
                "<td>" +
                    "<button onclick='updateContact(" + contact.contact_id + ")'>Update</button> " +
                    "<button onclick='deleteContact(" + contact.contact_id + ")'>Delete</button>" +
                "</td>" +
            "</tr>";
    }
}


/*
|--------------------------------------------------------------------------
| Get Single Contact
|--------------------------------------------------------------------------
*/

async function getContact() {

    const id =
        document.getElementById("search-id").value;

    if (!id) {

        alert("Enter a contact ID");
        return;
    }

    const response =
        await fetch("/contacts/" + id);

    const resultDiv =
        document.getElementById("search-result");

    if (!response.ok) {

        resultDiv.innerHTML =
            "<p>Contact not found</p>";

        return;
    }

    const contact =
        await response.json();

    resultDiv.innerHTML =
        "<p><strong>Name:</strong> "
        + contact.contact_name +
        "</p>" +

        "<p><strong>Phone:</strong> "
        + contact.contact_number +
        "</p>";
}


/*
|--------------------------------------------------------------------------
| Update Contact
|--------------------------------------------------------------------------
*/

async function updateContact(id) {

    const newName =
        prompt("Enter new name");

    if (newName === null) {
        return;
    }

    const newPhone =
        prompt("Enter new phone number");

    if (newPhone === null) {
        return;
    }

    const response =
        await fetch("/contacts/" + id, {

            method: "PUT",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                contact_name: newName,
                contact_number: Number(newPhone)
            })
        });

    if (response.ok) {

        alert("Contact updated");
        loadContacts();

    } else {

        alert("Failed to update contact");
    }
}


/*
|--------------------------------------------------------------------------
| Delete Contact
|--------------------------------------------------------------------------
*/

async function deleteContact(id) {

    const confirmed =
        confirm("Delete this contact?");

    if (!confirmed) {
        return;
    }

    const response =
        await fetch("/contacts/" + id, {
            method: "DELETE"
        });

    if (response.ok) {

        alert("Contact deleted");
        loadContacts();

    } else {

        alert("Failed to delete contact");
    }
}