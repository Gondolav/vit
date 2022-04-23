from dataclasses import dataclass
from typing import List
import os
import filecmp

from vit.commands.config import (
    TEMP_FOLDER,
    TRACKED_FILES_FILE,
    VIT_MAIN_FOLDER,
    VIT_STAGING_FOLDER,
)
from vit.commands.helpers import merged_commits


@dataclass
class Status:
    branch: str
    unstaged_files: List[str]
    staged_files: List[str]
    modified_files: List[str]


def get_status():
    staged_files = os.listdir(VIT_STAGING_FOLDER)
    all_files = os.listdir(os.getcwd())

    unstaged_files = list(set(all_files) - set(staged_files))

    # Collect tracked files
    tracked_files = []
    with open(TRACKED_FILES_FILE, "r") as tracked_files_file:
        tracked_files_names = filter(
            lambda l: l, map(lambda l: l.strip(), tracked_files_file.readlines())
        )

        tracked_files.extend(tracked_files_names)

    with merged_commits():
        # Collect modified files
        modified_files = []
        for file in tracked_files:
            committed_file = f"{TEMP_FOLDER}/{file}"
            if not os.path.exists(committed_file):
                modified_files.append(file)
            elif not filecmp.cmp(
                committed_file,
                file,
                shallow=False,
            ):
                modified_files.append(file)

        # Remove staged files from the modified ones
        modified_files = list(set(modified_files) - set(staged_files))

        # Remove .vit/
        unstaged_files.remove(VIT_MAIN_FOLDER)

        # Remove tracked and modified files from the unstaged ones
        unstaged_files = list(
            set(unstaged_files) - set(tracked_files) - set(modified_files)
        )

        return Status(
            branch="main",
            unstaged_files=unstaged_files,
            staged_files=staged_files,
            modified_files=modified_files,
        )
