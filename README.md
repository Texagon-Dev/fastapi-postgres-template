# FastAPI Postgres Template

This is a template project for a FastAPI application with a PostgreSQL database, pgAdmin for database management, and Traefik as a reverse proxy. All services are containerized using Docker.

## Features

- **FastAPI Backend**: High-performance API framework
- **PostgreSQL Database**: Robust relational database
- **Alembic Migrations**: Database versioning and migrations
- **Docker & Docker Compose**: Containerization for consistent environments
- **pgAdmin**: Database management UI
- **Traefik**: API Gateway and reverse proxy
- **Authentication**:
  - JWT Token-based authentication (Bearer tokens)
  - Cookie-based authentication with HTTP-only cookies
  - Refresh token functionality
  - Password reset functionality
- **Environment-based configuration**: Different settings for development, staging, and production

## Getting Started

### Prerequisites

- **Python 3.11+** and pip/uv
- **PostgreSQL** (local or remote)
- **Git** for version control
- **Docker & Docker Compose** (for containerized development)
- **Terminal/Command Prompt** (PowerShell recommended for Windows)

### Quick Start

**Clone the repository**:
   ```bash
   git clone https://github.com/Texagon-Dev/fastapi-postgres-template your-project-name
   cd your-project-name
   git remote set-url origin <your-project-repo-url>
   ```

### Development Setup

### Option 1: Automated Setup (Recommended)
We provide a setup script to help you get started quickly. Choose the appropriate command for your operating system:

#### Mac/Linux:
```bash
# Make the script executable
chmod +x scripts/dev_setup.py

# Run the setup script
./scripts/dev_setup.py
```

#### Windows (Command Prompt):
```cmd
# Run the setup script directly with Python
python scripts/dev_setup.py
```

#### Windows (PowerShell):
```powershell
# Run the setup script directly with Python
python .\scripts\dev_setup.py
```

### Option 2: Manual Setup
**The setup script will**:
- Create a `.env` file from the example
- Set up git hooks
- Install pre-commit hooks

    2. **Set up environment**:
   - Copy the example environment file:
     ```bash
     # Linux/macOS
     cp .example.env .env
     
     # Windows (Command Prompt)
     copy .example.env .env
     
     # Windows (PowerShell)
     Copy-Item -Path .example.env -Destination .env
     ```
   - Update the `.env` file with your configuration (see Configuration section below)

    ### Configuration

    - Edit the `.env` file with your settings:

    ```env
    # Core settings
    FRONTEND_URL='http://localhost:3000'
    SECRET_KEY='your_32_char_strong_secret_key_here'
    DEBUG=True
    ENVIRONMENT='development'  # Options: development, staging, production

    # Database settings
    POSTGRES_USER="your_username"
    POSTGRES_PASSWORD="your_password"
    POSTGRES_DB_NAME="fastapi_db"

    # Authentication
    ALGORITHM='HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES=30  # Short-lived access tokens for security
    REFRESH_TOKEN_EXPIRE_DAYS=7     # Longer-lived refresh tokens
    ```

    3. **Install dependencies** (using uv - recommended):
   ```bash
   # Install dependencies and create virtual environment
   uv sync
   
   # Activate virtual environment
   # Linux/macOS:
   source .venv/bin/activate
   # Windows (Command Prompt):
   .venv\Scripts\activate
   # Windows (PowerShell):
   .\.venv\Scripts\Activate.ps1
   ```

    4. **Set up the database**:
   ```bash
   # Run migrations
   uv run alembic upgrade head
   
   # Or using make (if available)
   make alembic-upgrade
   ```

   5. **Set up pre-commit hooks**:
   ```bash
   # Linux/macOS/Windows (Git Bash)
   cp misc/pre-commit .git/hooks/pre-commit
   chmod +x .git/hooks/pre-commit
   
   # Windows (Command Prompt)
   copy /Y misc\pre-commit .git\hooks\pre-commit
   ```

    6. **Start the development server**:
    ```bash
    # Using uvicorn directly
    uv run uvicorn app.main:app --reload
    
    # Or using make (if available)
    make start
    ```
    The API will be available at `http://localhost:8000` and interactive docs at `http://localhost:8000/docs`


### Database Migrations Guide

This project uses Alembic for managing database schema migrations. Understanding the migration workflow is essential for all developers working on this project.

#### How Migrations Work

1. **Migration Tracking:**
   - Alembic maintains a version table (`alembic_version`) in your database
   - This table stores the current revision ID that has been applied
   - Each migration has a unique revision ID (e.g., `9ead825737b6`)

2. **Creating New Migrations:**

   When you modify SQLAlchemy models (e.g., add/change/remove columns), you need to create and apply migrations:

   ```bash
   # Generate a migration automatically by detecting model changes
   uv run alembic revision --autogenerate -m "Add new user table"

   # or with make
   make alembic-revision MSG="Add new user table"

   # Review the generated migration file in app/alembic/versions/
   # Make any necessary adjustments (e.g., adding default values for non-nullable columns)

   # Apply the migration
   uv run alembic upgrade head
   ```

