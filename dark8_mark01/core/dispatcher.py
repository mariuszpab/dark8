# dispatcher.py
# DARK8 OS — Warstwa wykonawcza (ACTION LAYER + TOOLS LAYER)

from dark8_mark01.core.actions import (
    run_app,
    delete_file,
    make_dir,
    remove_dir,
    read_file,
    write_file,
    list_dir,
    change_dir,
    run_python_script,
    show_cwd,
    copy_file,
    move_file,
    touch_file,
)

from dark8_mark01.tools.codegen import generate_code
from dark8_mark01.tools.project_builder import create_project
from dark8_mark01.tools.file_editor import append_to_file, overwrite_file
from dark8_mark01.tools.compiler import run_python


ACTIONS = {
    # --- SYSTEM OPERATIONS ---
    "RUN_APP": run_app,
    "DELETE_FILE": delete_file,
    "MAKE_DIR": make_dir,
    "REMOVE_DIR": remove_dir,
    "READ_FILE": read_file,
    "WRITE_FILE": write_file,

    # --- FILE / SHELL COMMANDS ---
    "LIST_DIR": list_dir,
    "CHANGE_DIR": change_dir,
    "RUN_PYTHON_SCRIPT": run_python_script,
    "SHOW_CWD": show_cwd,
    "COPY_FILE": copy_file,
    "MOVE_FILE": move_file,
    "TOUCH_FILE": touch_file,

    # --- TOOLS LAYER ---
    "GENERATE_CODE": generate_code,
    "CREATE_PROJECT": create_project,
    "EDIT_FILE": append_to_file,
    "OVERWRITE_FILE": overwrite_file,
    "BUILD_PROJECT": run_python,
}


def dispatch(intent: str, args: dict):
    if intent not in ACTIONS:
        return f"Brak obsługi dla intencji: {intent}"

    try:
        func = ACTIONS[intent]
        return func(**args)
    except TypeError as e:
        return f"Niepoprawne argumenty dla intencji {intent}: {e}"
    except Exception as e:
        return f"Błąd wykonania intencji {intent}: {e}"
