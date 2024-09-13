from pydantic import BaseModel

from .models import DownloadStatus


# Pydantic model for creating a new SoundCloud link
class SoundCloudLinkCreate(BaseModel):
    url: str

# Pydantic model for reading the SoundCloud link
class SoundCloudLinkRead(BaseModel):
    id: int
    url: str
    status: DownloadStatus
    word_file_path: str | None = None

    class Config:
        orm_mode = True

# Pydantic model for updating a SoundCloud link
class SoundCloudLinkUpdate(BaseModel):
    status: DownloadStatus | None = None
    word_file_path: str | None = None
