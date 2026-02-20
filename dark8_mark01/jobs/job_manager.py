# job_manager.py
# DARK8 OS — Warstwa procesów / jobów

import time
from typing import Dict, Any, List


_jobs: Dict[int, Dict[str, Any]] = {}
_next_id: int = 1


def _now():
    return time.strftime("%Y-%m-%d %H:%M:%S")


def create_job(goal: str) -> int:
    global _next_id
    job_id = _next_id
    _next_id += 1

    _jobs[job_id] = {
        "id": job_id,
        "goal": goal,
        "status": "pending",
        "created_at": _now(),
        "started_at": None,
        "finished_at": None,
        "result": None,
    }
    return job_id


def start_job(job_id: int):
    job = _jobs.get(job_id)
    if not job:
        return
    job["status"] = "running"
    job["started_at"] = _now()


def finish_job(job_id: int, result: Any):
    job = _jobs.get(job_id)
    if not job:
        return
    job["status"] = "finished"
    job["finished_at"] = _now()
    job["result"] = result


def fail_job(job_id: int, error: str):
    job = _jobs.get(job_id)
    if not job:
        return
    job["status"] = "failed"
    job["finished_at"] = _now()
    job["result"] = error


def kill_job(job_id: int):
    job = _jobs.get(job_id)
    if not job:
        return "Brak joba o ID: {job_id}"
    if job["status"] in ["finished", "failed"]:
        return f"Job {job_id} już zakończony."
    job["status"] = "killed"
    job["finished_at"] = _now()
    return f"Oznaczono job {job_id} jako killed."


def list_jobs() -> List[Dict[str, Any]]:
    return list(_jobs.values())


def get_job(job_id: int):
    return _jobs.get(job_id)
