from sqlmodel import SQLModel, Field
from enum import Enum
from typing import Optional

# Enum to track the status of the process
class DownloadStatus(str, Enum):
    pending = "pending"
    downloading = "downloading"
    transcribing = "transcribing"
    finished = "finished"
    failed = "failed"

# SQLModel to track each SoundCloud link's progress
class SoundCloudLink(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str
    status: DownloadStatus = Field(default=DownloadStatus.pending)
    word_file_path: Optional[str] = None  # Path to the generated Word file
