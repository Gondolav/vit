from vit.commands.config import HISTORY_FILE


def get_history() -> str:
    with open(HISTORY_FILE, "r") as history_file:
        lines = filter(lambda l: l, map(lambda l: l.strip(), history_file.readlines()))
        return "\n".join(lines)
