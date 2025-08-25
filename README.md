# Library Management System

A Django-based library management system for managing books, users, and loans in a school library. The system provides both admin and user interfaces with features for managing the complete lifecycle of library operations.

## Features

### Admin Features
- **User Management**
  - Create and manage user accounts with custom fields (fullname, class, member number)
  - Track user scores and history
  - View user statistics and borrowing patterns

- **Book Management** 
  - Import books from PDF catalog files
  - Search and browse book inventory
  - Track book status and availability
  - View popular books statistics

- **Loan Management**
  - Issue books to users
  - Process loan extensions and returns
  - Track overdue books
  - Manage loan requests

- **Dashboard**
  - Visual statistics for loans and returns
  - Overdue book monitoring
  - User activity tracking
  
- **AI Assistant**
  - Chat interface for quick information lookup
  - Smart recommendations based on user history
  - Natural language queries for library data

### User Features
- **Personal Dashboard**
  - View borrowed books
  - Track return dates
  - Check personal score
  - Request loan extensions

- **Book Discovery**
  - Search available books
  - Get personalized book recommendations
  - View borrowing history

## Installation

1. Clone the repository:
```sh
git clone https://github.com/AliAhmadi1080/khorami_library
cd khorami_library
```

2. Create and activate virtual environment:
```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies:
```sh
pip install -r requirements.txt
```

4. Configure environment variables:
- Create `.env` file with required settings
- Set `SECRET_KEY` and other environment variables

5. Setup database:
```sh
python manage.py migrate
```

6. Create admin user:
```sh
python manage.py createsuperuser
```

7. Run development server:
```sh
python manage.py runserver
```

The application will be available at http://127.0.0.1:8000/

## Tech Stack
- Django
- SQLite
- Tailwind CSS
- Chart.js
- OpenAI API (for AI features)
- PDF Plumber (for PDF processing)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
GNU General Public License