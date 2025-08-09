from sqlalchemy.orm import session 
from app.models.user import User
from app.schemas.user import UserCreate



def create_user(db : session, user_data : UserCreate):
    new_user =User(
        first_name = user_data.first_name,
        last_name =  user_data.last_name,
        email = user_data.email,
        password = user_data.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
