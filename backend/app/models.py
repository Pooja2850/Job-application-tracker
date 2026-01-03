from sqlalchemy import Column, Integer, String, Date, Text, Boolean
from .db import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=False)
    role_title = Column(String, nullable=False)
    location = Column(String, nullable=True)
    link = Column(String, nullable=True)
    date_applied = Column(Date, nullable=True)
    status = Column(String, nullable=False, default="Applied")
    tags = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
