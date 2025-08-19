from fastapi import HTTPException,Depends
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.services.jwt import token_decoder
from app.models.user import User
from app.db.session import SessionLocal,get_db


security = HTTPBearer()

def get_current_user(credentials : HTTPAuthorizationCredentials = Depends(security), db : Session = Depends(get_db)):
    access_token = credentials.credentials
    payload = token_decoder(access_token)

    if not payload:
        raise HTTPException(status_code = 401, detail = "Invalid token.")
    
    email = payload.get("sub")
    if not email:
        raise HTTPexception(status_code = 401, detail = "Invalid token.")

    user = db.query(User).filter_by(User.email == email).first()
    if not user:
        raise HTTPException(status_code = 401, detail = "User not found.")

    return user