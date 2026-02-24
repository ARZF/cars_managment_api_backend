from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from routers import auth, users, cars
from database import Base, engine, SessionLocal
from Models import Car

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.on_event("startup")
@repeat_every(seconds=3600)
def delete_rejected_cars_task() -> None:
    db = SessionLocal()
    try:
        db.query(Car).filter(Car.rejection_count >= 3).delete(synchronize_session=False)
        db.commit()
    finally:
        db.close()


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(cars.router)