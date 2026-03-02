from fastapi import FastAPI

from app.api.routers import courses, learning_sessions, users #, inscriptions

app = FastAPI(title="Simplon API")

@app.get('/')
def welcome():
    return {'message': 'Bienvenue sur l\'application FastAPI de Simplon.'}
  
app.include_router(users.router)
app.include_router(courses.router)
# app.include_router(inscriptions.router)
app.include_router(learning_sessions.router)
