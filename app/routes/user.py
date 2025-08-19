from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate,UserResponse,Login,OtpVerify,PasswordReset,ForgotPassword
from app.services.user_service import create_user
from app.db.session import get_db
from app.models.user import User
import random
from app.utils.password_hash import pass_hash
from fastapi.security import OAuth2
from app.services.otpservice import send_otp

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")

@router.post("/register/")
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
            password = pass_hash(user_data.password),
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

@router.post("/verify/")
def verify_user(user_data : OtpVerify,db : Session = Depends(get_db)):
    user = db.query(User).filter_by(email = user_data.email).first()

    if not user or user.otp != user_data.otp:
        raise HTTPException(status_code = 400, detail = "Invalid Otp")

    user.otp = None
    user.is_verified = True
    db.commit()
    return {"message" : "Email verified successfully! You can now login."}

@router.post("/login/")
def login_user(user_data : Login, db :Session = Depends(get_db)):
    try:
        user = db.query(User).filter_by(email = user_data.email).first()
        if not user:
            raise HTTPException(status_code = 401, detail = "Invalid Credentials")
        if not user.is_verified:
            raise HTTPException(status_code = 403, detail = "Please verify your email first")
        if not pwd.context.verify(user_data.password, user.password):
            raise HTTPException(status_code = 401, detail = "Invalid Credentials")

        access_token = create_access_token({"sub" : user_data.email})
        #refresh_token = create_refresh_token({"sub" : user_data.email})

        return {"access_token" : token, "token_type" : "bearer"}

    except Excaption as e:
        raise HTTPException(status_code = 500, details = "login failed.: {e}" )


@router.post("/forgot-password/")
def forgot_password(user_data : ForgotPassword, db : Session = Depends(get_db)):
    user = db.query(User).filter_by(email = user_data.email).first()
    if not user:
        raise HTTPException(status_code = 404, detail = "Email not found.")
    otp = str(random.randint(100000,999999))
    user.otp = otp
    db.commit()
    send_otp(user.email, otp)
    return {"message" : "otp sent successfully."}

@router.post("/reset-password/")
def reset_password(user_data : PasswordReset, db : Session = Depends(get_db)):
    user = db.query(User).filter_by(email = user_data.email).first()
    if not user or user.otp != user_data.otp:
        raise HTTPException(status_code = 400, dettail = "Invalid otp.")
    password = pass_hash(user_data.password)
    user.otp = None
    db.commit()
    return {"message" : "Password has been reset successfully"}




@router.get("/me/", response_model = UserResponse)
def get_me(access_token : str = Depends(oauth2_scheme), db : Session = Depends(get_db)):
    payload = decode_access_token(access_token)
    if not payload:
        raise HTTPException(status_code = 401, detail = "Invalid token")
    user = db.query(User).get(int(payload.get("sub")))
    if not user:
        raise HTTPException(status_code = 404, detail = "User detail not found")
    return user







