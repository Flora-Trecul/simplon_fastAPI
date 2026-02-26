from fastapi import FastAPI
from app.api.routers import users 

app = FastAPI()

@app.get('/')
def welcome():
    return {'message': 'Welcome to my FastAPI application'}

app.include_router(users.router)