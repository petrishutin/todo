from fastapi import APIRouter

from app.filestorage import FileStorage

attachments_router = APIRouter(prefix="/files")


def file_storage():
    return FileStorage()
