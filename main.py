from fastapi import FastAPI
from routers import auth, users, cars
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(cars.router)