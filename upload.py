from fastapi import UploadFile
from app.services.pdf_parser import extract_text_from_pdf_bytes
from azure.storage.blob import BlobServiceClient
import os

AZURE_STORAGE_KEY = os.getenv("AZURE_STORAGE_KEY")
AZURE_STORAGE_ACCOUNT = os.getenv("AZURE_STORAGE_ACCOUNT")
AZURE_CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME")

blob_service_client = BlobServiceClient(
    f"https://{AZURE_STORAGE_ACCOUNT}.blob.core.windows.net",
    credential=AZURE_STORAGE_KEY
)

@router.post("/upload")
async def upload_pdf(file: UploadFile):
    blob_client = blob_service_client.get_blob_client(
        container=AZURE_CONTAINER_NAME,
        blob=file.filename
    )
    content = await file.read()
    blob_client.upload_blob(content, overwrite=True)

    # Extract text from uploaded PDF
    extracted_text = extract_text_from_pdf_bytes(content)

    return {"filename": file.filename, "text": extracted_text[:500]}  # Preview first 500 chars
