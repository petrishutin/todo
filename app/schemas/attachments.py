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
    file_name: str
    file_type: str
    file_size: int
    file_uid: str | None = None
    file_url: str | None = None

    @staticmethod
    def from_upload_file(
        file: UploadFile,
        user_id: PydanticObjectId,
    ):
        return Attachment(
            user_id=user_id,
            file_name=file.filename,
            file_type=file.content_type,
            file_size=file.size,
        )

    class Settings:
        name = "Attachments"
