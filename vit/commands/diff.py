import difflib
from vit.commands.config import TEMP_FOLDER

from vit.commands.helpers import merged_commits


def get_diff(file: str) -> str:
    with merged_commits():
        with open(file, "r") as curr_file:
            with open(f"{TEMP_FOLDER}/{file}") as stored_file:
                curr_file_lines = list(map(lambda l: l.strip(), curr_file.readlines()))
                stored_file_lines = list(
                    map(lambda l: l.strip(), stored_file.readlines())
                )
                return "\n".join(
                    difflib.unified_diff(
                        stored_file_lines,
                        curr_file_lines,
                        fromfile=f"{file} (stored)",
                        tofile=f"{file} (current)",
                        lineterm="",
                    )
                )
