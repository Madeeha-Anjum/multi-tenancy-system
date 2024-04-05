# Multi-Tenant System with FastAPI and Postgres :rocket:

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/) [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/) [![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-282C34?style=flat&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/) [![Alembic](https://img.shields.io/badge/Alembic-4E98E8?style=flat&logo=alembic&logoColor=white)](https://alembic.sqlalchemy.org/en/latest/) [![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/) [![Docker Compose](https://img.shields.io/badge/Docker_Compose-2496ED?style=flat&logo=docker&logoColor=white)](https://docs.docker.com/compose/) [![Google Cloud Platform](https://img.shields.io/badge/Google_Cloud_Platform-4285F4?style=flat&logo=google-cloud&logoColor=white)](https://cloud.google.com/) [![Pydantic](https://img.shields.io/badge/Pydantic-2B7DBC?style=flat&logo=python&logoColor=white)](https://pydantic-docs.helpmanual.io/) [![Uvicorn](https://img.shields.io/badge/Uvicorn-2B7DBC?style=flat&logo=python&logoColor=white)](https://www.uvicorn.org/) [![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=flat&logo=pytest&logoColor=white)](https://docs.pytest.org/en/6.2.x/) [![Git](https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white)](https://git-scm.com/) [![VSCode](https://img.shields.io/badge/VSCode-007ACC?style=flat&logo=visual-studio-code&logoColor=white)](https://code.visualstudio.com/) [![Swagger UI](https://img.shields.io/badge/Swagger_UI-85EA2D?style=flat&logo=swagger&logoColor=black)](https://swagger.io/tools/swagger-ui/) [![Markdown](https://img.shields.io/badge/Markdown-000000?style=flat&logo=markdown&logoColor=white)](https://www.markdownguide.org/)

> A Scalable Web Application with Efficient Database Management

A website, that serves multiple users or groups, also known as tenants.Each tenant `company1.example.com`  has its own database schema.
Fork this repository to get started with a multi-tenant system using **FastAPI**, **PostgreSQL**, **Alembic**, **Docker**, **Ruff**, **Pdm**, **Typer**, and more.

## Installation

## Pre-requisites :clipboard:

1. Clone the repository

2. Install [PDM](https://pdm.fming.dev/) (Python Development Master) package manager:

   ```bash
   pip install pdm --user
   ```

3. Create and activate the virtual environment

    ```bash
    pdm venv create --with venv
    ```

    ```bash
      pdm use
      ```

      ```bash
      eval $(pdm venv activate )
      ```

## Getting Started :wrench:

### Install python dependencies

- May need to upgrade: `rustup default nightly && rustup update`

   ```bash
      pdm install --no-self 
   ```

### Setup `.env` file

Create a `.env` file in the root directory and add the following environment variables:

```env
ENVIRONMENT=development

DB_NAME=db_name
DB_USER=user
DB_PASS=root
DB_PORT=5432
DB_HOST=localhost 

PGADMIN_DEFAULT_EMAIL=user@user.com
PGADMIN_DEFAULT_PASSWORD=password
```

### Setup Local Postgres Database

- Alternatively you can setup a GCP database following the instructions in [.guide/gcp_database]

1. Start postgres database in docker

   ```bash
   docker-compose -f .local_database/postgres_compose.yml --env-file .env up
   ```

2. Login to PG Admin
   - open [localhost](http://localhost)
   - login with the credentials you provided in the `.env` file
     - `PGADMIN_DEFAULT_EMAIL`
     - `PGADMIN_DEFAULT_PASSWORD`

3. Setup PGAdmin Access to database

   Add a new server `Register->Server` with the following details:

   ```yaml
   General:
        # or any name you prefer
        Name : myserver 
   Connection:
        # as configured in .local_database/postgres_compose.yml
        Port: 5432 (from docker container)
        Hostname/address: db 
        Username: postgres
        Password: postgres
   ```

### Run  Alembic Migrations to create Database schemas and tables

1. Run alembic migrations:

    ```bash
    alembic upgrade head
    ```

### Create Tenants in the Database

1. Run management command  
    - `python manage.py --help` for more information

    ```bash
    python manage.py tenant create_tenant company1 company1 company1.localhost 
    ```

## Running the Application :running:

1. Run the application

   ````bash
   pdm run start
   # equivalent to: uvicorn main:app --reload 
   ````

2. Access the interactive API documentation:
   - Open your browser and go to <http://localhost:8000/docs> for Swagger UI.
   - Alternatively, access <http://localhost:8000/redoc> for ReDoc.

## Tools and Technologies :hammer_and_wrench:

- [PDM](https://pdm.fming.dev/)
  - PDM is a modern Python package manager with a focus on simplicity and ease of use. It allows you to specify dependencies in a `pyproject.toml` file and install them using a lock file.
  - `pdm use` to select the venv
  - add package in pyproject.toml file `pdm add package_name`
  - add package to dev dependencies `pdm add package_name --dev`
- [FastAPI](https://fastapi.tiangolo.com/)
- [Typer](https://typer.tiangolo.com/)

- [PostgreSQL](https://www.postgresql.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
  - See [.guide/alembic_commands.md](./.guide/alembic_commands.md) for more information on how to use Alembic.
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
