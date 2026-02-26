from fastapi import FastAPI
from .api.routers import learning_sessions

app = FastAPI()

app.include_router(learning_sessions.router)

app.get("/")
async def root():
	return {"message": "Bienvenue chez Simplon !"}