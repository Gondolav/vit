import os
import shutil
from typing import List
import sysrsync
from contextlib import contextmanager

from vit.commands.config import (
    HISTORY_FILE,
    TEMP_FOLDER,
    VIT_COMMITS_FOLDER,
    VITIGNORE_FILE_NAME,
)


def get_ignored_files() -> List[str]:
    if os.path.exists(VITIGNORE_FILE_NAME):
        with open(VITIGNORE_FILE_NAME, "r") as vitignore_file:
            return list(
                filter(
                    lambda l: l, map(lambda l: l.strip(), vitignore_file.readlines())
                )
            )
    else:
        return []


@contextmanager
def merged_commits():
    with open(HISTORY_FILE, "r") as history_file:
        commit_names = map(
            lambda l: l.strip().split(" - ")[-2], history_file.readlines()
        )
        os.mkdir(TEMP_FOLDER)
        for commit in commit_names:
            commit_folder = f"{VIT_COMMITS_FOLDER}/{commit}"
            shutil.unpack_archive(
                f"{commit_folder}.zip",
                commit_folder,
                "zip",
            )
            for file in os.listdir(commit_folder):
                sysrsync.run(
                    source=f"{commit_folder}/{file}",
                    destination=TEMP_FOLDER,
                )
            shutil.rmtree(commit_folder)

        yield

        shutil.rmtree(TEMP_FOLDER)
