import os
import shutil
from uuid import uuid4
from datetime import datetime

from vit.commands.config import (
    HISTORY_FILE,
    TRACKED_FILES_FILE,
    VIT_COMMITS_FOLDER,
    VIT_STAGING_FOLDER,
)
from vit.commands.helpers import update_current_commit_id


def commit_files(msg: str):
    commit_id = uuid4().hex
    commit_folder = f"{VIT_COMMITS_FOLDER}/{commit_id}"

    shutil.copytree(VIT_STAGING_FOLDER, commit_folder)

    with open(TRACKED_FILES_FILE, "a+") as tracked_files_file:
        tracked_files_file.seek(0)
        tracked_files = filter(
            lambda l: l, map(lambda l: l.strip(), tracked_files_file.readlines())
        )
        new_to_track_files = set(os.listdir(VIT_STAGING_FOLDER)) - set(tracked_files)
        tracked_files_file.write("\n".join(new_to_track_files) + "\n")

    with open(HISTORY_FILE, "a") as history_file:
        history_file.write(f"{datetime.now()} - commit {commit_id} - {msg}\n")

    update_current_commit_id(commit_id)

    shutil.rmtree(VIT_STAGING_FOLDER)
    os.mkdir(VIT_STAGING_FOLDER)

    shutil.make_archive(commit_folder, "zip", commit_folder)
    shutil.rmtree(commit_folder)
