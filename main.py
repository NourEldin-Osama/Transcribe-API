from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException
from sqlmodel import Session
from App.database import create_db_and_tables, get_session
from App.schemas import SoundCloudLinkCreate, SoundCloudLinkRead
from App.crud import create_soundcloud_link, get_all_links, get_link_by_id
from App.tasks import process_soundcloud_link

app = FastAPI()

# Initialize the database and create tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Endpoint for creating a new SoundCloud link and processing it in the background
@app.post("/soundcloud-links/", response_model=SoundCloudLinkRead)
def create_link(link: SoundCloudLinkCreate, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    # Create a new SoundCloud link in the database
    new_link = create_soundcloud_link(session, link.url)
    
    # Start background tasks to process the link (download, transcribe, and save to Word)
    background_tasks.add_task(process_soundcloud_link, new_link.id, link.url, session, background_tasks)

    return new_link

# Endpoint for getting all SoundCloud links and their statuses
@app.get("/soundcloud-links/", response_model=list[SoundCloudLinkRead])
def list_links(session: Session = Depends(get_session)):
    return get_all_links(session)

# Endpoint for getting the status of a specific SoundCloud link
@app.get("/soundcloud-links/{link_id}", response_model=SoundCloudLinkRead)
def get_link_status(link_id: int, session: Session = Depends(get_session)):
    link = get_link_by_id(session, link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link
