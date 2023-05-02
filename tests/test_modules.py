import uuid

import pytest

import os

print(os.getcwd())

from app.filestorage import FileStorage
from app.settings import get_settings


@pytest.mark.asyncio
async def test_upload_download_delete():
    storage = FileStorage(get_settings())
    uid = await storage.upload(b"test")
    assert uuid.UUID(uid), uid
    assert await storage.download(uid) == b"test"
    await storage.delete(uid)
