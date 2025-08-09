from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True) # No need of index=True because primary key is already indexed by db
    first_name = Column(String, nullable = False)
    last_name = Column(String, nullable = False)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    otp = Column(String, nullable = True)
    isverified = Column(Boolean, default = False)
    is_active = Column(Boolean, default = True)
    

