from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, UploadFile

from app.filestorage import FileStorage
from app.schemas import Attachment
from app.settings import Settings, get_settings

attachments_router = APIRouter(prefix="/attachments")


def file_storage():
    return FileStorage(get_settings())


@attachments_router.post("/{user_id}", status_code=201)
async def upload_data(
    user_id: PydanticObjectId,
    file: UploadFile,
    client: FileStorage = Depends(file_storage),
    setting: Settings = Depends(get_settings),
):
    attachment = await Attachment.create(Attachment.from_upload_file(file, user_id))
    file_uid = await client.upload(file)
    attachment.file_uid = file_uid
    attachment.file_url = f"{setting.HOST_NAME}/files/{file_uid}"
    await attachment.save()
    return attachment
