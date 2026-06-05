# E-Commerce Flask API

## Author

**Magali Bogarin**  
GitHub: https://github.com/mbogarin

---

## Project Description

This project is a fully functional RESTful API for an e-commerce system built using Flask, SQLAlchemy, Marshmallow, and MySQL.

The application manages Users, Products, and Orders with proper relationships including one-to-many and many-to-many associations.

### Purpose of the Project

- Practice building a real-world backend API
- Learn relational database design with SQLAlchemy
- Implement CRUD operations using Flask routes
- Use Marshmallow for serialization and validation
- Work with MySQL as a relational database

### Features

- User management (create, read, update, delete)
- Product management (CRUD operations)
- Order creation and management
- Add/remove products from orders
- Order summary endpoint with total price calculation

---

## Table of Contents

- [Project Description](#project-description)
- [Installation & Setup](#installation--setup)
- [Database Setup](#database-setup)
- [API Endpoints](#api-endpoints)
- [Usage](#usage)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Collaborators](#collaborators)

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/mbogarin/ecommerce-flask-api.git
cd ecommerce-flask-api
```

### 2. Create virtual environment

```bash
python3 -m venv venv
```

### 3. Activate virtual environment

Mac/Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install Flask Flask-SQLAlchemy Flask-Marshmallow marshmallow-sqlalchemy mysql-connector-python
```

## Database Setup

1. Open MySQL Workbench
2. Create database:

```bash
CREATE DATABASE ecommerce_api;
```

3. Update database URI in app.py:

```bash
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:<YOUR_PASSWORD>@localhost/ecommerce_api'
```

## API Endpoints

User Endpoints

- GET /users
- GET /users/
- POST /users
- PUT /users/
- DELETE /users/

Product Endpoints

- GET /products
- GET /products/
- POST /products
- PUT /products/
- DELETE /products/

Order Endpoints

- POST /orders
- PUT /orders/<order_id>/add_product/<product_id>
- DELETE /orders/<order_id>/remove_product/<product_id>
- GET /orders/user/<user_id>
- GET /orders/<order_id>/products
- GET /orders/<order_id>/summary

⸻

## Usage

Run the application:

```bash
python app.py
```

The API will run on:

```bash
http://127.0.0.1:5000
```

Use Postman to test all endpoints by sending requests to the routes listed above.

## Testing

- Use Postman Collection to test all endpoints
- Verify data in MySQL Workbench
- Ensure CRUD operations work correctly
- Check relationships between Users, Orders, and Products

## Project Structure

```bash
ecommerce-flask-api/
│
├── app.py
├── venv/
└── README.md
```

## Collaborators

Currently this project was developed independently.
Future collaborators can be listed here:

### Credits

Classmates and mentors at Coding Temple
