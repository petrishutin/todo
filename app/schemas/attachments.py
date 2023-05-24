from datetime import datetime

from beanie import Document, PydanticObjectId
from fastapi import UploadFile
from pydantic import BaseModel


class AttachmentIn(BaseModel):
    user_id: str
    file_name: str
    file_type: str
    file_size: int


class Attachment(Document):
    user_id: PydanticObjectId
    file_name: str | None = None
    file_mime_type: str
    file_size: int
    file_uid: str | None = None
    file_url: str | None = None
    created_at: datetime | None = None

    @staticmethod
    async def from_upload_file(
        file: UploadFile,
        user_id: PydanticObjectId,
    ):
        return Attachment(
            user_id=user_id,
            file_name=file.filename,
            file_mime_type=file.content_type,
            file_size=file.size,
            created_at=datetime.utcnow(),
        )

    class Settings:
        name = "Attachments"
