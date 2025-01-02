# Library Management System

This is a Django-based library management system for managing books, users, and loans in a school library.

## Features

- **User Management**:

  - Custom user model with fields like fullname, classname, joined_number, and username.
  - User creation form and view.

- **Book Management**:

  - Book model with fields like name, code, and row_number.
  - Book search form and view.

- **Loan Management**:

  - Loan model with fields like book, user, loan_date, return_date, is_return, and notes.
  - Loan creation form and view.
  - Loan undo view.

- **PDF Import**:

  - Function to handle uploaded PDF files and extract book data.
  - View to import Excel files.

- **Dashboard**:
  - Dashboard view displaying loan statistics.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/AliAhmadi1080/khorami_library
    cd khorami_library
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Apply migrations:
    ```sh
    python manage.py migrate
    ```

5. Create a superuser:
    ```sh
    python manage.py createsuperuser
    ```

6. Run the development server:
    ```sh
    python manage.py runserver
    ```

7. Access the application at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Usage

- **Login**: Access the login page at `/account/login/`.
- **Dashboard**: Access the dashboard at `/dashbord/`.
- **Create User**: Create a new user at `/create_user/`.
- **Create Loan**: Create a new loan at `/create_loan/`.
- **Search Books**: Search for books at `/search_books/`.
- **Import PDF File**: Import book data from a PDF file at `/import_file/`.

# TODO
- use stronger password generator 

## License

This project is licensed under the GNU General Public License v3.0.