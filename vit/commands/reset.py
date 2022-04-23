import shutil
from typing import List
from vit.commands.config import TEMP_FOLDER
from vit.commands.helpers import merged_commits


def reset_files(files: List[str]):
    with merged_commits():
        for file in files:
            shutil.copy2(f"{TEMP_FOLDER}/{file}", file)
