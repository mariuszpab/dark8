import curses
import time
import os
import socket
import psutil


LOG_DIR = "dark8_logs"
BACKEND_LOG = os.path.join(LOG_DIR, "backend.log")
WATCHDOG_LOG = os.path.join(LOG_DIR, "watchdog.log")
SCHEDULER_LOG = os.path.join(LOG_DIR, "scheduler_snapshot.log")
STATE_LOG = os.path.join(LOG_DIR, "state_monitor.log")

REFRESH_INTERVAL = 1  # sekundy
MAX_LOG_LINES = 10


def _port_open(host: str, port: int, timeout: float = 1.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False


def _tail_file(path: str, max_lines: int):
    if not os.path.exists(path):
        return ["(brak pliku)"]

    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        return [f"(błąd odczytu: {e})"]

    lines = [ln.rstrip("\n") for ln in lines]
    if len(lines) <= max_lines:
        return lines
    return lines[-max_lines:]


def _draw_box(win, y, x, h, w, title):
    win.attron(curses.color_pair(2))
    win.border()
    win.attroff(curses.color_pair(2))
    win.addstr(y, x + 2, f"[ {title} ]", curses.color_pair(3))


def _draw_dashboard(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)

    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)   # normal
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)    # box
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)    # title
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)   # OK
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)     # ERROR
    curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # WARN

    while True:
        stdscr.erase()
        max_y, max_x = stdscr.getmaxyx()

        # Minimalny rozmiar
        if max_y < 24 or max_x < 80:
            stdscr.addstr(0, 0, "Zwiększ rozmiar terminala (min 80x24).", curses.color_pair(5))
            stdscr.refresh()
            time.sleep(1)
            continue

        # Sekcja 1: Backend + CPU/RAM
        backend_ok = _port_open("127.0.0.1", 11434)
        cpu = psutil.cpu_percent(interval=0.1)
        ram = psutil.virtual_memory().percent

        stdscr.addstr(0, 2, "DARK8‑OS TERMINAL DASHBOARD v1 (Q = wyjście)", curses.color_pair(3))

        # Backend status
        stdscr.addstr(2, 2, "Backend LLM: ", curses.color_pair(1))
        if backend_ok:
            stdscr.addstr("OK", curses.color_pair(4))
        else:
            stdscr.addstr("DOWN", curses.color_pair(5))

        # CPU / RAM
        stdscr.addstr(3, 2, f"CPU: {cpu:.1f}%   RAM: {ram:.1f}%", curses.color_pair(1))

        # Sekcja logów
        box_height = 8
        box_width = max_x // 2 - 2

        # Backend log
        backend_win = curses.newwin(box_height, box_width, 5, 1)
        _draw_box(backend_win, 0, 0, box_height - 1, box_width - 1, "backend.log")
        backend_lines = _tail_file(BACKEND_LOG, MAX_LOG_LINES)
        for i, line in enumerate(backend_lines[: box_height - 2]):
            backend_win.addstr(1 + i, 2, line[: box_width - 4], curses.color_pair(1))
        backend_win.refresh()

        # Watchdog log
        watchdog_win = curses.newwin(box_height, box_width, 5, box_width + 2)
        _draw_box(watchdog_win, 0, 0, box_height - 1, box_width - 1, "watchdog.log")
        watchdog_lines = _tail_file(WATCHDOG_LOG, MAX_LOG_LINES)
        for i, line in enumerate(watchdog_lines[: box_height - 2]):
            watchdog_win.addstr(1 + i, 2, line[: box_width - 4], curses.color_pair(1))
        watchdog_win.refresh()

        # Scheduler log
        sched_win = curses.newwin(box_height, box_width, 5 + box_height, 1)
        _draw_box(sched_win, 0, 0, box_height - 1, box_width - 1, "scheduler_snapshot.log")
        sched_lines = _tail_file(SCHEDULER_LOG, MAX_LOG_LINES)
        for i, line in enumerate(sched_lines[: box_height - 2]):
            sched_win.addstr(1 + i, 2, line[: box_width - 4], curses.color_pair(1))
        sched_win.refresh()

        # State monitor log
        state_win = curses.newwin(box_height, box_width, 5 + box_height, box_width + 2)
        _draw_box(state_win, 0, 0, box_height - 1, box_width - 1, "state_monitor.log")
        state_lines = _tail_file(STATE_LOG, MAX_LOG_LINES)
        for i, line in enumerate(state_lines[: box_height - 2]):
            state_win.addstr(1 + i, 2, line[: box_width - 4], curses.color_pair(1))
        state_win.refresh()

        stdscr.refresh()

        # Obsługa klawiszy
        try:
            ch = stdscr.getch()
            if ch in (ord("q"), ord("Q")):
                break
        except Exception:
            pass

        time.sleep(REFRESH_INTERVAL)


def run_dashboard():
    curses.wrapper(_draw_dashboard)
