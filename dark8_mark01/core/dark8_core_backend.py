from dark8_mark01.core.vfs.dark8_vfs_manager import Dark8VFSManager
from dark8_mark01.core.kernel.dark8_kernel_scheduler import Dark8KernelScheduler
from dark8_mark01.core.kernel.dark8_user_task import Dark8UserTask
from dark8_mark01.core.kernel.dark8_ipc_bus import Dark8IPC


class Dark8CoreBackend:
    """
    Backend DARK8:
    - VFS
    - procesy (ps, run, kill)
    - IPC (send, inbox)
    - INIT + runlevels (runlevel, set-runlevel, init-status)
    """

    def __init__(self):
        self.running = False
        self.vfs = Dark8VFSManager.instance()
        self.cwd = "/"
        self.scheduler = Dark8KernelScheduler.instance()

        # terminal = PID 0
        Dark8IPC.instance().register_pid(0)

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def get_status(self):
        return "running" if self.running else "stopped"

    def _get_init(self):
        return next((t for t in self.scheduler.tasks if t.name == "init"), None)

    def execute_command(self, command: str) -> str:
        command = command.strip()
        if not command:
            return ""

        parts = command.split()
        cmd = parts[0]
        args = parts[1:]

        # ===== HELP =====
        if cmd == "help":
            return (
                "DARK8 COMMANDS:\n"
                "\nVFS:\n"
                "  pwd, ls, cd, mkdir, touch, rm, cat, write\n"
                "\nPROCESSES:\n"
                "  ps, run <name>, kill <pid>\n"
                "\nIPC:\n"
                "  send <pid> <msg>, inbox\n"
                "\nINIT / RUNLEVELS:\n"
                "  runlevel\n"
                "  set-runlevel <boot|normal|maintenance|shutdown>\n"
                "  init-status\n"
            )

        # ===== STATUS =====
        if cmd == "status":
            return f"DARK8 backend: {self.get_status()}"

        # ===== VFS =====
        if cmd == "pwd":
            return self.cwd

        if cmd == "ls":
            try:
                return "\n".join(self.vfs.list_dir(self.cwd))
            except Exception as e:
                return f"ls: {e}"

        if cmd == "cd":
            if not args:
                self.cwd = "/"
                return self.cwd

            target = args[0]

            if target == "/":
                self.cwd = "/"
                return self.cwd

            if target == "..":
                if self.cwd != "/":
                    self.cwd = "/".join(self.cwd.rstrip("/").split("/")[:-1]) or "/"
                return self.cwd

            new_path = self.cwd.rstrip("/") + "/" + target
            try:
                self.vfs.list_dir(new_path)
                self.cwd = new_path
                return self.cwd
            except Exception as e:
                return f"cd: {e}"

        if cmd == "mkdir":
            if not args:
                return "mkdir: missing name"
            path = self.cwd.rstrip("/") + "/" + args[0]
            try:
                self.vfs.create_dir(path)
                return ""
            except Exception as e:
                return f"mkdir: {e}"

        if cmd == "touch":
            if not args:
                return "touch: missing name"
            path = self.cwd.rstrip("/") + "/" + args[0]
            try:
                self.vfs.create_file(path)
                return ""
            except Exception as e:
                return f"touch: {e}"

        if cmd == "rm":
            if not args:
                return "rm: missing name"
            path = self.cwd.rstrip("/") + "/" + args[0]
            try:
                self.vfs.delete(path)
                return ""
            except Exception as e:
                return f"rm: {e}"

        if cmd == "cat":
            if not args:
                return "cat: missing name"
            path = self.cwd.rstrip("/") + "/" + args[0]
            try:
                return self.vfs.read_file(path)
            except Exception as e:
                return f"cat: {e}"

        if cmd == "write":
            if len(args) < 2:
                return "write: usage: write <name> <text>"
            name = args[0]
            text = " ".join(args[1:])
            path = self.cwd.rstrip("/") + "/" + name
            try:
                self.vfs.write_file(path, text)
                return ""
            except Exception as e:
                return f"write: {e}"

        # ===== PROCESSES =====
        if cmd == "ps":
            lines = []
            for t in self.scheduler.tasks:
                ttype = "user" if getattr(t, "userland", False) else "system"
                lines.append(f"{t.pid:4}  {t.name:20}  {t.state.name:8}  {ttype}")
            return "\n".join(lines)

        if cmd == "run":
            if not args:
                return "run: missing name"
            task = Dark8UserTask(args[0])
            self.scheduler.add_task(task)
            return f"Started process {args[0]} with PID {task.pid}"

        if cmd == "kill":
            if not args:
                return "kill: missing pid"
            if not args[0].isdigit():
                return "kill: pid must be a number"
            pid = int(args[0])
            if self.scheduler.kill_task(pid):
                return f"Killed process {pid}"
            return f"kill: no such pid"

        # ===== IPC =====
        if cmd == "send":
            if len(args) < 2:
                return "send: usage: send <pid> <msg>"
            if not args[0].isdigit():
                return "send: pid must be a number"
            pid = int(args[0])
            msg = " ".join(args[1:])
            ok = Dark8IPC.instance().send(0, pid, msg)
            return "OK" if ok else "send: no such pid"

        if cmd == "inbox":
            msgs = Dark8IPC.instance().receive(0)
            if not msgs:
                return "(empty)"
            return "\n".join([f"from {m.sender_pid}: {m.message}" for m in msgs])

        # ===== INIT / RUNLEVELS =====
        if cmd == "runlevel":
            init = self._get_init()
            if not init:
                return "init not running"
            return init.runlevel

        if cmd == "set-runlevel":
            if not args:
                return "set-runlevel: missing value"
            level = args[0]
            if level not in ("boot", "normal", "maintenance", "shutdown"):
                return "set-runlevel: invalid value"
            init = self._get_init()
            if not init:
                return "init not running"
            init.runlevel = level
            return f"runlevel set to {level}"

        if cmd == "init-status":
            init = self._get_init()
            if not init:
                return "init not running"
            lines = [f"INIT SYSTEM STATUS (runlevel={init.runlevel}):"]
            for name, pid in init.system_services.items():
                lines.append(f"  {name} -> PID {pid}")
            return "\n".join(lines)

        return f"Unknown command: {cmd}"
