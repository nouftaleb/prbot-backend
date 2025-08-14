from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import AzureOpenAI
from app.config import AZURE_OPENAI_KEY, AZURE_OPENAI_ENDPOINT, EMBEDDING_MODEL

router = APIRouter()

client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    api_version="2023-05-15",
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

class EmbedRequest(BaseModel):
    text: str

@router.post("/embed")
def embed_text(payload: EmbedRequest):
    try:
        response = client.embeddings.create(
            input=payload.text,
            model=EMBEDDING_MODEL
        )
        return {"embedding": response.data[0].embedding}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
