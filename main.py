from fastapi import FastAPI, Depends, HTTPException, status , Path, Request 
from fastapi import FastAPI, File, UploadFile
import pandas as pd
from typing import Annotated, Union
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from google.cloud import storage
import os 

app = FastAPI()

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] ="/app/gcp_credentials.json"
# Get values from environment variables
PROJECT_ID = os.environ.get("PROJECT_ID")
BUCKET_NAME = os.environ.get("BUCKET_NAME")

if not PROJECT_ID or not BUCKET_NAME:
    raise ValueError("PROJECT_ID and BUCKET_NAME environment variables must be set.")

try:
    storage_client = storage.Client(project=PROJECT_ID)
    bucket = storage_client.bucket(BUCKET_NAME)
except Exception as e:
    print(f"Error initializing GCS client: {e}")
    exit(1)


# Initialize GCS client (do this outside of the route function for efficiency)
try:
    storage_client = storage.Client(project=PROJECT_ID)
    bucket = storage_client.bucket(BUCKET_NAME)
except Exception as e:
    print(f"Error initializing GCS client: {e}")
    # Handle the error appropriately, e.g., exit the application or return an error message.
    exit(1) # Or raise an exception if you want FastAPI to handle it.
    # raise HTTPException(status_code=500, detail=f"Error initializing GCS: {e}")

templates = Jinja2Templates(directory="frontend")


@app.get('/', response_class=HTMLResponse)
def image_upload(request: Request):
    result = "Please upload your image"
    return templates.TemplateResponse('form.html',context={'request': request,'result':result})



@app.post("/upload")  # Use POST for file uploads
async def upload_image(request: Request, file: UploadFile = File(...)): # Added file parameter
    try:
        if not file:
            raise HTTPException(status_code=400, detail="No file uploaded")

        # Check file type (important for security)
        allowed_types = ["image/jpeg", "image/png"]
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG and PNG are allowed.")

        # Upload to GCS
        blob = bucket.blob(file.filename) # Use original filename
        contents = await file.read() # Read file contents as bytes
        blob.upload_from_string(contents, content_type=file.content_type) # Set Content-Type

        # Construct the public URL (optional, if you need it)
        public_url = blob.public_url

        return templates.TemplateResponse('form.html', context={'request': request, 'result': f"File '{file.filename}' uploaded successfully to GCS. Public URL: {public_url}"})

    except Exception as e:
        print(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail=f"File upload failed: {e}")



@app.get("/hello")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}