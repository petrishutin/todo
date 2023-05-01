from fastapi import APIRouter, HTTPException

from app.schemas import Attachment, AttachmentIn


attachments_router = APIRouter(prefix="/attachments")


@attachments_router.post("/")
async def create_attachment():
    pass