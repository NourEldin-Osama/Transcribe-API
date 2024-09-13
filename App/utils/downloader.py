import os
import httpx
import tempfile
from bs4 import BeautifulSoup
from rich.progress import Progress, BarColumn, DownloadColumn, TextColumn, TimeRemainingColumn, TransferSpeedColumn

async def download_soundcloud_track(link):
    """
    Download a SoundCloud track and save it to a temporary file using a rich progress bar.

    :param link: SoundCloud track URL
    :return: Path to the temporary audio file
    """
    base_url = "https://sclouddownloader.net"
    download_url = f"{base_url}/download-sound-track"

    headers = {
        "authority": "sclouddownloader.net",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://sclouddownloader.net",
        "referer": "https://sclouddownloader.net/",
        "user-agent": "Mozilla/5.0"
    }

    async with httpx.AsyncClient() as client:
        # Get the initial page
        response = await client.get(base_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        csrf_token = soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]
        headers["cookie"] = f"csrftoken={csrf_token}"

        # Prepare the form data with the CSRF token and track URL
        data = {"csrfmiddlewaretoken": csrf_token, "url": link}
        response = await client.post(download_url, data=data, headers=headers)

        if response.status_code == 200:
            # Extract the download link and track title
            soup = BeautifulSoup(response.text, "html.parser")
            track_title = soup.find("p", {"id": "trackTitle"}).text.replace(" ", "_").replace("/", "_")
            download_link = soup.find("a", {"id": "trackLink"})["href"]

            # Create a temporary file to store the audio
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")

            # Use rich progress to display the download progress
            with Progress(
                TextColumn("[bold blue]{task.description}"),
                BarColumn(),
                DownloadColumn(),
                TransferSpeedColumn(),
                TimeRemainingColumn(),
            ) as progress:
                task_id = progress.add_task(f"Downloading {track_title}", total=None)

                async with client.stream("GET", download_link) as response:
                    total_size = int(response.headers.get("content-length", 0))
                    progress.update(task_id, total=total_size)
                    
                    with open(temp_file.name, "wb") as f:
                        async for chunk in response.aiter_bytes(chunk_size=8192):
                            f.write(chunk)
                            progress.update(task_id, advance=len(chunk))

            # Return the path to the temporary file
            return temp_file.name
        else:
            raise Exception(f"Failed to download track from {link}. Status code: {response.status_code}")
