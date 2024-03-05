# HOw to use alembic

## How dose Alembic work

Alembic creates a table in the database to keep track of the migration history. This table is called `alembic_version` and it contains a single column called `version_num` which stores the version number of the migration that has been applied to the database.

Each migration has a unique version number that is that is database to find the migration that has been applied to the database.

## Available commands

1. `alembic stamp head`
   - If the migration table is not present in the database, this command will create it. If the migration table is present, this command will update the version number in the migration table to the latest version available in the migration scripts on your filesystem.
   - This command is useful when you want to pull the latest migration from the database to your filesystem.

2. `alembic revision --autogenerate -m "message"`
    This command generates a new migration script automatically based on the changes detected in the database schema, and the -m flag allows you to provide a brief message describing the changes.
3. `alembic downgrade base && alembic upgrade head alembic upgrade head`
    - This command applies all the migrations that have not been applied to the database yet.
    - This command is useful when you want to run all the migrations on a new database.
  
4. `a1alembic downgrade -1`
    - This command rolls back the most recent migration applied to the database.

5. `alembic downgrade base`
    - This command rolls back all the migrations applied to the database

6. `alembic current`
    - This command shows the current revision of the database`

7. `alembic history`
    - This command shows the history of migrations that have been applied to the database.
8. `alembic history --verbose`
    - This command shows the history of migrations in a more detailed way.
9. `alembic show`
    - This command shows the current revision of the database and the latest revision available in the migration scripts on your filesystem.
