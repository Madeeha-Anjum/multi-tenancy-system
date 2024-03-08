import importlib
import os

import typer

app = typer.Typer()

parent_folder = "management"
sub_folder = "commands"
path = os.path.join(parent_folder, sub_folder)

for file_name in os.listdir(path):
    if file_name.startswith("__"):
        continue

    module = importlib.import_module(f"{parent_folder}.{sub_folder}.{file_name[:-3]}")

    app.add_typer(module.app, name=file_name[:-3])

if __name__ == "__main__":
    app()