3. **Common Migration Tasks:**

   ```bash
   # View current migration status
   uv run alembic current

   # View migration history
   uv run alembic history

   # Downgrade to a specific version
  uv run  alembic downgrade <revision_id>

   # Downgrade one version
   uv run alembic downgrade -1
   ```

4. **Important Considerations:**

   - **Adding Non-Nullable Columns:** When adding non-nullable columns to existing tables, you MUST provide a server_default value
   - **JSONB Columns:** Require the PostgreSQL dialect to be properly imported and used
   - **Data Migrations:** For complex data transformations, you may need to write custom Python in your migration scripts
   - **Testing Migrations:** Always test migrations in a development environment before applying to production

5. **Troubleshooting Migration Issues:**

   - If a migration fails, check the error message carefully - common issues include constraint violations or missing dependencies
   - If you need to reset a failed migration, you may need to modify the `alembic_version` table directly
   - When working with existing data, consider data integrity and constraints

4. **Run the application**:

   ```bash
   uv run uvicorn app.main:app --reload
   ```

   The API will be available at http://localhost:8000

## Docker Build and Run

To build and start all the services (FastAPI application, PostgreSQL database, pgAdmin, and Traefik):

```bash
docker compose up --build -d
```

*   `--build`: Forces Docker to rebuild the images if there are changes (e.g., in your `Dockerfile` or application code).
*   `-d`: Runs the containers in detached mode (in the background).

To stop the services:

```bash
docker compose down
```

To stop and remove volumes (useful for a clean restart, **will delete database data**):

```bash
docker compose down -v
```

To view logs for all services:
```bash
docker compose logs -f
```
To view logs for a specific service (e.g., `fastapi`):
```bash
docker compose logs -f fastapi
```

## Accessing Services

Once the containers are running:

*   **Backend API (FastAPI)**:
    *   Via Traefik: `http://api.localhost`
    *   Directly (if Traefik is not used or for direct port access): `http://localhost:8000`
    *   API Docs (Swagger UI): `http://api.localhost/docs` or `http://localhost:8000/docs`
    *   Alternative API Docs (ReDoc): `http://api.localhost/redoc` or `http://localhost:8000/redoc`

*   **pgAdmin (Database Management)**:
    *   Via Traefik: `http://pgadmin.localhost`
    *   Directly: `http://localhost:9000`
    *   **Login Credentials** (defined in `docker-compose.yml`):
        *   Email: `admin@admin.com`
        *   Password: `admin`

*   **Traefik Dashboard** (for inspecting routes and services):
    *   `http://localhost:8080`

## Authentication

This application supports two authentication methods:

### 1. Bearer Token Authentication (Standard OAuth2)

- **Login**: Send a POST request to `/api/auth/token` with username/password to get an access token
- **Usage**: Include the token in the Authorization header: `Authorization: Bearer <your_token>`
- **API Docs**: Works with Swagger UI's "Authorize" button

### 2. Cookie-Based Authentication

- **Login**: Send a POST request to `/api/auth/login` with username/password
- **Security**: Tokens are stored in HTTP-only cookies for protection against XSS attacks
- **Refresh**: When the access token expires, use `/api/auth/refresh` to get a new one
- **Logout**: Send a POST request to `/api/auth/logout` to clear authentication cookies

### Environment-Based Security

Cookie security settings are automatically configured based on the `ENVIRONMENT` variable:

- **Development**: Less restrictive settings (HTTP allowed, lax same-site policy)
- **Staging**: HTTPS required, lax same-site policy
- **Production**: HTTPS required, strict same-site policy

## pgAdmin: Connecting to the PostgreSQL Database

After logging into pgAdmin, you'll need to register your PostgreSQL server (the `db` service from `docker-compose.yml`):

1.  In the pgAdmin browser tree (left panel), right-click on **Servers**.
2.  Select **Register** -> **Server...**.
3.  In the **General** tab:
    *   **Name**: Enter a descriptive name for your server (e.g., `Local Docker DB`, `fastapi_db_service`).
4.  Switch to the **Connection** tab:
    *   **Host name/address**: `db` (This is the service name of your PostgreSQL container in `docker-compose.yml`).
    *   **Port**: `5432` (Default PostgreSQL port).
    *   **Maintenance database**: `fastapi_db` (This is the `POSTGRES_DB` value from your `db` service environment).
    *   **Username**: `texagon` (This is the `POSTGRES_USER` value).
    *   **Password**: `password` (This is the `POSTGRES_PASSWORD` value).
    *   You can leave other settings as default or adjust as needed.
5.  Click **Save**.

Your database server should now appear in the list, and you can browse its contents, run queries, etc.


