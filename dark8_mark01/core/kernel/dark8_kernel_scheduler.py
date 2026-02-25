from dark8_mark01.core.kernel.dark8_init_task import Dark8InitTask
from dark8_mark01.core.kernel.dark8_ipc_bus import Dark8IPC
from dark8_mark01.core.kernel.dark8_kernel_event_dispatcher import Dark8KernelEventDispatcher
from dark8_mark01.core.kernel.dark8_kernel_task import Dark8KernelTask, Dark8TaskState


class Dark8KernelScheduler:
    """
    Scheduler DARK8 – procesy systemowe, userland, INIT, IPC.
    """

    _instance = None

    def __init__(self):
        self.tasks: list[Dark8KernelTask] = []
        self.dispatcher = Dark8KernelEventDispatcher.instance()

        # INIT (PID 1)
        self.init_task = Dark8InitTask()
        self.add_task(self.init_task)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = Dark8KernelScheduler()
        return cls._instance

    def add_task(self, task: Dark8KernelTask):
        self.tasks.append(task)
        Dark8IPC.instance().register_pid(task.pid)

        self.dispatcher.emit(
            "TASK_ADDED",
            "KernelScheduler",
            {
                "pid": task.pid,
                "name": task.name,
                "priority": task.priority,
                "state": task.state.name,
                "type": "user" if getattr(task, "userland", False) else "system",
            },
        )

    def stop_task(self, pid: int):
        for t in self.tasks:
            if t.pid == pid:
                t.state = Dark8TaskState.STOPPED
                Dark8IPC.instance().unregister_pid(pid)
                self.dispatcher.emit(
                    "TASK_STOPPED",
                    "KernelScheduler",
                    {"pid": t.pid, "name": t.name},
                )
                break

    def kill_task(self, pid: int) -> bool:
        for t in self.tasks:
            if t.pid == pid:
                t.state = Dark8TaskState.STOPPED
                Dark8IPC.instance().unregister_pid(pid)
                self.dispatcher.emit(
                    "TASK_KILLED",
                    "KernelScheduler",
                    {"pid": t.pid, "name": t.name},
                )
                return True
        return False

    def tick(self):
        """
        Wywoływane z heartbeat.
        INIT zarządza runlevelami.
        """
        runnable = [t for t in self.tasks if t.state == Dark8TaskState.RUNNING]
        runnable.sort(key=lambda t: t.priority)

        for task in runnable:
            task.tick()
