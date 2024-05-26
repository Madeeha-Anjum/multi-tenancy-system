import typer

app = typer.Typer()


@app.command(name="create_tenant")
def create_tenant(tenant_schema_name: str, sub_domain: str):
    # Start the server subprocess
    # Perform any operations while the server is running
    # For example, you could wait for user input to stop the server
    from multi_tenancy_system.api.tenant import service

    service.create_tenant(
        tenant_schema_name=tenant_schema_name,
        sub_domain=sub_domain,
    )

    typer.echo("This is a tenant subcommand")


@app.command(name="test_basic")
def test_basic():
    typer.echo("This is a test subcommand")
