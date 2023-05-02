from fastapi import APIRouter, UploadFile, Depends

from app.schemas import Attachment
from app.filestorage import FileStorage

attachments_router = APIRouter(prefix="/files")


def file_storage():
    return FileStorage()


@attachments_router.post("/{user_id}/{todo_id}")
async def create_attachment(
        file: UploadFile = None,
        user_id: str = None,
        storage: FileStorage = Depends(file_storage),
        todo_id: str | None = None
):
    attachment = await Attachment.from_upload_file(file, user_id, todo_id)
