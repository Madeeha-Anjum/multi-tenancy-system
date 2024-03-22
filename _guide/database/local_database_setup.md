# Local database setup

1. Install Docker

2. Navigate to location of the postgres_compose.yml file create a .env file with the following content:

    ```bash
      DB_PASS=postgres
      DB_USER=postgres
      DB_NAME=postgres
      PGADMIN_DEFAULT_EMAIL=admin@gmail.com
      PGADMIN_DEFAULT_PASSWORD=password
    ```

3. Run the following command to start the database:

    ```bash
      docker-compose -f postgres_compose.yml --env-file .env up
    ```

4. open pgAdmin in your browser at `http://localhost` login with the credentials you provided in the .env file  PGADMIN_DEFAULT_EMAIL and PGADMIN_DEFAULT_PASSWORD

5. Add a new server `Register->Server" with the following details:

```bash
 +-------------------+  +-------------------+
 |                   |                      |
 |    General        |       Connection     |
 |   +-------------+ |   +-------------+    |
 |   |  Name       | |   |  Port       |    |
 +-------------------+   |  Hostname   |    |
                         |  Username   |    |
                         |  Password   |    |
                         +-------------+
```

- Name : myserver (or any name you prefer)
- Port: 5432
- Hostname/address: (DOCKER CONTAINER NAME OR IP ADDRESS)
- Maintenance database: postgres
- Username: postgres
- Password: postgres

**Note:** The DOCKER CONTAINER NAME can be found by running the following command:

```bash
docker ps or docker compose ls 
```
