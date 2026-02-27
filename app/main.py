from fastapi import FastAPI

from app.api.routers import courses, inscriptions, learning_sessions, users

app = FastAPI(title="Simplon API")

@app.get('/')
def welcome():
    return {'message': 'Welcome to my FastAPI application'}
  
app.include_router(users.router)
app.include_router(courses.router)
app.include_router(inscriptions.router)
app.include_router(learning_sessions.router)
