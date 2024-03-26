from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import os
import shutil
import tarfile
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(root_path="/api-upload")
# app = FastAPI(openapi_prefix="/api-upload")


# Directory where files will be stored
UPLOAD_DIRECTORY = "projects/ui-automate-regression/reports"
LARGE_UPLOAD_DIRECTORY = "projects/api-automated-regression/reports"
# Ensure the upload directories exist
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
os.makedirs(LARGE_UPLOAD_DIRECTORY, exist_ok=True)

@app.post("/uploadfile")
async def create_upload_file(file: UploadFile = File(...)):
    return await save_and_extract_file(file, UPLOAD_DIRECTORY)

@app.post("/uploadfile-large")
async def create_upload_file_large(file: UploadFile = File(...)):
    return await save_and_extract_file(file, LARGE_UPLOAD_DIRECTORY)

async def save_and_extract_file(file: UploadFile, upload_dir: str):
    file_location = os.path.join(upload_dir, file.filename)
    with open(file_location, "wb") as buffer:
        # Use shutil.copyfileobj to handle large file efficiently
        shutil.copyfileobj(file.file, buffer)

    # Check if the file is a tar.gz and extract it
    if file.filename.endswith(".tar.gz"):
        with tarfile.open(file_location, "r:gz") as tar:
            tar.extractall(path=upload_dir)
        # Delete the compressed file after extraction
        os.remove(file_location)

    return {"info": f"file '{file.filename}' saved and extracted at '{upload_dir}'"}


@app.get("/")
async def main():
    content = """
<form action="/uploadfile/" enctype="multipart/form-data" method="post">
<input name="file" type="file">
<input type="submit">
</form>
"""
    return HTMLResponse(content=content)

