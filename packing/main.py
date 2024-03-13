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
# Ensure the upload directory exists
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@app.post("/uploadfile")
async def create_upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # Check if the file is a tar.gz and extract it
    if file.filename.endswith(".tar.gz"):
        with tarfile.open(file_location, "r:gz") as tar:
            tar.extractall(path=UPLOAD_DIRECTORY)
        # Delete the compressed file after extraction
        os.remove(file_location)

    return {"info": f"file '{file.filename}' saved and extracted at '{UPLOAD_DIRECTORY}'"}

@app.get("/")
async def main():
    content = """
<form action="/uploadfile/" enctype="multipart/form-data" method="post">
<input name="file" type="file">
<input type="submit">
</form>
"""
    return HTMLResponse(content=content)

