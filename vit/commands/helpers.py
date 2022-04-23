import os
import shutil
from typing import List
import sysrsync
from contextlib import contextmanager

from vit.commands.config import (
    CURRENT_COMMIT_FILE,
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


def get_commit_id_from_history_line(line: str) -> str:
    return line.strip().split(" - ")[-2].replace("commit ", "")


def get_current_commit_id() -> str:
    with open(CURRENT_COMMIT_FILE, "r") as current_commit_file:
        return current_commit_file.readline().strip()


def get_last_commit_id() -> str:
    with open(HISTORY_FILE, "r") as history_file:
        commit_names = list(
            map(lambda l: get_commit_id_from_history_line(l), history_file.readlines())
        )
        return commit_names[-1]


def am_i_in_the_past(current_commit_id: str, last_commit_id: str) -> bool:
    commit_ids = get_all_commit_ids()
    current_commit_index = commit_ids.index(current_commit_id)
    last_commit_index = commit_ids.index(last_commit_id)

    if current_commit_index >= last_commit_index:
        return False
    else:
        return True


def update_current_commit_id(new_commit_id: str):
    with open(CURRENT_COMMIT_FILE, "w") as current_commit_file:
        current_commit_file.write(f"{new_commit_id}\n")


def get_all_commit_ids() -> List[str]:
    with open(HISTORY_FILE, "r") as history_file:
        return list(
            map(lambda l: get_commit_id_from_history_line(l), history_file.readlines())
        )


@contextmanager
def merged_commits():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as history_file:
            commit_ids = map(
                lambda l: get_commit_id_from_history_line(l), history_file.readlines()
            )
            os.mkdir(TEMP_FOLDER)
            for commit in commit_ids:
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
    else:
        yield
