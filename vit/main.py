from typing import List
import typer
import os
from vit.commands.initialize import init_vit
from vit.commands.config import VIT_MAIN_FOLDER
from vit.commands.stage import stage_files, unstage_files
from vit.commands.commit import commit_files
from vit.commands.status import get_status
from vit.commands.history import get_history
from vit.commands.diff import get_diff
from vit.commands.reset import reset_files

app = typer.Typer()


@app.command()
def init():
    init_vit()
    typer.echo(f"Initialized empty Vit repository in {os.getcwd()}/{VIT_MAIN_FOLDER}/")


@app.command()
def stage(files: List[str]):
    stage_files(files)
    typer.echo(f"{len(files)} files added to staging area")


@app.command()
def unstage(files: List[str]):
    unstage_files(files)
    typer.echo(f"{len(files)} files removed from staging area")


@app.command()
def commit(msg: str):
    commit_files(msg)
    typer.echo(f"Commit created")


@app.command()
def history():
    typer.echo(get_history())


@app.command()
def diff(file: str):
    difference = get_diff(file)
    if difference:
        typer.echo(difference)
    else:
        typer.echo("No difference")


@app.command()
def reset(files: List[str]):
    reset_files(files)
    typer.echo(f"Files reset")


@app.command()
def status():
    status = get_status()
    files_to_be_committed = "\n  ".join(status.staged_files)
    unstaged_files = "\n  ".join(status.unstaged_files)
    modified_files = "\n  ".join(status.modified_files)

    if files_to_be_committed:
        typer.echo(
            f"""
On branch {status.branch}

Files to be committed:
  {files_to_be_committed}

Modified files:
  {modified_files}

Unstaged files:
  {unstaged_files}
""".strip()
        )
    else:
        typer.echo(
            f"""
On branch {status.branch}

Nothing to be committed

Modified files:
  {modified_files}

Unstaged files:
  {unstaged_files}
""".strip()
        )


if __name__ == "__main__":
    app()
