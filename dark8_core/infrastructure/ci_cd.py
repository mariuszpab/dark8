"""
DARK8 OS - Phase 4: CI/CD Pipeline
Ciągła integracja i automatyczne deployementy
Autor: DARK8 Development Team
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
from collections import deque


class PipelineStage(Enum):
    """Etapy pipeline'u CI/CD"""
    CHECKOUT = "checkout"
    BUILD = "build"
    TEST = "test"
    SECURITY_SCAN = "security_scan"
    DEPLOY_STAGING = "deploy_staging"
    INTEGRATION_TEST = "integration_test"
    DEPLOY_PRODUCTION = "deploy_production"
    SMOKE_TEST = "smoke_test"


class JobStatus(Enum):
    """Status jobu w pipeline'ie"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"
    CANCELLED = "cancelled"


@dataclass
class PipelineJob:
    """Reprezentacja jobu w pipeline'ie"""
    job_id: str
    name: str
    stage: PipelineStage
    status: JobStatus = JobStatus.PENDING
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    duration_seconds: float = 0.0
    output: str = ""
    exit_code: int = 0
    
    def to_dict(self) -> dict:
        """Konwersja do słownika"""
        d = asdict(self)
        d['stage'] = self.stage.value
        d['status'] = self.status.value
        d['started_at'] = self.started_at.isoformat() if self.started_at else None
        d['finished_at'] = self.finished_at.isoformat() if self.finished_at else None
        return d


@dataclass
class Pipeline:
    """Reprezentacja pipeline'u CI/CD"""
    pipeline_id: str
    name: str
    repository: str
    branch: str
    commit_sha: str
    triggered_by: str
    created_at: datetime
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    status: JobStatus = JobStatus.PENDING
    jobs: List[PipelineJob] = None
    
    def __post_init__(self):
        if self.jobs is None:
            self.jobs = []
    
    def to_dict(self) -> dict:
        """Konwersja do słownika"""
        d = asdict(self)
        d['created_at'] = self.created_at.isoformat()
        d['started_at'] = self.started_at.isoformat() if self.started_at else None
        d['finished_at'] = self.finished_at.isoformat() if self.finished_at else None
        d['status'] = self.status.value
        d['jobs'] = [j.to_dict() for j in self.jobs]
        return d


