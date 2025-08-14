from fastapi import FastAPI
from app.routes import embed

app = FastAPI()
app.include_router(embed.router)
