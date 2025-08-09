from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    first_name : str
    last_name : str
    email : EmailStr
    password : str


class OtpVerify(BaseModel):
    otp : str



class PasswordReset(BaseModel):
    email : EmailStr
    otp : str
    new_password : str

class Login(BaseModel):
    email : EmailStr
    password : str



class UserResponse(BaseModel):
    id : int
    first_name : str
    last_name : str
    email : EmailStr


    class Config:
        orm_mode = True