import os
from pathlib import Path
from typing import BinaryIO
from src.domain.interfaces import FileStorage

class LocalFileStorage(FileStorage):
    def __init__(self, base_path: str = "store"):
        self._base = Path(base_path)

    def _get_path(self, file_hash: str) -> Path:
        if not all(c in "0123456789abcdef" for c in file_hash) or len(file_hash) != 64:
            raise ValueError("Invalid hash")
        return self._base / file_hash[:2] / file_hash

    def save(self, file_hash: str, content: bytes) -> None:
        path = self._get_path(file_hash)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)

    def load(self, file_hash: str) -> bytes:
        path = self._get_path(file_hash)
        if not path.exists():
            raise FileNotFoundError()
        return path.read_bytes()

    def delete(self, file_hash: str) -> bool:
        path = self._get_path(file_hash)
        if not path.exists():
            return False
        path.unlink()
        try:
            path.parent.rmdir()
        except OSError:
            pass
        return True

    def exists(self, file_hash: str) -> bool:
        return self._get_path(file_hash).exists()