class PipelineEngine:
    """
    Engine orkiestracji CI/CD
    Managuje buildami, deploymentami i testami
    """
    
    def __init__(self, repo_url: str = "https://github.com/dark8os/core"):
        """Inicjalizacja Pipeline Engine"""
        self.repo_url = repo_url
        self.pipelines: Dict[str, Pipeline] = {}
        self.pipeline_queue: deque = deque()
        self.completed_pipelines: deque = deque(maxlen=1000)
        self.webhook_secrets: Dict[str, str] = {}
        self.build_cache: Dict[str, Dict] = {}
        self.created_at = datetime.now()
        
    def create_pipeline(self,
                       commit_sha: str,
                       branch: str = "main",
                       triggered_by: str = "webhook") -> Pipeline:
        """
        Tworzenie nowego pipeline'u
        
        Args:
            commit_sha: SHA commita
            branch: Gałąź
            triggered_by: Kto wyzwolił (webhook, manual, schedule)
            
        Returns:
            Pipeline: Nowy pipeline
        """
        pipeline_id = f"pipeline-{len(self.pipelines)}"
        
        pipeline = Pipeline(
            pipeline_id=pipeline_id,
            name=f"Build {commit_sha[:7]} on {branch}",
            repository=self.repo_url,
            branch=branch,
            commit_sha=commit_sha,
            triggered_by=triggered_by,
            created_at=datetime.now()
        )
        
        self.pipelines[pipeline_id] = pipeline
        self.pipeline_queue.append(pipeline_id)
        
        return pipeline
    
    def create_default_jobs(self, pipeline: Pipeline) -> List[PipelineJob]:
        """Tworzenie domyślnych jobów dla pipeline'u"""
        jobs = [
            PipelineJob(
                job_id=f"{pipeline.pipeline_id}-checkout",
                name="Checkout code",
                stage=PipelineStage.CHECKOUT
            ),
            PipelineJob(
                job_id=f"{pipeline.pipeline_id}-build",
                name="Build Docker image",
                stage=PipelineStage.BUILD
            ),
            PipelineJob(
                job_id=f"{pipeline.pipeline_id}-test",
                name="Run tests",
                stage=PipelineStage.TEST
            ),
            PipelineJob(
                job_id=f"{pipeline.pipeline_id}-security",
                name="Security scan",
                stage=PipelineStage.SECURITY_SCAN
            ),
            PipelineJob(
                job_id=f"{pipeline.pipeline_id}-staging",
                name="Deploy to staging",
                stage=PipelineStage.DEPLOY_STAGING
            ),
            PipelineJob(
                job_id=f"{pipeline.pipeline_id}-integration",
                name="Integration tests",
                stage=PipelineStage.INTEGRATION_TEST
            ),
            PipelineJob(
                job_id=f"{pipeline.pipeline_id}-production",
                name="Deploy to production",
                stage=PipelineStage.DEPLOY_PRODUCTION
            ),
            PipelineJob(
                job_id=f"{pipeline.pipeline_id}-smoke",
                name="Smoke tests",
                stage=PipelineStage.SMOKE_TEST
            )
        ]
        
        pipeline.jobs = jobs
        return jobs
    
    def execute_job(self, pipeline_id: str, job_id: str) -> bool:
        """
        Wykonanie jobu
        
        Args:
            pipeline_id: ID pipeline'u
            job_id: ID jobu
            
        Returns:
            bool: Czy job powiódł się
        """
        if pipeline_id not in self.pipelines:
            return False
        
        pipeline = self.pipelines[pipeline_id]
        job = next((j for j in pipeline.jobs if j.job_id == job_id), None)
        
        if not job:
            return False
        
        job.status = JobStatus.RUNNING
        job.started_at = datetime.now()

        # Wsparcie dla retry - można ustawić max_retries na jobie przez metadata
        max_retries = getattr(job, 'max_retries', 3)
        attempt = 0

        while attempt < max_retries:
            attempt += 1
            try:
                # Symulacja wykonania jobu
                time.sleep(0.05)

                # Symulacja różnych wyników
                success_rate = 0.92  # trochę niżej, retry pomoże
                import random

                if random.random() < success_rate:
                    job.status = JobStatus.SUCCESS
                    job.exit_code = 0
                    job.output = f"✅ Job {job.name} completed successfully on attempt {attempt}"
                else:
                    job.status = JobStatus.FAILED
                    job.exit_code = 1
                    job.output = f"❌ Job {job.name} failed on attempt {attempt}"

                job.finished_at = datetime.now()
                job.duration_seconds = (job.finished_at - job.started_at).total_seconds()

                if job.status == JobStatus.SUCCESS:
                    return True
                else:
                    # Retry jeśli nie osiągnięto sukcesu
                    if attempt < max_retries:
                        time.sleep(0.02)  # krótka pauza przed retry
                        continue
                    else:
                        return False

            except Exception as e:
                job.status = JobStatus.FAILED
                job.exit_code = 1
                job.output = f"Error: {str(e)}"
                job.finished_at = datetime.now()
                if attempt < max_retries:
                    time.sleep(0.02)
                    continue
                return False
    
    def run_pipeline(self, pipeline_id: str) -> bool:
        """
        Uruchomienie kompletnego pipeline'u
        
        Args:
            pipeline_id: ID pipeline'u
            
        Returns:
            bool: Czy pipeline powiódł się
        """
        if pipeline_id not in self.pipelines:
            return False
        
        pipeline = self.pipelines[pipeline_id]
        
        if not pipeline.jobs:
            self.create_default_jobs(pipeline)
        
        pipeline.status = JobStatus.RUNNING
        pipeline.started_at = datetime.now()
        
        all_success = True
        
        # Uruchomienie jobów sekwencyjnie
        for job in pipeline.jobs:
            success = self.execute_job(pipeline_id, job.job_id)
            
            if not success:
                all_success = False
                # Failfast - stop pipeline na pierwszym błędzie
                break
        
        # Finalizacja pipeline'u
        pipeline.finished_at = datetime.now()
        pipeline.status = JobStatus.SUCCESS if all_success else JobStatus.FAILED
        
        # Przenieś do completed
        self.completed_pipelines.append(pipeline_id)
        
        return all_success
    
    def get_pipeline_status(self, pipeline_id: str) -> Optional[Dict]:
        """Pobranie statusu pipeline'u"""
        if pipeline_id not in self.pipelines:
            return None
        
        pipeline = self.pipelines[pipeline_id]
        
        return {
            'pipeline_id': pipeline_id,
            'status': pipeline.status.value,
            'commit': pipeline.commit_sha[:7],
            'branch': pipeline.branch,
            'jobs_completed': sum(1 for j in pipeline.jobs if j.status != JobStatus.PENDING),
            'jobs_total': len(pipeline.jobs),
            'duration_seconds': (pipeline.finished_at - pipeline.started_at).total_seconds() 
                              if pipeline.finished_at else 0
        }
    
    def get_pipeline_history(self, limit: int = 20) -> List[Dict]:
        """Pobranie historii pipeline'ów"""
        history = []
        
        for pipeline_id in reversed(list(self.completed_pipelines)[-limit:]):
            status = self.get_pipeline_status(pipeline_id)
            if status:
                history.append(status)
        
        return history


