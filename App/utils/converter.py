import os
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

def save_transcript_to_word(transcript: str, word_folder: str, link_id: int, language: str = 'ar') -> str:
    """
    Save the transcript to a Word document directly.

    :param transcript: The transcript string to save to Word.
    :param word_folder: The folder where the Word file will be saved.
    :param link_id: The unique ID of the SoundCloud link (used for file naming).
    :param language: The language of the transcript, default is 'en' (English).
    :return: Path to the saved Word document.
    """
    # Ensure the Word folder exists
    os.makedirs(word_folder, exist_ok=True)

    # Construct the full path for the Word file
    word_file_path = os.path.join(word_folder, f"transcript_{link_id}.docx")

    # Create a new Document
    doc = Document()

    # Add each line of the transcript to the Word document
    for line in transcript.splitlines():
        paragraph = doc.add_paragraph(line)
        # If the language is Arabic, set the paragraph alignment to the right
        # and enable right-to-left text direction.
        if language == 'ar':
            paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
            paragraph.paragraph_format.right_to_left = True

    # Save the Word document
    doc.save(word_file_path)

    return word_file_path
