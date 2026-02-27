from sqlalchemy import Column, Integer, String
from .database import Base


class Course(Base):
    __tablename__ = "sqldb"

    id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String, nullable=False)
    instructor = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    website = Column(String, nullable=False)