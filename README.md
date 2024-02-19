# Multi Tenant System

In a multi-tenant system, there's one central software system, like a website, that serves multiple users or groups, also known as tenants. Each tenant, such as `company1.example.com` and `company2.example.com`, operates within this shared system.

Despite using the same website, each tenant is associated with its own schema and has its own separate area or "space" within the system where they store their data and settings. This ensures that the data and settings of one tenant are completely separate and inaccessible to other tenants.

## Installation

1. Clone the repository:

2. Create a virtual environment: (Optional but recommended)

    ```bash
    python3 -m venv .venv
    source .venv/Scripts/activate
    ```

3. Install dependencies using pip:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory and add the following environment variables:

    ```env
    ENVIRONMENT=development
    DB_USER=...
    DB_PASS=...
    DB_HOST=... 
    DB_PORT=...
    DB_NAME=...
    ```

    - check app.config.settings.py for more environment variables

5. Create a postgres database
   - Option1: Follow the steps in the `_setup_guide` folder to create a postgres database on Google Cloud Platform
   - Option2: Use the docker compose file in the `_setup_guide` folder to run the database locally
   - Option 3: Download postgres and pgAdmin and run the database locally

6. Run alembic migrations:

    ```bash
    alembic upgrade head
    ```

    see [Databases Information](./_setup_guide/database/database_structure.md) for more information on the database structure.

7. Load the initial data into the database: (optional)
   When the application is run for the first time, it will create the necessary tables in the database.
   However, if you want to load some initial data into the database, you can run the following command:

     ```bash
     python scripts/startup.py
     ```

## Usage

1. Run the FastAPI application:

    ```bash
    uvicorn main:app --reload
    ```

2. Access the interactive API documentation:
   - Open your browser and go to [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI.
   - Alternatively, access [http://localhost:8000/redoc](http://localhost:8000/redoc) for ReDoc.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
