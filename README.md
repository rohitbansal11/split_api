# Test-Splitwise

A FastAPI-based expense sharing application that allows users to create groups, add members, track expenses, and calculate balances. Similar to Splitwise, this application helps friends and groups split expenses fairly.

## Features

- **User Management**: User registration, authentication with JWT tokens, user search, and profile management
- **Group Management**: Create groups, add/remove members, view group details and members
- **Expense Tracking**: Create, edit, and delete expenses within groups
- **Balance Calculation**: Calculate and view expense balances for groups
- **Activity Logging**: Track activities within groups (member additions, expense creation, etc.)
- **Connections**: Manage connections between users

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT (JSON Web Tokens) with python-jose
- **Password Hashing**: bcrypt (via passlib)
- **Server**: Uvicorn

## Project Structure

```
test-spitwise/
├── src/
│   ├── activity/          # Activity tracking module
│   │   ├── modal.py       # Activity database model
│   │   ├── routes.py      # Activity API routes
│   │   ├── scheema.py     # Activity Pydantic schemas
│   │   └── service.py     # Activity business logic
│   ├── connect/           # User connections module
│   │   ├── modal.py       # Connect database model
│   │   ├── routes.py      # Connect API routes
│   │   ├── scheema.py     # Connect Pydantic schemas
│   │   └── service.py     # Connect business logic
│   ├── database/          # Database configuration
│   │   └── db.py          # Database connection and session management
│   ├── expances/          # Expense management module
│   │   ├── modal.py       # Expense database model
│   │   ├── routes.py      # Expense API routes
│   │   ├── scheema.py     # Expense Pydantic schemas
│   │   └── service.py     # Expense business logic
│   ├── group/             # Group management module
│   │   ├── group_member.py # Group member database model
│   │   ├── group_modal.py  # Group database model
│   │   ├── routes.py       # Group API routes
│   │   ├── scheema.py      # Group Pydantic schemas
│   │   └── service.py      # Group business logic
│   ├── user/              # User management module
│   │   ├── modal.py       # User database model
│   │   ├── routes.py      # User API routes
│   │   ├── scheema.py     # User Pydantic schemas
│   │   └── service.py     # User business logic
│   ├── utils/             # Utility modules
│   │   ├── deps.py        # Dependency injection (auth, db)
│   │   ├── errors.py      # Error handlers
│   │   ├── hash.py        # Password hashing utilities
│   │   ├── jwt_handler.py # JWT token generation/validation
│   │   └── middleware.py  # Custom middleware
│   └── main.py            # FastAPI application entry point
└── requirements.txt       # Python dependencies
```

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL database
- pip (Python package manager)

### Setup

1. **Clone the repository** (if applicable) or navigate to the project directory:
   ```bash
   cd test-spitwise
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the database**:
   - Update the database connection string in `src/database/db.py`
   - Replace the connection URL with your PostgreSQL credentials:
     ```python
     SQLALCHEMY_DATABASE_URL = "postgresql://username:password@host:port/database"
     ```

5. **Run the application**:
   ```bash
   uvicorn src.main:app --reload
   ```

   The API will be available at `http://localhost:8000`

6. **Access the API documentation**:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### User Endpoints (`/users`)

- `POST /users/` - Create a new user
- `GET /users/` - Get all users
- `GET /users/{user_id}` - Get user by ID
- `GET /users/email/{email}` - Get user by email
- `GET /users/exists/{email}` - Check if user exists
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user
- `POST /users/login` - User login (returns JWT token)
- `GET /users/checkuser/me` - Get current authenticated user
- `GET /users/search/{value}` - Search users by email, name, or phone

### Group Endpoints (`/groups`)

- `POST /groups/create-group` - Create a new group
- `GET /groups/get-all-groups` - Get all groups for current user
- `GET /groups/get-group-by-id/{group_id}` - Get group by ID
- `POST /groups/add-member-to-group` - Add member to group
- `GET /groups/get-all-members-by-group-id/{group_id}` - Get all members of a group
- `DELETE /groups/delete-group/{group_id}` - Delete a group
- `DELETE /groups/delete-member-from-group/{group_id}/{member_id}` - Remove member from group
- `GET /groups/get-group-calulated-expances/{group_id}` - Get calculated expenses for a group

### Expense Endpoints (`/expances`)

- `POST /expances/create-expense` - Create a new expense
- `PUT /expances/edit-expense/{expense_id}` - Edit an expense
- `DELETE /expances/delete-expense/{expense_id}` - Delete an expense
- `GET /expances/get-expenses/{group_id}` - Get all expenses for a group
- `GET /expances/get-expense-by-id/{expense_id}` - Get expense by ID

### Activity Endpoints (`/activity`)

- `POST /activity/create` - Create an activity
- `GET /activity/get-activity-by-id/{activity_id}` - Get activity by ID
- `GET /activity/get-all-activities` - Get all activities
- `PUT /activity/update-activity/{activity_id}` - Update an activity
- `DELETE /activity/delete-activity/{activity_id}` - Delete an activity
- `GET /activity/get-activities-by-group-id/{group_id}` - Get activities by group
- `GET /activity/get-activities-by-user-id/{user_id}` - Get activities by user

### Connect Endpoints (`/connects`)

- `POST /connects/` - Create a connection
- `GET /connects/` - Get all connections for current user
- `GET /connects/{connect_id}` - Get connection by ID
- `DELETE /connects/{connect_id}` - Delete a connection

## Authentication

Most endpoints require authentication using JWT tokens. To authenticate:

1. **Login** to get a token:
   ```bash
   POST /users/login
   {
     "email": "user@example.com",
     "password": "password123"
   }
   ```

2. **Use the token** in subsequent requests:
   ```
   Authorization: Bearer <your_jwt_token>
   ```

## Database Models

- **User**: User accounts with email, password, name, phone
- **Group**: Expense groups with name and description
- **GroupMember**: Many-to-many relationship between users and groups
- **Expense**: Expenses with amount, description, payer, and group
- **Activity**: Activity logs for groups
- **Connect**: Connections between users

## Development

### Running in Development Mode

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Code Structure

- **Models** (`modal.py`): SQLAlchemy database models
- **Schemas** (`scheema.py`): Pydantic models for request/response validation
- **Services** (`service.py`): Business logic and database operations
- **Routes** (`routes.py`): FastAPI route handlers

## Dependencies

Key dependencies include:

- `fastapi` - Web framework
- `uvicorn[standard]` - ASGI server
- `sqlalchemy==2.0.20` - ORM
- `psycopg2-binary==2.9.7` - PostgreSQL adapter
- `pydantic==2.12.4` - Data validation
- `passlib[bcrypt]==1.7.3` - Password hashing
- `python-jose==3.3.0` - JWT handling

## Notes

- The database connection string in `src/database/db.py` contains credentials. In production, use environment variables for sensitive information.
- The application automatically creates database tables on startup via `Base.metadata.create_all(bind=engine)`
- Error handling and middleware are registered in `main.py`

## License

This project is for learning purposes.

## Contributing

Feel free to submit issues and enhancement requests!

