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
from vit.commands.travel import travel_to

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
    history_str = get_history()
    if history_str:
        typer.echo(history_str)
    else:
        typer.echo("No commits")


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
def travel(commit_id: str):
    travel_to(commit_id)


@app.command()
def status():
    status = get_status()
    current_commit_id = status.current_commit_id
    last_commit_id = status.last_commit_id

    files_to_be_committed = "\n  ".join(status.staged_files)
    untracked_files = "\n  ".join(status.untracked_files)
    modified_files = "\n  ".join(status.modified_files)

    commit_id_message = (
        f"\nYou're in the past (at commit {current_commit_id})\nChanges are compared to the last commit {last_commit_id}"
        if status.in_the_past
        else f"\nLast commit is {last_commit_id}"
    )

    modified_files_message = (
        typer.style(
            f"""
\nModified files:
  {modified_files}""",
            fg=typer.colors.RED,
        ).strip()
        if modified_files
        else ""
    )

    files_to_be_committed_message = (
        typer.style(
            f"""
\nFiles to be committed:
  {files_to_be_committed}""",
            fg=typer.colors.GREEN,
        ).strip()
        if files_to_be_committed
        else ""
    )

    untracked_files_message = (
        typer.style(
            f"""
\nUntracked files:
  {untracked_files}""",
            fg=typer.colors.CYAN,
        ).strip()
        if untracked_files
        else ""
    )

    typer.echo(
        f"""
On branch {status.branch}\n{commit_id_message}{files_to_be_committed_message}{modified_files_message}{untracked_files_message}
""".strip()
    )


if __name__ == "__main__":
    app()
