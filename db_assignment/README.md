# Sales and Inventory Management System

This project is a Sales and Inventory Management System built with **FastAPI**, **MySQL**, and **Vanilla JavaScript**.

## Prerequisites

- **Python 3.8+**
- **MySQL Server** running locally with the following credentials (or update `database.py`):
    - User: `db_assignment`
    - Password: `1234`
    - Host: `localhost`

## Installation & Setup

1. **Create and Activate Environment**:
   It is recommended to use a virtual environment.
   ```bash
   conda create -n my_env python=3.10
   conda activate my_env
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Setup**:
   This will create the database `db_assignment`, all tables, and seed initial data.
   ```bash
   # Create database if not exists
   python create_database.py
   
   # Create tables
   python init_db.py
   
   # (Optional) Seed initial data (Admin, Products, Warehouses)
   python seed_data.py
   ```

## Running the Application

Start the FastAPI server:
```bash
uvicorn main:app --reload
```

## Accessing the Application

- **Web Interface**: Open [http://localhost:8000](http://localhost:8000)
    - **Login**: Select "Admin" or "User" from the landing page.
- **Admin Dashboard**: Manage products, check inventory, and view reports.
- **User Dashboard**: Browse products and place orders.

## API Documentation

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
