# Multi-Tenant System with FastAPI and Postgres :rocket:

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/) [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/) [![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-282C34?style=flat&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/) [![Alembic](https://img.shields.io/badge/Alembic-4E98E8?style=flat&logo=alembic&logoColor=white)](https://alembic.sqlalchemy.org/en/latest/) [![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/) [![Docker Compose](https://img.shields.io/badge/Docker_Compose-2496ED?style=flat&logo=docker&logoColor=white)](https://docs.docker.com/compose/) [![Google Cloud Platform](https://img.shields.io/badge/Google_Cloud_Platform-4285F4?style=flat&logo=google-cloud&logoColor=white)](https://cloud.google.com/) [![Pydantic](https://img.shields.io/badge/Pydantic-2B7DBC?style=flat&logo=python&logoColor=white)](https://pydantic-docs.helpmanual.io/) [![Uvicorn](https://img.shields.io/badge/Uvicorn-2B7DBC?style=flat&logo=python&logoColor=white)](https://www.uvicorn.org/) [![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=flat&logo=pytest&logoColor=white)](https://docs.pytest.org/en/6.2.x/) [![Git](https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white)](https://git-scm.com/) [![VSCode](https://img.shields.io/badge/VSCode-007ACC?style=flat&logo=visual-studio-code&logoColor=white)](https://code.visualstudio.com/) [![Swagger UI](https://img.shields.io/badge/Swagger_UI-85EA2D?style=flat&logo=swagger&logoColor=black)](https://swagger.io/tools/swagger-ui/) [![Markdown](https://img.shields.io/badge/Markdown-000000?style=flat&logo=markdown&logoColor=white)](https://www.markdownguide.org/)

**A Scalable Web Application with Efficient Database Management**

In a multi-tenant system, there's one central software system, like a website, that serves multiple users or groups, also known as tenants. Each tenant, such as `company1.example.com` and `company2.example.com`, operates within this shared system.

Despite using the same website, each tenant is associated with its own schema and has its own separate area or "space" within the system where they store their data and settings. This ensures that the data and settings of one tenant are completely separate and inaccessible to other tenants.

## Installation :wrench:

### Pre-requisites :clipboard:

1. Clone the repository

2. Create a virtual environment

    ```bash
    python3 -m venv .venv
    source .venv/Scripts/activate
    ```

3. Install [PDM](https://pdm.fming.dev/) (Python Development Master) package manager:

    ```bash
        pip install pdm
    ```

    - PDM is a modern Python package manager with a focus on simplicity and ease of use. It allows you to specify dependencies in a `pyproject.toml` file and install them using a lock file.

4. Install dependencies using pdm:

    ```bash
    pdm install
    ```

5. Create a `.env` file in the root directory and add the following environment variables:

    ```env
    ENVIRONMENT=development
    DB_USER=...
    DB_PASS=...
    DB_HOST=... 
    DB_PORT=...
    DB_NAME=...
    PGADMIN_DEFAULT_EMAIL=madee@admin.com   
    PGADMIN_DEFAULT_PASSWORD=AmazingPassword
    ```

    - check app.config.settings.py for more environment variables

6. Create a postgres database
   - Follow the steps in the `_guide/database` folder to create a postgres database on Google Cloud Platform or locally using Docker.

7. Run alembic migrations:

    ```bash
    alembic upgrade head
    ```

    See [Databases Information](./_setup_guide/database/database_structure.md) for more information on the database structure.

8. Run management commands to create your first tenants:
    For example, to create a tenant with the name `company1` and the domain `company1.example.com`, run the following command:

    ```bash
        python manage.py tenant create_tenant company1 company1 company1.localhost 
    ```

    **Tips:**
    `python manage.py --help` for more information on the management commands available

## Running the Application :running:

1. Run the FastAPI application using the following 2 options:

   ```bash
       uvicorn main:app --reload 
   ```

   ````bash
       pdm run start`
   ````

2. Access the interactive API documentation:
   - Open your browser and go to [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI.
   - Alternatively, access [http://localhost:8000/redoc](http://localhost:8000/redoc) for ReDoc.

<!-- 
TODO: possible seed file for initial data
1. Load the initial data into the database: (optional)
   - When the application is run for the first time, it will create the necessary tables in the database.
   However, if you want to load some initial data into the tables, you can run the following file using the command below:

    -->

<!-- ## Testing :white_check_mark: -->

## Tools and Technologies :hammer_and_wrench:

- [FastAPI](https://fastapi.tiangolo.com/)
- [Typer](https://typer.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Google Cloud Platform](https://cloud.google.com/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [Uvicorn](https://www.uvicorn.org/)
- [Pytest](https://docs.pytest.org/en/6.2.x/)
- [Git](https://git-scm.com/)
- [VSCode](https://code.visualstudio.com/)
- [Swagger UI](https://swagger.io/tools/swagger-ui/)
- [Markdown](https://www.markdownguide.org/)

## License :page_facing_up:

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
