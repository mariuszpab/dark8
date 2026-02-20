from dark8_mark01.core.kernel.dark8_kernel_task import Dark8KernelTask, Dark8TaskState
from dark8_mark01.core.kernel.dark8_user_task import Dark8UserTask
from dark8_mark01.core.kernel.dark8_ipc_bus import Dark8IPC


class Dark8InitTask(Dark8KernelTask):
    """
    DARK8 INIT (PID 1)
    - runlevel: boot, normal, maintenance, shutdown
    - startuje usługi systemowe
    - monitoruje i restartuje
    - zarządza trybami pracy systemu
    """

    def __init__(self):
        super().__init__("init", priority=1)
        self.userland = False
        self.system_services: dict[str, int] = {}
        self.started = False
        self.runlevel = "boot"  # boot -> normal -> maintenance/shutdown

    def start_services(self, scheduler):
        """
        Uruchamiamy usługi systemowe przy runlevel=boot.
        """
        services = [
            ("system_monitor", 3),
            ("event_dispatcher", 4),
            ("shell_runtime", 5),
        ]

        for name, prio in services:
            task = Dark8UserTask(name, prio)
            task.userland = False  # oznacz jako systemowy
            scheduler.add_task(task)
            self.system_services[name] = task.pid

        self.started = True
        self.runlevel = "normal"

    def _ensure_services_running(self, scheduler):
        """
        Restart usług systemowych, jeśli padły.
        """
        for name, pid in list(self.system_services.items()):
            proc = next((t for t in scheduler.tasks if t.pid == pid), None)
            if proc is None or proc.state == Dark8TaskState.STOPPED:
                print(f"[INIT] Restarting service: {name}")
                new_task = Dark8UserTask(name, priority=3)
                new_task.userland = False
                scheduler.add_task(new_task)
                self.system_services[name] = new_task.pid

    def _enter_maintenance(self, scheduler):
        """
        Maintenance: zatrzymujemy procesy userland.
        """
        for t in scheduler.tasks:
            if getattr(t, "userland", False) and t.name not in ("init",):
                t.state = Dark8TaskState.STOPPED

    def _enter_shutdown(self, scheduler):
        """
        Shutdown: zatrzymujemy wszystko poza INIT.
        """
        for t in scheduler.tasks:
            if t is self:
                continue
            t.state = Dark8TaskState.STOPPED

    def tick(self):
        """
        INIT działa w pętli:
        - obsługuje runlevel
        - monitoruje usługi
        - reaguje na IPC
        """
        ipc = Dark8IPC.instance()
        msgs = ipc.receive(self.pid)
        for msg in msgs:
            print(f"[INIT] message from {msg.sender_pid}: {msg.message}")

        from dark8_mark01.core.kernel.dark8_kernel_scheduler import Dark8KernelScheduler
        scheduler = Dark8KernelScheduler.instance()

        # runlevel: boot → start usług
        if self.runlevel == "boot" and not self.started:
            print("[INIT] Starting system services (runlevel=boot)")
            self.start_services(scheduler)
            return

        # runlevel: normal → usługi muszą żyć
        if self.runlevel == "normal":
            self._ensure_services_running(scheduler)
            return

        # runlevel: maintenance → zatrzymaj userland
        if self.runlevel == "maintenance":
            self._enter_maintenance(scheduler)
            self._ensure_services_running(scheduler)
            return

        # runlevel: shutdown → zatrzymaj wszystko
        if self.runlevel == "shutdown":
            self._enter_shutdown(scheduler)
            return
