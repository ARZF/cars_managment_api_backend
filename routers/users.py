from fastapi import APIRouter, Depends
from Models import User
from depends import get_current_user, require_role

router = APIRouter(prefix="/users", tags=["Users"])



@router.get("/dashboard")
def dashboard(current_user: User = Depends(get_current_user)):
    return {"message": f"Welcome {current_user.email}"}



@router.get("/admin")
def admin_panel(current_user: User = Depends(require_role("admin"))):
    return {"message": "Admin access granted"}