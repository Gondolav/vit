import os
from vit.commands.config import VIT_MAIN_FOLDER


def init_vit():
    os.mkdir(VIT_MAIN_FOLDER)
    os.mkdir(f"{VIT_MAIN_FOLDER}/staging")
    os.mkdir(f"{VIT_MAIN_FOLDER}/commits")
