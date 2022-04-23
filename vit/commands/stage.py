from typing import List
import sysrsync
import typer
import os

from vit.commands.config import VIT_STAGING_FOLDER


def stage_files(files: List[str]):
    with typer.progressbar(files, label="Staging files...") as progress:
        for file in progress:
            sysrsync.run(source=file, destination=VIT_STAGING_FOLDER)


def unstage_files(files: List[str]):
    with typer.progressbar(files, label="Unstaging files...") as progress:
        for file in progress:
            os.remove(f"{VIT_STAGING_FOLDER}/{file}")
