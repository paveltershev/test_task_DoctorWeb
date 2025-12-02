from typing import Optional
from src.domain.models import FileMetadata
from src.domain.interfaces import FileRepository, FileStorage
from src.domain.exceptions import FileNotFoundError, FileNotOwnedException

class FileService:
    def __init__(self, storage: FileStorage, repo: FileRepository):
        self._storage = storage
        self._repo = repo

    def upload(self, owner: str, content: bytes) -> str:
        import hashlib
        file_hash = hashlib.sha256(content).hexdigest()
        if not self._storage.exists(file_hash):
            self._storage.save(file_hash, content)
        self._repo.add_owner(owner, file_hash)
        return file_hash

    def delete(self, owner: str, file_hash: str) -> None:
        if not self._storage.exists(file_hash):
            raise FileNotFoundError()
        if not self._repo.is_owned_by(owner, file_hash):
            raise FileNotOwnedException()
        self._repo.remove_owner(owner, file_hash)
        if not self._repo.has_any_owner(file_hash):
            self._storage.delete(file_hash)

    def download(self, file_hash: str) -> bytes:
        if not self._storage.exists(file_hash):
            raise FileNotFoundError()
        return self._storage.load(file_hash)