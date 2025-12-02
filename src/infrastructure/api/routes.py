from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status
from fastapi.responses import Response

from src.application.file_service import FileService
from src.infrastructure.auth import authenticate, AuthenticationError
from src.domain.exceptions import FileNotFoundError, FileNotOwnedException

router = APIRouter()

def get_file_service(request) -> FileService:
    return request.app.state.file_service

@router.post("/upload")
async def upload(
    file: UploadFile = File(...),
    username: str = Depends(authenticate),
    service: FileService = Depends(get_file_service)
):
    try:
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="Empty file")
        file_hash = service.upload(username, content)
        return {"hash": file_hash}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Upload failed")

@router.delete("/delete/{file_hash}", status_code=204)
async def delete_file(
    file_hash: str,
    username: str = Depends(authenticate),
    service: FileService = Depends(get_file_service)
):
    try:
        service.delete(username, file_hash)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except FileNotOwnedException:
        raise HTTPException(status_code=403, detail="Not your file")
    except Exception:
        raise HTTPException(status_code=500, detail="Delete failed")

@router.get("/download/{file_hash}")
async def download(
    file_hash: str,
    service: FileService = Depends(get_file_service)
):
    try:
        content = service.download(file_hash)
        return Response(content, media_type="application/octet-stream")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception:
        raise HTTPException(status_code=500, detail="Download failed")