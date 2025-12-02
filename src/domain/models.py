from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class FileMetadata:
    hash: str
    owner: str