import psutil


class Dark8ProcessBackend:
    """
    Backend menadżera procesów DARK8‑OS.
    """

    def get_system_usage(self):
        cpu = psutil.cpu_percent(interval=0.1)
        ram = psutil.virtual_memory().percent
        return cpu, ram

    def get_process_list(self):
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                info = proc.info
                processes.append(info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return processes

    def kill_process(self, pid: int):
        try:
            p = psutil.Process(pid)
            p.terminate()
            return True
        except Exception:
            return False
