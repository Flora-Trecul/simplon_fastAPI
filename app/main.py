from fastapi import FastAPI
from fastapi_pagination import add_pagination
from app.api.routers import courses, learning_sessions, users

app = FastAPI(title="Simplon API")
add_pagination(app)

@app.get('/')
def welcome():
    return {'message': 'Bienvenue sur l\'application FastAPI de Simplon.'}
  
app.include_router(users.router)
app.include_router(courses.router)
app.include_router(learning_sessions.router)
