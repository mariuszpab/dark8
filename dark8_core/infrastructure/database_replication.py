"""
DARK8 OS - Phase 4: Database Replication
Replikacja danych i synchronizacja bazy
Autor: DARK8 Development Team
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
from collections import deque


class ReplicationMode(Enum):
    """Tryby replikacji bazy danych"""
    MASTER_SLAVE = "master_slave"
    MULTI_MASTER = "multi_master"
    PEER_TO_PEER = "peer_to_peer"


class SyncStatus(Enum):
    """Status synchronizacji"""
    IN_SYNC = "in_sync"
    LAGGING = "lagging"
    OUT_OF_SYNC = "out_of_sync"
    SYNCING = "syncing"


@dataclass
class DatabaseInstance:
    """Reprezentacja instancji bazy danych"""
    instance_id: str
    host: str
    port: int
    role: str  # 'master' or 'slave'
    is_active: bool = True
    created_at: datetime = None
    last_heartbeat: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.last_heartbeat is None:
            self.last_heartbeat = datetime.now()
    
    def to_dict(self) -> dict:
        """Konwersja do słownika"""
        d = asdict(self)
        d['created_at'] = self.created_at.isoformat()
        d['last_heartbeat'] = self.last_heartbeat.isoformat()
        return d


@dataclass
class BinlogEntry:
    """Reprezentacja wpisu z binlogu"""
    entry_id: str
    timestamp: datetime
    query: str
    database: str
    transaction_id: int
    checksum: str
    size_bytes: int


class DatabaseReplication:
    """
    Manager replikacji bazy danych
    Wspiera Master-Slave, Multi-Master, i P2P
    """
    
    def __init__(self, replication_mode: ReplicationMode = ReplicationMode.MASTER_SLAVE):
        """
        Inicjalizacja replikacji bazy
        
        Args:
            replication_mode: Tryb replikacji
        """
        self.replication_mode = replication_mode
        self.instances: Dict[str, DatabaseInstance] = {}
        self.binlog: deque = deque(maxlen=10000)
        self.sync_status: Dict[str, SyncStatus] = {}
        self.replication_lag: Dict[str, float] = {}  # seconds
        self.last_synced_position: Dict[str, int] = {}
        self.created_at = datetime.now()
        
    def add_instance(self, instance: DatabaseInstance) -> bool:
        """
        Dodanie instancji bazy
        
        Args:
            instance: Instancja bazy do dodania
            
        Returns:
            bool: Czy instancja została dodana
        """
        try:
            self.instances[instance.instance_id] = instance
            self.sync_status[instance.instance_id] = SyncStatus.SYNCING
            self.replication_lag[instance.instance_id] = 0.0
            self.last_synced_position[instance.instance_id] = 0
            return True
        except Exception as e:
            print(f"❌ Błąd dodawania instancji: {e}")
            return False
    
    def remove_instance(self, instance_id: str) -> bool:
        """Usunięcie instancji"""
        if instance_id in self.instances:
            del self.instances[instance_id]
            del self.sync_status[instance_id]
            del self.replication_lag[instance_id]
            return True
        return False
    
    def get_master(self) -> Optional[DatabaseInstance]:
        """
        Pobranie master instancji
        
        Returns:
            Master instancja lub None
        """
        for instance in self.instances.values():
            if instance.role == 'master' and instance.is_active:
                return instance
        return None
    
    def get_slaves(self) -> List[DatabaseInstance]:
        """Pobranie listy slave instancji"""
        return [inst for inst in self.instances.values() 
                if inst.role == 'slave' and inst.is_active]
    
    def write_to_binlog(self,
                       query: str,
                       database: str,
                       transaction_id: int) -> BinlogEntry:
        """
        Zapis do binlogu
        
        Args:
            query: SQL query
            database: Nazwa bazy
            transaction_id: ID transakcji
            
        Returns:
            BinlogEntry: Dodany wpis
        """
        entry_id = f"binlog-{len(self.binlog)}"
        checksum = self._calculate_checksum(query)
        
        entry = BinlogEntry(
            entry_id=entry_id,
            timestamp=datetime.now(),
            query=query,
            database=database,
            transaction_id=transaction_id,
            checksum=checksum,
            size_bytes=len(query.encode())
        )
        
        self.binlog.append(entry)
        return entry
    
    def _calculate_checksum(self, data: str) -> str:
        """Kalkulacja checksumu"""
        import hashlib
        return hashlib.md5(data.encode()).hexdigest()
    
    def replicate_binlog_to_slaves(self) -> Dict[str, bool]:
        """
        Replikacja binlogu na slave instancje
        
        Returns:
            Dict: Status replikacji dla każdej slave
        """
        results = {}
        master = self.get_master()
        
        if not master:
            return results
        
        slaves = self.get_slaves()
        
        for slave in slaves:
            try:
                # Symulacja replikacji
                last_synced = self.last_synced_position.get(slave.instance_id, 0)
                new_entries = list(self.binlog)[last_synced:]
                
                if new_entries:
                    # Zastosuj wpisy na slave
                    for entry in new_entries:
                        # Symulacja: uruchamianie query na slave
                        time.sleep(0.001)  # Symulacja opóźnienia
                    
                    # Aktualizacja pozycji
                    self.last_synced_position[slave.instance_id] = len(self.binlog)
                    self.sync_status[slave.instance_id] = SyncStatus.IN_SYNC
                    self.replication_lag[slave.instance_id] = 0.0
                    results[slave.instance_id] = True
                else:
                    self.sync_status[slave.instance_id] = SyncStatus.IN_SYNC
                    results[slave.instance_id] = True
                
            except Exception as e:
                self.sync_status[slave.instance_id] = SyncStatus.OUT_OF_SYNC
                results[slave.instance_id] = False
                print(f"❌ Błąd replikacji na {slave.instance_id}: {e}")
        
        return results
    
    def check_sync_status(self) -> Dict[str, Dict]:
        """Sprawdzenie statusu synchronizacji"""
        status_report = {}
        
        for instance_id, instance in self.instances.items():
            status_report[instance_id] = {
                'instance_id': instance_id,
                'role': instance.role,
                'sync_status': self.sync_status[instance_id].value,
                'replication_lag_seconds': self.replication_lag[instance_id],
                'last_synced_position': self.last_synced_position[instance_id],
                'is_active': instance.is_active
            }
        
        return status_report
    
    def perform_heartbeat(self) -> Dict[str, bool]:
        """Wykonanie heartbeat'u dla wszystkich instancji"""
        heartbeat_results = {}
        
        for instance_id, instance in self.instances.items():
            try:
                # Symulacja heartbeat'u
                instance.last_heartbeat = datetime.now()
                heartbeat_results[instance_id] = True
                
                # Sprawdzenie czy instancja nie ma timeout'u
                time_since_heartbeat = (datetime.now() - instance.last_heartbeat).total_seconds()
                if time_since_heartbeat > 30:  # 30 seconds timeout
                    instance.is_active = False
                    heartbeat_results[instance_id] = False
                
            except Exception as e:
                heartbeat_results[instance_id] = False
                print(f"❌ Heartbeat failed na {instance_id}: {e}")
        
        return heartbeat_results
    
    def get_replication_stats(self) -> Dict:
        """Pobranie statystyk replikacji"""
        binlog_size = sum(e.size_bytes for e in self.binlog)
        total_lag = sum(self.replication_lag.values())
        
        return {
            'mode': self.replication_mode.value,
            'total_instances': len(self.instances),
            'active_instances': sum(1 for i in self.instances.values() if i.is_active),
            'binlog_entries': len(self.binlog),
            'binlog_size_bytes': binlog_size,
            'average_lag_seconds': total_lag / len(self.instances) if self.instances else 0,
            'uptime_seconds': (datetime.now() - self.created_at).total_seconds()
        }


