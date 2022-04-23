import os
import shutil
import sysrsync
from vit.commands.config import TEMP_FOLDER, VIT_COMMITS_FOLDER
from vit.commands.helpers import (
    am_i_in_the_past,
    get_all_commit_ids,
    get_current_commit_id,
    update_current_commit_id,
)


def travel_to(commit_id: str):
    commit_ids = get_all_commit_ids()

    current_commit_id = get_current_commit_id()
    current_commit_index = commit_ids.index(current_commit_id)
    destination_commit_index = commit_ids.index(commit_id)

    in_the_past = am_i_in_the_past(current_commit_id, commit_id)

    if not in_the_past:
        commit_ids = reversed(
            commit_ids[destination_commit_index : current_commit_index + 1]
        )
    else:
        commit_ids = commit_ids[current_commit_index : destination_commit_index + 1]

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
            shutil.copy2(f"{TEMP_FOLDER}/{file}", file)

        shutil.rmtree(commit_folder)

    for file in os.listdir(TEMP_FOLDER):
        shutil.copy2(f"{TEMP_FOLDER}/{file}", file)

    shutil.rmtree(TEMP_FOLDER)

    update_current_commit_id(commit_id)
