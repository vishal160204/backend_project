import jwt,JWTError
import datetime, timedelata
from app.config import SECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data : dict):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"expire" : expire})
    access_token = jwt.encode(data, SECRET_KEY, ALGORITHM)
    return access_token



def create_refresh_token(data : dict):
    expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    data.update({"expire" : expire})
    refresh_token = jwt.encode(data, SECRET_KEY, ALGORITHM)
    return refresh_token

def token_decoder(token : str):
    try:
        return jwt.decode(token,SECRET_KEY, ALGORITHM)
    except Exception as e:
        return none






