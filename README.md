# Library Management System Using Python 

A Django-based web application designed to simplify library operations by managing book records, member accounts, borrowing activities, and book returns. The system provides a responsive interface, book search and category filtering, role-based administrative functionality, and borrowing history.

## Features

- User registration, login, and logout
- Book catalogue with search, category filtering, and pagination
- Book detail pages with availability information
- Admin and staff functionality for adding, editing, and deleting books
- Book borrowing and return management
- Automatic due dates set to 14 days after borrowing
- Maximum of five active loans for regular members
- Member dashboard with borrowing statistics
- Staff dashboard with book, member, and borrowing statistics
- Borrowing history and overdue book indicators
- Django administration panel for managing application data
- Sample book catalogue using a Django management command
- Automated tests for verifying application functionality
- Responsive user interface for convenient browsing

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django 5.2 | Web framework and application logic |
| SQLite | Relational database |
| HTML5 | Web page structure |
| CSS3 | Styling and responsive layout |
| JavaScript | Frontend interactions |
| Django ORM | Database operations |
| Django Authentication | User authentication and access control |

## System Requirements

- Python 3.10 or newer
- pip package manager
- A modern web browser
- Visual Studio Code or another Python-compatible editor (optional)

## Installation and Setup

### 1. Clone or Download the Project

Download the project ZIP and extract it to a folder on your computer.

Open the project folder in Visual Studio Code or a terminal.

### 2. Create a Virtual Environment

Run the following command in Windows PowerShell:

```powershell
python -m venv venv
```

### 3. Activate the Virtual Environment

```powershell
.\venv\Scripts\activate
```

If PowerShell does not allow activation, open Command Prompt and run:

```cmd
venv\Scripts\activate.bat
```

### 4. Install Dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Apply Database Migrations

```powershell
python manage.py migrate
```

### 6. Create an Administrator Account

```powershell
python manage.py createsuperuser
```

Enter the requested username, email address, and password.

### 7. Add Sample Books

```powershell
python manage.py seed_books
```

This command inserts sample books into the catalogue. Books with existing matching ISBN values are not duplicated.

### 8. Run the Development Server

```powershell
python manage.py runserver
```

Open the following address in your browser:

http://127.0.0.1:8000/

## Main Application URLs

| URL | Description |
|---|---|
| `/` | Home page |
| `/books/` | Browse and search books |
| `/signup/` | Register a new member |
| `/login/` | User login |
| `/logout/` | User logout |
| `/dashboard/` | Member or staff dashboard |
| `/books/add/` | Add a book (staff only) |
| `/borrowings/` | View borrowing records |
| `/admin/` | Django administration panel |

## How the System Works

### 1. User Registration and Login

Members can create an account and log in using their credentials. Django's authentication system manages user sessions and restricts access to protected pages.

### 2. Book Catalogue

Users can browse available books, search by relevant details, filter by category, and open individual book detail pages.

### 3. Book Management

Authorized staff members can add new books, update existing book information, and delete books when there are no active borrowing records for them.

### 4. Book Borrowing

Authenticated members can borrow available books. The system checks book availability, prevents duplicate active loans for the same book, and limits regular members to five active loans.

### 5. Book Returns

Members can return their own borrowed books. Staff members can manage returns for any member. Successful returns update the borrowing record and the book's available copy count.

### 6. Dashboards and Borrowing History

Members can view their borrowing records and relevant statistics. Staff users can view library-wide statistics, recent borrowing records, and overdue information.

## Database

The application uses SQLite as its default database. Django ORM manages database interactions without requiring manual SQL queries for routine operations.

The main data entities include:

- **User:** Stores account information and authentication details.
- **Book:** Stores the title, author, ISBN, category, description, total copies, and available copies.
- **BorrowRecord:** Tracks borrowing transactions, members, due dates, return dates, and borrowing status.

Database migrations are used to create and update the database schema.

## Testing

Run the following command to execute the project's automated tests:

```powershell
python manage.py test
```

The tests help verify application behavior, including authentication, book management, borrowing operations, and access restrictions implemented in the test suite.

## Project Structure

```text
library_management_system/
├── library_project/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── library/
│   ├── migrations/
│   ├── management/
│   │   └── commands/
│   │       └── seed_books.py
│   ├── templates/
│   │   └── library/
│   ├── static/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
├── templates/
├── static/
├── manage.py
├── requirements.txt
└── README.md
```

The exact folder arrangement may vary depending on the project version and where templates and static files are configured.

## Security and Production Considerations

This project is intended for educational and demonstration purposes. Before deploying it to a production environment, the following measures should be considered:

- Set `DEBUG = False`.
- Store the Django secret key in an environment variable.
- Configure `ALLOWED_HOSTS` for the deployment environment.
- Use HTTPS and secure session and CSRF cookie settings.
- Keep database credentials outside source control.
- Configure regular database backups.
- Review authentication, authorization, and form validation.
- Assign staff privileges only to trusted administrators.
- Configure a production-ready database, such as PostgreSQL or MySQL, if required.
- Run Django's deployment checks before publishing the application.

## Future Enhancements

Possible future improvements include:

- Automated email notifications for upcoming due dates
- Fine calculation for overdue books
- Barcode or QR-code-based book identification
- Advanced reports and analytics
- Book reservation and waiting-list functionality
- Exporting library reports
- Integration with external book catalogue services

## Learning Outcomes

This project demonstrates practical knowledge of Python programming, Django web development, database management, authentication, CRUD operations, responsive frontend development, application testing, and software engineering principles.

It provides experience in designing and implementing a web application that addresses common library management requirements.