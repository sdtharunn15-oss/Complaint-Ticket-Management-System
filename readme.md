Complaint & Ticket Management System

A RESTful backend application built with **FastAPI** for managing customer complaints and support tickets. The system provides secure authentication, role-based authorization, customer management, ticket management, ticket assignment, search, filtering, pagination, and reporting.


Features

Authentication

* JWT Authentication
* User Registration
* User Login
* Password Hashing using bcrypt

User Roles

* Admin
* Customer
* Support Agent

Customer Management

* Create Customer
* View All Customers
* View Customer by ID
* Update Customer
* Delete Customer

Ticket Management

* Create Ticket
* View All Tickets
* View Ticket by ID
* Update Ticket
* Delete Ticket

Ticket Assignment

* Assign Tickets to Support Agents
* View Tickets Assigned to an Agent

Search & Reports

* Search Tickets by Title
* Filter by Priority
* Filter by Status
* View Customer Tickets
* Pagination Support

Validation & Security

* JWT Protected APIs
* Unique Email Validation
* Phone Number Validation
* Role-Based Authorization

Tech Stack

* Python 3.9+
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* JWT Authentication
* Passlib (bcrypt)
* Uvicorn
* Pytest


Project Structure

text
complaint_ticket_management_system/
│
├── routers/
│   ├── auth.py
│   ├── customers.py
│   ├── tickets.py
│   └── agents.py
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_customers.py
│   ├── test_tickets.py
│   └── test_agents.py
│
├── database.py
├── models.py
├── schemas.py
├── security.py
├── main.py
├── requirements.txt
├── README.md
└── complaint.db

Installation

Clone the Repository

bash
git clone <repository-url>
cd complaint_ticket_management_system


Create Virtual Environment

Windows

bash
python -m venv venv
venv\Scripts\activate

Linux / macOS

bash
python3 -m venv venv
source venv/bin/activate

Install Dependencies

bash
pip install -r requirements.txt


Run the Server

bash
uvicorn main:app --reload


Open:


http://127.0.0.1:8000/docs



Authentication APIs

| Method | Endpoint       | Description   |
| ------ | -------------- | ------------- |
| POST   | /auth/register | Register User |
| POST   | /auth/login    | Login User    |



Customer APIs

| Method | Endpoint                         |
| ------ | -------------------------------- |
| POST   | /customers                       |
| GET    | /customers                       |
| GET    | /customers/{customer_id}         |
| PUT    | /customers/{customer_id}         |
| DELETE | /customers/{customer_id}         |
| GET    | /customers/{customer_id}/tickets |



Ticket APIs

| Method | Endpoint             |
| ------ | -------------------- |
| POST   | /tickets             |
| GET    | /tickets             |
| GET    | /tickets/{ticket_id} |
| PUT    | /tickets/{ticket_id} |
| DELETE | /tickets/{ticket_id} |

Search Example

/tickets?title=laptop


Filter by Priority

/tickets?priority=High


Filter by Status

/tickets?status=Open

Pagination


/tickets?page=1&limit=10



Agent APIs

| Method | Endpoint                                      |
| ------ | --------------------------------------------- |
| POST   | /agents/tickets/{ticket_id}/assign/{agent_id} |
| GET    | /agents/{agent_id}/tickets                    |



Business Rules

* One customer can create multiple tickets.
* One ticket can be assigned to only one support agent.
* Closed tickets cannot be updated.
* Only the assigned support agent can update the ticket status.
* Customers can view only their own tickets.
* Support agents can manage only assigned tickets.
* Admin can manage all modules.



Validation

* Unique Email Address
* Valid 10-digit Phone Number
* JWT Authentication
* Password Hashing
* Role-Based Authorization


Testing

Run all tests using:

bash
pytest



Sample Roles

Admin

* Manage Customers
* Manage Tickets
* Assign Tickets
* View All Records

Customer

* Create Tickets
* View Own Tickets
* Update Own Profile

Support Agent

* View Assigned Tickets
* Update Assigned Ticket Status



Future Enhancements

* Email Notifications
* Ticket Comments
* File Attachments
* Dashboard & Analytics
* Docker Support
* PostgreSQL Integration
* Audit Logs
* API Rate Limiting


Author

Tharun

Backend Developer | FastAPI | Python | SQLAlchemy
