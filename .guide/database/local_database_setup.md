# Local database setup

1. Install Docker

2. Navigate to location of the postgres_compose.yml file
3. Run the following command to start the database:

    ```bash
      docker-compose -f postgres_compose.yml --env-file ../../.env up
    ```

    **Note**: The --env-file flag is used to specify the location of the .env file. The path is relative to the location of the docker-compose file.
    **Note**: `-d` flag is used to run the container in detached mode.
    **Note**:  `docker-compose -f postgres_compose.yml --env-file ../../.env up config` will show you the configuration of the container before starting it.

4. open pgAdmin in your browser at [localhost](http://localhost) login with the credentials you provided in the .env file PGADMIN_DEFAULT_EMAIL and PGADMIN_DEFAULT_PASSWORD

5. Add a new server `Register->Server` with the following details:

- General/Name : myserver (or any name you prefer)
- Connection/Port: 5432 (from docker container)
- Connection/Hostname/address: **db** (DOCKER CONTAINER NAME OR IP ADDRESS)
- Connection/Maintenance database: postgres
- Connection/Username: postgres
- Connection/Password: postgres
