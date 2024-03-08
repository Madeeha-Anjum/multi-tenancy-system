from subprocess import PIPE, Popen

import typer

app = typer.Typer()


@app.command(name="create_tenant")
def create_tenant(name: str, schema: str, host: str):
    # Start the server subprocess
    with Popen(["uvicorn", "main:app"], stdout=PIPE, stderr=PIPE) as server_process:
        try:
            # Perform any operations while the server is running
            # For example, you could wait for user input to stop the server
            from main import tenant_create

            tenant_create(name=name, schema=schema, host=host)

        finally:
            # Terminate the server subprocess
            server_process.terminate()

    typer.echo("This is a tenant subcommand")


@app.command(name="test_basic")
def test_basic():
    typer.echo("This is a test subcommand")
