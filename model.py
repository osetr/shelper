from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "User"

    login = Column(String(30), primary_key=True)
    hashed_password = Column(Text)
