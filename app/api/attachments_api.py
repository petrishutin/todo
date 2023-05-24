from fastapi import APIRouter, Depends, HTTPException, Response, UploadFile

from app.auth_utils import get_current_user_id
from app.filestorage import FileStorage
from app.schemas import Attachment
from app.settings import Settings, get_settings

attachments_router = APIRouter(prefix="/attachments")


def file_storage():
    return FileStorage(get_settings())


@attachments_router.post("", status_code=201)
async def upload_data(
    file: UploadFile,
    client: FileStorage = Depends(file_storage),
    setting: Settings = Depends(get_settings),
    user_id=Depends(get_current_user_id),
):
    attachment = await Attachment.create(await Attachment.from_upload_file(file, user_id))
    file_uid = await client.upload(file.file)  # type: ignore
    attachment.file_uid = file_uid
    attachment.file_url = f"{setting.HOST_NAME}/api/v1/attachments/{file_uid}"
    await attachment.save()
    return attachment


@attachments_router.get("/{file_uid}")
async def download_attachment(
    file_uid: str, client: FileStorage = Depends(file_storage), user_id=Depends(get_current_user_id)
):
    file_metadata = await Attachment.find_one({"file_uid": file_uid})
    if not file_metadata:
        raise HTTPException(status_code=404)
    if str(file_metadata.user_id) != user_id:
        raise HTTPException(status_code=403, detail="You don't have access to this file")
    return Response(content=await client.download(file_uid), media_type=file_metadata.file_mime_type)  # type: ignore