## Use of Pagination
```python
#service.py
from app.utils.pagination import paginator
@paginator(UserSchema)
async def get_users_service(
    db: Session,
    current_user: CurrentUser,
    start_date: date = None,
    end_date: date = None,
    page: int = 1,
    page_size: int = 10,
):
    query = db.query(UserModel)
    if start_date:
        query = query.filter(UserModel.created_at >= start_date)
    if end_date:
        query = query.filter(UserModel.created_at <= end_date)
    return query


#router.py
from .service import users_service
from app.schema.pagination import PaginationResponseSchema

@router.get(
    "/users",
    response_model=PaginationResponseSchema[UserSchema],
    status_code=status.HTTP_200_OK,
)
async def get_users(
    request: Request,
    current_user: CurrentUser,
    db_session: DbSession,
    start_date: date = None,
    end_date: date = None,
    page: int = 1,
    per_page: int = 10,
):
    users = await get_users_service(
        db_session, current_user, start_date, end_date, page, per_page
    )
    return users

```

## Pre-commit Hooks
This project uses pre-commit to automatically check and format code before each commit.
Pre-commit hooks help enforce code style, catch errors early, and keep your codebase clean.

### Install the hooks
 ```
uv run pre-commit install
 ```
### Update the hooks
 ```
uv run pre-commit autoupdate
 ```
### Run all hooks manually (recommended before your first commit):
```
uv run pre-commit run --all-files
```
### What gets checked?
    Code formatting: black, autopep8, isort
    Linting: flake8, bandit, autoflake
    YAML and whitespace checks
    Security checks: bandit
### Troubleshooting
If you add new hooks or update .pre-commit-config.yaml, run:
```
uv run pre-commit install
uv run pre-commit autoupdate
```
To clear the pre-commit cache (if you see strange errors):
```
uv run pre-commit clean
```

### Lint, Format & Start (Development)

This repo includes Make targets to run linting, formatting, and start the dev server. You can use the Makefile targets or run the underlying commands directly with `uv`.

- Run linter (ruff):
```bash
make lint
# or
uv run ruff check ./app
```

- Format code (ruff):
```bash
make format
# or
uv run ruff format ./app
```

- Start development server (uvicorn with auto-reload):
```bash
make start
# or
uv run uvicorn app.main:app --reload
```

Notes:
- `uv` will create/manage the virtual environment for you if you use it.
- If you don't have `make` available, use the `uv run ...` commands shown above.
- Run `pre-commit run --all-files` to apply all pre-commit checks and auto-fixes before committing.


## Cache Management
```python
from app.utils.cache import cache_response, invalidate_cache_key


@router.get("/items")
@cache_response(ttl=15, key="items") #ttl is time to live in seconds
async def get_items():
    items = await fetch_items_from_db()  # Replace with actual DB fetch logic
    return items

# invalidate cache for items
@router.post("/add-items")
async def add_item(item):
    item = await add_item_to_db(item)  # Replace with actual DB insert logic
    # Invalidate the cache for items
    await invalidate_cache_key("items")
    return {"message": "Items added to cache"}

```


## Project Structure (Brief Overview)

```
.
app/
├── features/
│   └── auth/
│       ├── router.py          # REST API endpoints
│       ├── service.py         # Business logic
│       ├── schema.py          # Pydantic models
│       └── graphql/
│           ├── types/ # GraphQL types
│           ├── queries/ # GraphQL queries
│           └── mutations/ # GraphQL mutations
├── models/
│   ├── user.py               # SQLAlchemy models
│   └── deal.py               # Deal model
├── utils/
│   ├── dependencies.py      # Common dependencies
│   ├── security.py          # Password & JWT utilities
│   ├── permissions.py       # Role-based access control
│   ├── database.py              # Database configuration
│   ├── config.py                # Application settings
│   ├── api.py               # Regiseter api routes
│   └── exception_handler.py # Custom error handlers
├── graphql/
│   ├── schema.py            # Main GraphQL schema
│   └── context.py           # GraphQL context
├── alembic/                 # Database migrations
├── main.py                  # FastAPI application
├── alembic/              # Alembic database migration scripts
├── tests/                # Unit and integration tests
├── .env                  # Local environment variables (create this file)
├── .gitignore
├── alembic.ini           # Alembic configuration
├── docker-compose.yml    # Docker Compose configuration
├── Dockerfile            # Dockerfile for the FastAPI application
├── entrypoint.sh         # Entrypoint script for the FastAPI container
├── pyproject.toml        # Project metadata and dependencies (using Poetry/uv)
├── README.md             # This file
└── uv.lock               # Lock file for dependencies managed by uv
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**:
   - Check if PostgreSQL is running
   - Verify your DATABASE_URL in the .env file
   - Ensure your PostgreSQL user has proper permissions

2. **Authentication Issues**:
   - Make sure SECRET_KEY is set correctly
   - Check that COOKIE_SECURE is False in development if not using HTTPS

3. **Alembic Migration Errors**:
   - Run `alembic revision --autogenerate -m "message"` to create a new migration
   - Check your database models for any issues


### Getting Help

If you encounter issues not covered here, please check the FastAPI documentation or create an issue in the repository.

Happy coding!
