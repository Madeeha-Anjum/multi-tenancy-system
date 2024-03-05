# Postgres on GCP VM

## vm setup

- Create a vm instance in GCP

## Step1: GCP Setup

1. Install GCP cli tools: [here](https://cloud.google.com/sdk/docs/install)
2. Start the connection using the CLI `gcloud init`
3. ssh into the vm instance `gcloud compute ssh --zone "us-central1-a" "vm-1"`
   - if you have a default zone set you can omit the `--zone` flag

## Step2: SSH into the VM

- Add ssh to your own computer : `gcloud compute config-ssh`
  - this generates an ssh config and adds it to your ssh config file
  - Note: use SSH extension in vs code to open the ssh connection inside the editor

## Step3: Install Docker on the VM

- <https://docs.docker.com/desktop/install/debian/>
Note: curl -o <filename> <url> to download the official docker install script

## Install Postgres on the VM

1. Create ".env" file with the following variables inside the `_setup_guide` folder on the vm in the home directory
   - `DB_USER=postgres`
   - `DB_PASS=postgres`
   - `DB_NAME=postgres`
   - `PGADMIN_DEFAULT_EMAIL`
   - `PGADMIN_DEFAULT_PASSWORD`
2. Export the variables in the ".env" to the environment `export $( grep -v "^#" .env | xargs)`
3. Copy the `postgres_compose.yml` file from this folder to the vm inside "home/_setup_guide" folder
4. run the file containers `docker compose -f ./_setup_guide/postgres_compose.yml up` or use a .env file to run the containers `docker compose -f ./_setup_guide/postgres_compose.yml --env-file .env up`

## Expose the ports on the VM

1. (default exposed ports 80, 443)
   - port 80 is local and only runs on http
   - 433 is https

2. Open the external IP address of the VM in the browser in http
