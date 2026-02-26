from fastapi import FastAPI
from app.api.routers import courses

app = FastAPI(title="Simplon API")

app.include_router(courses.router)