from abc import ABC, abstractmethod
from typing import Optional
from .models import FileMetadata

class FileRepository(ABC):
    @abstractmethod
    def add_owner(self, owner: str, file_hash: str) -> None:
        pass

    @abstractmethod
    def is_owned_by(self, owner: str, file_hash: str) -> bool:
        pass

    @abstractmethod
    def remove_owner(self, owner: str, file_hash: str) -> bool:
        pass

    @abstractmethod
    def has_any_owner(self, file_hash: str) -> bool:
        pass

class FileStorage(ABC):
    @abstractmethod
    def save(self, file_hash: str, content: bytes) -> None:
        pass

    @abstractmethod
    def load(self, file_hash: str) -> bytes:
        pass

    @abstractmethod
    def delete(self, file_hash: str) -> bool:
        pass

    @abstractmethod
    def exists(self, file_hash: str) -> bool:
        pass