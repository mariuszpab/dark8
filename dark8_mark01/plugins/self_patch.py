from ..command_registry import register_command
from ..commands.patch_ops import patch_diff, patch_file


def handle_self_patch_file(command, args, block):
    """
    SELF_PATCH_FILE <ścieżka>
    <<<END
    { JSON5 patch }
    END
    """
    path = args.strip()
    if not path:
        print("[ERROR][SELF_PATCH] Brak ścieżki.")
        return

    print(f"[SELF_PATCH] Patchuję plik (JSON/YAML): {path}")
    patch_file(path, block)


def handle_self_patch_diff(command, args, block):
    """
    SELF_PATCH_DIFF <ścieżka>
    <<<END
    --- a/file
    +++ b/file
    @@ ...
    END
    """
    path = args.strip()
    if not path:
        print("[ERROR][SELF_PATCH] Brak ścieżki.")
        return

    print(f"[SELF_PATCH] Patchuję plik (DIFF): {path}")
    patch_diff(path, block)


def register():
    register_command("SELF_PATCH_FILE", handle_self_patch_file)
    register_command("SELF_PATCH_DIFF", handle_self_patch_diff)
    print("[INFO][PLUGINS] Plugin SELF_PATCH zarejestrowany")
