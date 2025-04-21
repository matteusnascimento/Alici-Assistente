
from sqlalchemy import Column, Integer, String, Text
from .database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String, index=True)
    content = Column(Text)
