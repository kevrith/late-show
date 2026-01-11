# Late Show API

A Flask REST API for managing episodes, guests, and appearances on a late-night talk show. This API provides endpoints to track which guests appeared on which episodes, along with ratings for each appearance.

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Data Model](#data-model)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Testing with Postman](#testing-with-postman)
- [Project Structure](#project-structure)
- [Validations](#validations)
- [Contributing](#contributing)

## Features

- View all episodes with basic information
- View detailed episode information including guest appearances
- View all guests
- Create new appearance records linking guests to episodes
- Data validation for appearance ratings (1-5 scale)
- Cascade delete functionality for appearances
- RESTful API design with proper HTTP status codes
- Comprehensive error handling

## Technology Stack

- **Python 3.12+**
- **Flask** - Web framework
- **Flask-SQLAlchemy** - ORM for database operations
- **Flask-Migrate** - Database migration management
- **Flask-RESTful** - REST API framework
- **SQLAlchemy-serializer** - Model serialization
- **SQLite** - Database (development)

## Data Model

The application implements a many-to-many relationship between Episodes and Guests through Appearances:

```
Episode (1) ----< Appearance >---- (1) Guest
```

### Models

**Episode**
- `id` (Primary Key)
- `date` (String)
- `number` (Integer)
- Relationship: has many `appearances`

**Guest**
- `id` (Primary Key)
- `name` (String)
- `occupation` (String)
- Relationship: has many `appearances`

**Appearance**
- `id` (Primary Key)
- `rating` (Integer, 1-5)
- `episode_id` (Foreign Key → episodes.id)
- `guest_id` (Foreign Key → guests.id)
- Relationships: belongs to `episode` and `guest`

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Postman (for API testing - optional)

### Setup Steps

1. Clone the repository:
```bash
git clone <repository-url>
cd late-show
```

2. Create a virtual environment:
```bash
python3 -m venv venv
```

3. Activate the virtual environment:
```bash
# On Linux/Mac
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Database Setup

1. Initialize the database:
```bash
flask db init
```

2. Create the initial migration:
```bash
flask db migrate -m "Initial migration"
```

3. Apply the migration:
```bash
flask db upgrade
```

4. Seed the database with sample data:
```bash
python seed.py
```

The seed script will populate the database with:
- 5 episodes
- 5 guests
- 10 appearances (from `data.csv`)

## Running the Application

Start the Flask development server:

```bash
python app.py
```

The API will be available at `http://localhost:5555`

To verify the server is running, visit `http://localhost:5555` in your browser.

## API Endpoints

### 1. GET /episodes

Returns a list of all episodes.

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "date": "1/11/99",
    "number": 1
  },
  {
    "id": 2,
    "date": "1/12/99",
    "number": 2
  }
]
```

### 2. GET /episodes/:id

Returns detailed information about a specific episode, including all appearances.

**Response** (200 OK):
```json
{
  "id": 1,
  "date": "1/11/99",
  "number": 1,
  "appearances": [
    {
      "id": 1,
      "episode_id": 1,
      "guest_id": 1,
      "rating": 4,
      "guest": {
        "id": 1,
        "name": "Michael J. Fox",
        "occupation": "actor"
      }
    }
  ]
}
```

**Response** (404 Not Found):
```json
{
  "error": "Episode not found"
}
```

### 3. GET /guests

Returns a list of all guests.

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "name": "Michael J. Fox",
    "occupation": "actor"
  },
  {
    "id": 2,
    "name": "Sandra Bernhard",
    "occupation": "Comedian"
  }
]
```

### 4. POST /appearances

Creates a new appearance linking a guest to an episode.

**Request Body**:
```json
{
  "rating": 5,
  "episode_id": 2,
  "guest_id": 3
}
```

**Response** (201 Created):
```json
{
  "id": 11,
  "rating": 5,
  "guest_id": 3,
  "episode_id": 2,
  "episode": {
    "id": 2,
    "date": "1/12/99",
    "number": 2
  },
  "guest": {
    "id": 3,
    "name": "Tracey Ullman",
    "occupation": "television actress"
  }
}
```

**Response** (400 Bad Request):
```json
{
  "errors": ["Rating must be between 1 and 5"]
}
```

## Testing with Postman

### Importing the Collection

1. Open Postman
2. Click **Import** in the top left
3. Select **Upload Files**
4. Navigate to the project directory
5. Select `challenge-4-lateshow.postman_collection.json`
6. Click **Import**

### Running Tests

The Postman collection includes:
- GET all episodes
- GET specific episode
- GET non-existent episode (404 test)
- GET all guests
- POST valid appearance
- POST invalid appearance (rating < 1)
- POST invalid appearance (rating > 5)

Each request includes automated tests that verify:
- Correct HTTP status codes
- Response data structure
- Expected field values

## Project Structure

```
late-show/
├── app.py                    # Main application file with routes
├── models.py                 # Database models
├── seed.py                   # Database seeding script
├── data.csv                  # CSV file with appearance data
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── challenge-4-lateshow.postman_collection.json  # Postman tests
├── instance/
│   └── app.db               # SQLite database (created after migration)
├── migrations/              # Database migration files
└── venv/                    # Virtual environment (not in git)
```

## Validations

### Appearance Model

The `Appearance` model includes validation for the `rating` field:

- **Required**: Rating must be provided
- **Type**: Must be an integer
- **Range**: Must be between 1 and 5 (inclusive)

Invalid ratings will return a 400 Bad Request response with an error message.

### Cascade Delete

When an `Episode` or `Guest` is deleted, all associated `Appearance` records are automatically deleted to maintain referential integrity.

### Serialization Rules

Serialization rules prevent infinite recursion when converting models to dictionaries:
- `Episode`: Excludes nested `appearances.episode`
- `Guest`: Excludes nested `appearances.guest`
- `Appearance`: Excludes nested `episode.appearances` and `guest.appearances`

## API Design Principles

This API follows REST conventions:

- **Resource-based URLs**: `/episodes`, `/guests`, `/appearances`
- **HTTP verbs**: GET for retrieval, POST for creation
- **Status codes**:
  - 200 OK for successful GET
  - 201 Created for successful POST
  - 400 Bad Request for validation errors
  - 404 Not Found for missing resources
- **JSON format**: All requests and responses use JSON
- **Error handling**: Consistent error response format

## Development

### Making Changes

1. Create a new branch for your feature
2. Make your changes
3. Test using Postman or curl
4. Commit with descriptive messages
5. Push and create a pull request

### Database Migrations

When modifying models:

```bash
# Create migration
flask db migrate -m "Description of changes"

# Apply migration
flask db upgrade

# Rollback if needed
flask db downgrade
```

### Resetting the Database

To start fresh:

```bash
# Delete the database
rm instance/app.db

# Recreate and seed
flask db upgrade
python seed.py
```

## Troubleshooting

**Issue**: `ModuleNotFoundError` when running the app

**Solution**: Ensure virtual environment is activated and dependencies are installed:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**Issue**: Database errors after model changes

**Solution**: Create and apply a new migration:
```bash
flask db migrate -m "Update models"
flask db upgrade
```

**Issue**: Port 5555 already in use

**Solution**: Change the port in [app.py:93](app.py#L93):
```python
app.run(port=5556, debug=True)  # Use a different port
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Ensure all tests pass
6. Submit a pull request

## License

This project is created for educational purposes as part of a coding challenge.

## Author

Created as part of Phase 4 Flask API development challenge.

## Acknowledgments

- Flask documentation
- SQLAlchemy documentation
- Postman for API testing tools
