import os
import asyncio
from fastapi import BackgroundTasks
from sqlmodel import Session
from .utils.downloader import download_soundcloud_track
from .utils.transcriber import transcribe_audio
from .utils.converter import save_transcript_to_word
from .crud import update_soundcloud_link
from .schemas import SoundCloudLinkUpdate
from .models import DownloadStatus


# Path configuration
WORD_FOLDER = "word_files"

# Ensure directories exist
os.makedirs(WORD_FOLDER, exist_ok=True)

async def process_soundcloud_link(link_id: int, url: str, session: Session, background_tasks: BackgroundTasks):
    """
    Main function that runs the download, transcription, and conversion as background tasks.
    """
    # Step 1: Update status to 'downloading'
    background_tasks.add_task(update_status, session, link_id, DownloadStatus.downloading)

    # Step 2: Download the track
    try:
        audio_file_path = await download_soundcloud_track(url)
    except Exception as e:
        # Handle download failure
        background_tasks.add_task(update_status, session, link_id, DownloadStatus.failed)
        return
    
    # Step 3: Update status to 'transcribing'
    background_tasks.add_task(update_status, session, link_id, DownloadStatus.transcribing)

    # Step 4: Transcribe the audio
    try:
        transcript = await transcribe_audio(audio_file_path)
    except Exception as e:
        background_tasks.add_task(update_status, session, link_id, DownloadStatus.failed)
        return
    finally:
        # Clean up the temporary file after transcription is complete
        os.remove(audio_file_path)

    # Step 5: Update status to 'finished'
    word_file_path = save_transcript_to_word(transcript, WORD_FOLDER, link_id)
    background_tasks.add_task(update_status_and_file_path, session, link_id, DownloadStatus.finished, word_file_path)



async def update_status(session: Session, link_id: int, status: DownloadStatus):
    """
    Helper function to update the status of a SoundCloud link in the database.
    """
    link_update = SoundCloudLinkUpdate(status=status)
    update_soundcloud_link(session, link_id, link_update)


async def update_status_and_file_path(session: Session, link_id: int, status: DownloadStatus, file_path: str):
    """
    Helper function to update both the status and the file path of a SoundCloud link in the database.
    """
    link_update = SoundCloudLinkUpdate(status=status, word_file_path=file_path)
    update_soundcloud_link(session, link_id, link_update)
