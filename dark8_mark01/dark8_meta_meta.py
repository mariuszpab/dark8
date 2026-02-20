# dark8_meta_meta.py
# Meta-meta-agent dla DARK8

from pprint import pformat

from dark8_mark01.dark8_self_diagnostics import full_diagnostics
from dark8_mark01.dark8_self_repair import self_repair


def meta_meta_status():
    diag = full_diagnostics()
    return (
        "META-META STATUS DARK8\n"
        "======================\n\n"
        f"{pformat(diag, indent=2, width=100)}"
    )


def meta_meta_repair():
    result = self_repair()
    return (
        "META-META REPAIR DARK8\n"
        "======================\n\n"
        f"Log migracji:\n{result['migrations_log']}\n\n"
        f"Diagnostyka po naprawie:\n{pformat(result['diagnostics_after'], indent=2, width=100)}"
    )
