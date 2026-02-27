from fastapi import FastAPI
from app.api.routers import courses, inscriptions, learning_sessions

app = FastAPI(title="Simplon API")

app.include_router(courses.router)
app.include_router(inscriptions.router)
app.include_router(learning_sessions.router)