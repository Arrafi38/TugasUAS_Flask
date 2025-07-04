# Flask CRUD Application

A simple Flask application demonstrating CRUD operations with both REST API and web interface.

## Features

- RESTful API for user management
- Web interface with Bootstrap 5
- SQLite database using SQLAlchemy

## Installation

1. Clone this repository
2. Install dependencies: `pip install flask flask-sqlalchemy flask-restful`
3. Run the application: `python app.py`
4. Access web interface at http://127.0.0.1:5000/

## API Endpoints

- GET /api/users/ - List all users
- POST /api/users/ - Create a new user
- GET /api/users/<id> - Get a specific user
- PUT /api/users/<id> - Update a user
- DELETE /api/users/<id> - Delete a user#