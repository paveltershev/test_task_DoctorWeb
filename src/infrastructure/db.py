import sqlite3
import threading
from src.domain.interfaces import FileRepository

class SQLiteFileRepository(FileRepository):
    def __init__(self, db_path: str = "filestore.db"):
        self._db_path = db_path
        self._lock = threading.RLock()
        self._init_db()

    def _init_db(self):
        with self._lock:
            conn = sqlite3.connect(self._db_path, check_same_thread=False)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS file_owners (
                    username TEXT NOT NULL,
                    file_hash TEXT NOT NULL,
                    PRIMARY KEY (username, file_hash)
                )
            """)
            conn.commit()
            conn.close()

    def add_owner(self, owner: str, file_hash: str) -> None:
        with self._lock:
            conn = sqlite3.connect(self._db_path, check_same_thread=False)
            conn.execute("INSERT OR IGNORE INTO file_owners VALUES (?, ?)", (owner, file_hash))
            conn.commit()
            conn.close()

    def is_owned_by(self, owner: str, file_hash: str) -> bool:
        with self._lock:
            conn = sqlite3.connect(self._db_path, check_same_thread=False)
            cur = conn.execute("SELECT 1 FROM file_owners WHERE username = ? AND file_hash = ?", (owner, file_hash))
            result = cur.fetchone() is not None
            conn.close()
            return result

    def remove_owner(self, owner: str, file_hash: str) -> bool:
        with self._lock:
            conn = sqlite3.connect(self._db_path, check_same_thread=False)
            cur = conn.execute("DELETE FROM file_owners WHERE username = ? AND file_hash = ?", (owner, file_hash))
            deleted = cur.rowcount > 0
            conn.commit()
            conn.close()
            return deleted

    def has_any_owner(self, file_hash: str) -> bool:
        with self._lock:
            conn = sqlite3.connect(self._db_path, check_same_thread=False)
            cur = conn.execute("SELECT 1 FROM file_owners WHERE file_hash = ? LIMIT 1", (file_hash,))
            result = cur.fetchone() is not None
            conn.close()
            return result