class ConflictResolver:
    """Resolver konfliktów dla Multi-Master replikacji"""
    
    def __init__(self, strategy: str = "last_write_wins"):
        """
        Inicjalizacja resolver'a konfliktów
        
        Args:
            strategy: Strategia: 'last_write_wins', 'version_vector', 'custom_logic'
        """
        self.strategy = strategy
        self.version_vectors: Dict[str, Dict] = {}
        self.conflict_history: List[Dict] = []
        
    def detect_conflict(self, 
                       instance_id: str,
                       row_id: str,
                       local_version: int,
                       remote_version: int) -> bool:
        """
        Detekcja konfliktu
        
        Args:
            instance_id: ID instancji
            row_id: ID wiersza
            local_version: Wersja lokalna
            remote_version: Wersja zdalna
            
        Returns:
            bool: Czy doszło do konfliktu
        """
        return local_version != remote_version
    
    def resolve_conflict(self,
                        row_id: str,
                        local_data: Dict,
                        remote_data: Dict) -> Dict:
        """
        Rozwiązanie konfliktu
        
        Args:
            row_id: ID wiersza
            local_data: Dane lokalne
            remote_data: Dane zdalne
            
        Returns:
            Dict: Rozwiązane dane
        """
        if self.strategy == "last_write_wins":
            # Ostatni zapis wygrywa
            if local_data.get('timestamp', 0) > remote_data.get('timestamp', 0):
                resolved = local_data
            else:
                resolved = remote_data
        
        elif self.strategy == "version_vector":
            # Porównanie version vector'ów
            resolved = self._resolve_by_version_vector(local_data, remote_data)
        
        else:
            # Domyślnie: ostatni zapis
            resolved = local_data
        
        # Zapis do historii
        self.conflict_history.append({
            'row_id': row_id,
            'timestamp': datetime.now().isoformat(),
            'resolved_to': resolved,
            'strategy': self.strategy
        })
        
        return resolved
    
    def _resolve_by_version_vector(self, local_data: Dict, remote_data: Dict) -> Dict:
        """Rozwiązanie używając version vector"""
        # Symplifikacja: porównanie versji
        if local_data.get('version', 0) > remote_data.get('version', 0):
            return local_data
        return remote_data
    
    def get_conflict_stats(self) -> Dict:
        """Statystyki konfliktów"""
        return {
            'total_conflicts': len(self.conflict_history),
            'strategy': self.strategy,
            'recent_conflicts': self.conflict_history[-10:] if self.conflict_history else []
        }


