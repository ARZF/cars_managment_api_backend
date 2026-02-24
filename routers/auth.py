from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import RegisterRequest, LoginRequest, LogoutRequest
from auth import hash_password, verify_password, create_access_token, decode_token
from Models import User
from fastapi import HTTPException
from depends import require_role

router = APIRouter(prefix="/auth", tags=["Auth"])

ALLOWED_ROLES = {"user", "admin"}
DEFAULT_ROLE = "user"

@router.post("/register")
async def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):

    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    if request.role not in ALLOWED_ROLES:
        raise HTTPException(status_code=400, detail="Invalid role")

    hashed = hash_password(request.password)

    new_user = User(
        email=request.email,
        hashed_password=hashed,
        role=request.role,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "email": new_user.email,
        "role": new_user.role
    }

@router.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user.id, user.role)

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.post("/logout")
async def logout():
    return {"message": "Logged out successfully"}