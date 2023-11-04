from sqlalchemy import Column, String, Integer
from database import Base, engine

class Users(Base):

    __tablename__ = "users_details"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    Password = Column(String)
    score = Column(String)

Base.metadata.create_all(engine)