class FailoverManager:
    """Manager failover'u dla DB"""
    
    def __init__(self, replication: DatabaseReplication):
        """Inicjalizacja Failover Manager'a"""
        self.replication = replication
        self.failover_history: List[Dict] = []
        self.promoted_slaves: List[str] = []
        
    def detect_master_failure(self) -> bool:
        """Detekcja utraty Master instancji"""
        master = self.replication.get_master()
        
        if not master:
            return False
        
        # Heartbeat check
        time_since_heartbeat = (datetime.now() - master.last_heartbeat).total_seconds()
        
        if time_since_heartbeat > 30:  # 30 seconds timeout
            return True
        
        return False
    
    def promote_slave_to_master(self, slave_id: str) -> bool:
        """
        Promocja slave na master
        
        Args:
            slave_id: ID slave do promocji
            
        Returns:
            bool: Czy promocja powiodła się
        """
        if slave_id not in self.replication.instances:
            return False
        
        try:
            slave = self.replication.instances[slave_id]
            
            # Zmiana roli
            slave.role = 'master'
            
            # Zatrzymanie replikacji
            self.replication.sync_status[slave_id] = SyncStatus.IN_SYNC
            
            # Zapis do historii
            self.failover_history.append({
                'promoted_slave': slave_id,
                'timestamp': datetime.now().isoformat(),
                'status': 'success'
            })
            
            self.promoted_slaves.append(slave_id)
            return True
            
        except Exception as e:
            print(f"❌ Błąd promocji slave: {e}")
            return False
    
    def automatic_failover(self) -> bool:
        """Automatyczne failover"""
        if not self.detect_master_failure():
            return False
        
        slaves = self.replication.get_slaves()
        if not slaves:
            return False
        
        # Promuj najlepszą slave (z najmniejszym lag'em)
        best_slave = min(slaves, 
                        key=lambda s: self.replication.replication_lag.get(s.instance_id, float('inf')))
        
        return self.promote_slave_to_master(best_slave.instance_id)
    
    def get_failover_history(self) -> List[Dict]:
        """Pobranie historii failover'ów"""
        return self.failover_history


def test_database_replication():
    """Test Database Replication"""
    print("\n🔧 Testowanie Database Replication...")
    
    # Inicjalizacja replikacji
    repl = DatabaseReplication(ReplicationMode.MASTER_SLAVE)
    
    # Dodawanie instancji
    master = DatabaseInstance(
        instance_id='db-master-1',
        host='db-master.dark8.local',
        port=5432,
        role='master'
    )
    repl.add_instance(master)
    
    for i in range(2):
        slave = DatabaseInstance(
            instance_id=f'db-slave-{i}',
            host=f'db-slave-{i}.dark8.local',
            port=5432,
            role='slave'
        )
        repl.add_instance(slave)
    
    print(f"✅ Instancji dodane: {len(repl.instances)}")
    
    # Zapis do binlogu
    for i in range(5):
        entry = repl.write_to_binlog(
            query=f"INSERT INTO users VALUES ({i})",
            database="dark8_db",
            transaction_id=i
        )
        print(f"✅ Binlog entry: {entry.entry_id}")
    
    # Replikacja
    results = repl.replicate_binlog_to_slaves()
    print(f"✅ Replikacja: {results}")
    
    # Statystyki replikacji
    stats = repl.get_replication_stats()
    print(f"✅ Stats: {json.dumps(stats, indent=2)}")
    
    # Failover
    failover = FailoverManager(repl)
    can_failover = failover.detect_master_failure()
    print(f"✅ Master failure detected: {can_failover}")


if __name__ == '__main__':
    test_database_replication()
