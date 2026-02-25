import os
import threading
import time

from dark8_mark01.utils.dark8_auto_fix import auto_fix_dark8_project
from dark8_mark01.utils.dark8_backend import ensure_backend_ready
from dark8_mark01.utils.dark8_code_reader import analyze_dark8_project

# Co ile minut wykonywać snapshot
SNAPSHOT_INTERVAL_MIN = 15

# Czy wykonywać auto-fix po snapshotach
ENABLE_AUTOFIX = False

# Gdzie zapisywać snapshoty
SNAPSHOT_LOG = "dark8_logs/scheduler_snapshot.log"


def _log(msg: str):
    os.makedirs(os.path.dirname(SNAPSHOT_LOG), exist_ok=True)
    with open(SNAPSHOT_LOG, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(f"[SCHEDULER] {msg}")


def _run_snapshot_cycle():
    """
    Wykonuje snapshot projektu DARK8.
    """
    project_root = os.path.abspath(os.getcwd())

    _log("Rozpoczynam snapshot projektu...")
    ensure_backend_ready()

    report = analyze_dark8_project(project_root)

    _log("Snapshot zakończony. Zapisuję raport...")

    with open(SNAPSHOT_LOG, "a", encoding="utf-8") as f:
        f.write("\n\n===== SNAPSHOT REPORT =====\n")
        f.write(report)
        f.write("\n===== END SNAPSHOT =====\n")

    _log("Raport snapshot zapisany.")

    if ENABLE_AUTOFIX:
        _log("AUTO-FIX włączony — rozpoczynam auto-fix projektu...")
        auto_fix_root = os.path.join(project_root, "projekty", "auto_fix")
        summary = auto_fix_dark8_project(project_root, auto_fix_root)

        with open(SNAPSHOT_LOG, "a", encoding="utf-8") as f:
            f.write("\n\n===== AUTO-FIX SUMMARY =====\n")
            f.write(summary)
            f.write("\n===== END AUTO-FIX =====\n")

        _log("Auto-fix zakończony.")


def _scheduler_loop():
    """
    Główna pętla schedulera.
    """
    _log("Scheduler DARK8-OS uruchomiony.")

    while True:
        _run_snapshot_cycle()
        _log(f"Czekam {SNAPSHOT_INTERVAL_MIN} minut do następnego cyklu...")
        time.sleep(SNAPSHOT_INTERVAL_MIN * 60)


def start_scheduler():
    """
    Uruchamia scheduler w tle.
    """
    thread = threading.Thread(target=_scheduler_loop, daemon=True)
    thread.start()
    _log("Scheduler wystartował w tle.")