class ArtifactManager:
    """Manager artefaktów (Docker images, binaries)"""
    
    def __init__(self):
        """Inicjalizacja Artifact Manager"""
        self.artifacts: Dict[str, Dict] = {}
        self.artifact_registry: Dict[str, List[str]] = {}  # artifact -> versions
        self.build_cache: Dict[str, Dict] = {}
        
    def store_artifact(self,
                      name: str,
                      version: str,
                      type: str,
                      size_bytes: int,
                      metadata: Dict = None) -> bool:
        """
        Zapamiętanie artefaktu
        
        Args:
            name: Nazwa artefaktu
            version: Wersja
            type: Typ ('docker_image', 'binary', 'package')
            size_bytes: Rozmiar
            metadata: Dodatkowe metadane
            
        Returns:
            bool: Czy artefakt został zapamiętany
        """
        artifact_id = f"{name}:{version}"
        
        self.artifacts[artifact_id] = {
            'name': name,
            'version': version,
            'type': type,
            'size_bytes': size_bytes,
            'created_at': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        
        if name not in self.artifact_registry:
            self.artifact_registry[name] = []
        
        self.artifact_registry[name].append(version)
        
        return True
    
    def get_artifact(self, name: str, version: str = "latest") -> Optional[Dict]:
        """Pobranie artefaktu"""
        if version == "latest" and name in self.artifact_registry:
            version = self.artifact_registry[name][-1]
        
        artifact_id = f"{name}:{version}"
        return self.artifacts.get(artifact_id)
    
    def get_artifact_stats(self) -> Dict:
        """Statystyki artefaktów"""
        total_size = sum(a['size_bytes'] for a in self.artifacts.values())
        
        return {
            'total_artifacts': len(self.artifacts),
            'total_size_bytes': total_size,
            'unique_names': len(self.artifact_registry),
            'registry_names': list(self.artifact_registry.keys())
        }


class Webhook:
    """Manager webhooku do Git'a"""
    
    def __init__(self, pipeline_engine: PipelineEngine):
        """Inicjalizacja Webhook'a"""
        self.pipeline_engine = pipeline_engine
        self.webhook_events: deque = deque(maxlen=1000)
        
    def handle_push_event(self, 
                         repository: str,
                         branch: str,
                         commit_sha: str) -> bool:
        """
        Obsłużenie push event'u z Git'a
        
        Args:
            repository: Repo URL
            branch: Branch
            commit_sha: Commit SHA
            
        Returns:
            bool: Czy pipeline został uruchomiony
        """
        # Zapis event'u
        self.webhook_events.append({
            'type': 'push',
            'repository': repository,
            'branch': branch,
            'commit': commit_sha[:7],
            'timestamp': datetime.now().isoformat()
        })
        
        # Filtruj tylko main branch
        if branch != 'main':
            return False
        
        # Utwórz pipeline
        pipeline = self.pipeline_engine.create_pipeline(
            commit_sha=commit_sha,
            branch=branch,
            triggered_by='webhook'
        )
        
        # Uruchom pipeline
        return self.pipeline_engine.run_pipeline(pipeline.pipeline_id)
    
    def handle_pull_request_event(self,
                                  repository: str,
                                  branch: str,
                                  commit_sha: str) -> bool:
        """Obsłużenie PR event'u"""
        self.webhook_events.append({
            'type': 'pull_request',
            'repository': repository,
            'branch': branch,
            'commit': commit_sha[:7],
            'timestamp': datetime.now().isoformat()
        })
        
        # Utwórz pipeline dla PR
        pipeline = self.pipeline_engine.create_pipeline(
            commit_sha=commit_sha,
            branch=branch,
            triggered_by='pull_request'
        )
        
        return self.pipeline_engine.run_pipeline(pipeline.pipeline_id)
    
    def get_webhook_stats(self) -> Dict:
        """Statystyki webhoku"""
        push_count = sum(1 for e in self.webhook_events if e['type'] == 'push')
        pr_count = sum(1 for e in self.webhook_events if e['type'] == 'pull_request')
        
        return {
            'total_events': len(self.webhook_events),
            'push_events': push_count,
            'pull_request_events': pr_count,
            'recent_events': list(self.webhook_events)[-5:]
        }


def test_cicd_pipeline():
    """Test CI/CD Pipeline"""
    print("\n🔧 Testowanie CI/CD Pipeline...")
    
    # Inicjalizacja
    engine = PipelineEngine()
    
    # Tworzenie pipeline'u
    pipeline = engine.create_pipeline(
        commit_sha='abc123def456',
        branch='main',
        triggered_by='webhook'
    )
    
    print(f"✅ Pipeline utworzony: {pipeline.pipeline_id}")
    
    # Uruchomienie pipeline'u
    success = engine.run_pipeline(pipeline.pipeline_id)
    print(f"✅ Pipeline wynik: {'SUCCESS' if success else 'FAILED'}")
    
    # Status
    status = engine.get_pipeline_status(pipeline.pipeline_id)
    print(f"✅ Status: {json.dumps(status, indent=2)}")
    
    # Artifacts
    artifacts = ArtifactManager()
    artifacts.store_artifact('dark8-api', '1.0.0', 'docker_image', 524288000)
    
    stats = artifacts.get_artifact_stats()
    print(f"✅ Artifacts: {stats}")
    
    # Webhook
    webhook = Webhook(engine)
    result = webhook.handle_push_event(
        'https://github.com/dark8os/core',
        'main',
        'xyz789abc123'
    )
    print(f"✅ Webhook result: {result}")
    
    webhook_stats = webhook.get_webhook_stats()
    print(f"✅ Webhook stats: {webhook_stats}")


if __name__ == '__main__':
    test_cicd_pipeline()
