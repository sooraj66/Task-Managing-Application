
# Task Manager Application

## Project Overview
This is a Task Manager Application with a Django backend and React frontend. Users can create, view, update, and delete tasks. The backend is built using Django REST Framework (DRF) with JWT authentication, and the frontend is implemented using React.

## Tech Stack
- **Backend**: Django, Django REST Framework (DRF), JWT
- **Database**: SQLite

## Prerequisites
Ensure you have the following installed:
- Python 3.12.5
- pip

## Backend Setup

### 1. **Download and Extract the Project**
- Download the project ZIP file.
- Extract the ZIP file to your desired location.

### 2. **Navigate to the Backend Directory**
- Open a terminal and navigate to the backend directory (where `manage.py` is located).

### 3. **Install Dependencies**
- Create and activate a virtual environment (optional but recommended):
  ```
  python -m venv venv
  source venv/bin/activate
  ```
- Install the required Python packages:
  ```
  pip install -r requirements.txt
  ```

### 4. **Apply Database Migrations**
- Run the following commands to set up the database:
  ```
  python manage.py makemigrations
  python manage.py migrate
  ```

### 5. **Start the Django Development Server**
- Run the server:
  ```
  python manage.py runserver
  ```
- The backend will be available at `http://localhost:8000`.
