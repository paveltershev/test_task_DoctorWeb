from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# хард код — только для демо (в production — хеши)
USER_DB = {"admin": "secret", "uploader": "pass123"}

security = HTTPBasic()

class AuthenticationError(Exception):
    """Инфраструктурное исключение — не часть бизнес-логики"""
    pass

def authenticate(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    if credentials.username not in USER_DB or USER_DB[credentials.username] != credentials.password:
        raise AuthenticationError()
    return credentials.username