import httpx

from async_retrying_ng import retry


class FileStorage:
    def __init__(self, settings):
        self.file_storage_url = settings.FILE_STORAGE_URL

    @retry(attempts=5, timeout=0.1)
    async def upload(self, file_data: bytes) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(self.file_storage_url, files={"file": file_data})
            return response.json()

    @retry(attempts=5, timeout=0.1)
    async def download(self, filename):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.file_storage_url}/{filename}")
            return response.content

    @retry(attempts=5, timeout=0.1)
    async def delete(self, filename):
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{self.file_storage_url}/{filename}")
            return response.content
