from fastapi import APIRouter, Depends
from Models import Car, User
from schemas import CarRequest, CarResponse, RejectCarRequest
from depends import get_current_user, require_role
from fastapi import HTTPException
from sqlalchemy.orm import Session
from database import get_db
from typing import List

router = APIRouter(prefix="/cars", tags=["Cars"])

@router.get("/search/{plate_number}", response_model=CarResponse)
def search_car(
    plate_number: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    car = db.query(Car).filter(Car.plate_number == plate_number).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    return car

@router.post("/{car_id}/approve", response_model=CarResponse)
def approve_car(
    car_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    car = db.query(Car).filter(Car.id == car_id).first()
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")

    car.approved_count += 1
    db.commit()
    db.refresh(car)

    return car

@router.post("/{car_id}/reject", response_model=RejectCarRequest)
def reject_car(
    car_id: int,
    request: RejectCarRequest,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    car = db.query(Car).filter(Car.id == car_id).first()
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")

# 🔹 Admin only
@router.post("/register", response_model=CarResponse)
def register_car(
    car_data: CarRequest,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    existing_car = db.query(Car).filter(
        Car.plate_number == car_data.plate_number
    ).first()

    if existing_car:
        raise HTTPException(status_code=400, detail="Car already registered")

    car = Car(
        plate_number=car_data.plate_number,
        brand=car_data.brand,
        model=car_data.model,
        year=car_data.year
    )

    db.add(car)
    db.commit()
    db.refresh(car)

    return car

@router.put("/{car_id}", response_model=CarResponse)
def update_car(
    car_id: int,
    car_data: CarRequest,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    car = db.query(Car).filter(Car.id == car_id).first()
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")

    car.plate_number = car_data.plate_number
    car.brand = car_data.brand
    car.model = car_data.model
    car.year = car_data.year

    db.commit()
    db.refresh(car)

    return car

@router.delete("/{car_id}", response_model=CarResponse)
def delete_car(
    car_id: int,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):

    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    db.delete(car)
    db.commit()
    return car

@router.get("/", response_model=List[CarResponse])
def list_all_cars(
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    cars = db.query(Car).all()
    return cars