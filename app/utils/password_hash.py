from passlib.context import CryptContext

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

def pass_hash(password :str)->str:

    return pwd_context.hash(password)

def pass_verify(password : str, hashed_password : str)-> bool:

    return pwd_context.verify(passowrd, hashed_password)
