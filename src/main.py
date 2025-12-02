from fastapi import FastAPI
from src.infrastructure.api.routes import router
from src.infrastructure.storage import LocalFileStorage
from src.infrastructure.db import SQLiteFileRepository
from src.application.file_service import FileService

app = FastAPI(title="File Storage API (Clean Architecture)")

@app.on_event("startup")
def startup():
    storage = LocalFileStorage()
    repo = SQLiteFileRepository()
    app.state.file_service = FileService(storage, repo)

app.include_router(router)