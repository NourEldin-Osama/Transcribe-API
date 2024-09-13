from fastapi import HTTPException
from sqlmodel import Session, select

from .models import DownloadStatus, SoundCloudLink
from .schemas import SoundCloudLinkUpdate


# Function to add a new SoundCloud link to the database
def create_soundcloud_link(session: Session, url: str) -> SoundCloudLink:
    link = SoundCloudLink(url=url, status=DownloadStatus.pending)
    session.add(link)
    session.commit()
    session.refresh(link)
    return link


# Function to get all links
def get_all_links(session: Session):
    statement = select(SoundCloudLink)
    return session.exec(statement).all()


# Function to get a specific SoundCloud link by ID
def get_link_by_id(session: Session, link_id: int) -> SoundCloudLink:
    return session.get(SoundCloudLink, link_id)


# Function to update the status or word file path or both
def update_soundcloud_link(
    session: Session, link_id: int, link_update: SoundCloudLinkUpdate
) -> SoundCloudLink:
    # Get the existing SoundCloud link from the DB
    db_link = session.get(SoundCloudLink, link_id)
    if not db_link:
        raise HTTPException(status_code=404, detail="SoundCloud link not found")

    # Get the fields to update
    link_data = link_update.model_dump(exclude_unset=True)

    db_link.sqlmodel_update(link_data)

    session.add(db_link)
    session.commit()
    session.refresh(db_link)

    return db_link
