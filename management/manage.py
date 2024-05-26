"""To run typer commands

$ python manage.py <command> <subcommand> <options>
    - command: name of the file in management/commands
    - subcommand: name of the function in the command file
    - options: arguments and flags for the subcommand
"""

# import importlib
# import os

# import typer

# app = typer.Typer()

# COMMANDS_MODULE = "management.commands"

# for file_name in os.listdir(COMMANDS_MODULE.replace(".", "/")):
#     if file_name.startswith("__"):
#         continue

#     # import each file as a module
#     module = importlib.import_module(f"{COMMANDS_MODULE}.{file_name[:-3]}")

#     # add the module as a subcommand to the app typer
#     app.add_typer(module.app, name=file_name[:-3])

# if __name__ == "__main__":
#     app()

import typer

app = typer.Typer()
