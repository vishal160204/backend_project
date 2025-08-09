from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate,UserResponse
from app.services.user_service import create_user
from app.db.session import get_db
from app.models.user import User
import random
from app.services.otpservice import send_otp

router = APIRouter()

@router.post("/users/")
def register_user(user_data: UserCreate, db :Session = Depends(get_db)):
    try:
        user = db.query(User).filter_by(email = user_data.email).first()
        if user:
            raise HTTPException(status_code=400, detail="email exists")
        
        otp = str(random.randint(100000, 999999))
        new_user = User(
            first_name = user_data.first_name,
            last_name = user_data.last_name,
            email = user_data.email,
            password = user_data.password,
            otp=otp
            )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        try:
            send_otp(user_data.email, otp)
            #return {"message":"otp send"}
            return {"message": "OTP sent to your email."}

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"otp send failed {e}")
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code = 500, detail = f"Registeration Failed. {e}")





