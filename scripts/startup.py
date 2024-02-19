# startup.py
from subprocess import Popen, PIPE
from main import tenant_create

# Define startup tasks
def startup_tasks():
    # Add your startup tasks here
    print("Running startup tasks...")

# Execute startup tasks
startup_tasks()
 
# Start a server using subprocess.Popen()
server_process = Popen(["uvicorn", "main:app", "--reload"], stdout=PIPE, stderr=PIPE)

# Define the data to be sent in the POST request
tenant_data = [{
    "name": "site1",
    "schema": "site1",
    "host": "site1.localhost:8000",
    "status": "active"
}]

for tenant in tenant_data:
    tenant_create(tenant.name, tenant.schema, tenant.host)

# Check the response status code
print("Tenant created successfully!")
print("Failed to create tenant.")


# The script will naturally reach its end and exit without waiting for user input
