from beanie import Document, PydanticObjectId
from fastapi import UploadFile
from pydantic import BaseModel


class AttachmentIn(BaseModel):
    user_id: str
    todo_id: str | None = None
    file_name: str
    file_type: str
    file_size: int


class Attachment(Document):
    user_id: str
    todo_id: str | None = None
    file_name: str
    file_type: str
    file_size: int

    @staticmethod
    def from_upload_file(file: UploadFile, user_id: str, todo_id: str | None = None):
        return Attachment(
            user_id=PydanticObjectId(user_id),
            todo_id=PydanticObjectId(todo_id),
            file_name=file.filename,
            file_type=file.content_type,
            file_size=file.size,
        )

    class Settings:
        name = "Attachments"
