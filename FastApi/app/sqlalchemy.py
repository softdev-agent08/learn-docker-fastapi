from fastapi import FastAPI, Depends, HTTPException, Response, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .database import get_db, engine, Base
from . import models

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)


# Pydantic schema (request body)
class CourseCreate(BaseModel):
    course_name: str
    instructor: str
    duration: int
    website: str


@app.get("/coursesalchemy")
def courses(db: Session = Depends(get_db)):
    courses = db.query(models.Course).all()
    return {"data": courses}


@app.post("/courses")
def create_course(course: CourseCreate, db: Session = Depends(get_db)):

    new_course = models.Course(
        course_name=course.course_name,
        instructor=course.instructor,
        duration=course.duration,
        website=course.website
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return {"message": f"Course '{new_course.course_name}' created successfully!"}

@app.get("/getallcourses")
def get_all_courses(db: Session = Depends(get_db)):
    courses = db.query(models.Course).all()
    return {"data": courses}

@app.get("/coursealchemy/{id}")
def get_course_by_id(id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"This Course id:{id} not found"
            )
    return {"data": course}

@app.put("/coursealchemy/{id}")
def update_course(id: int, course: CourseCreate, db: Session = Depends(get_db)):
    existing_course = db.query(models.Course).filter(models.Course.id == id)
    course_temp = existing_course.first()
    if not course_temp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"This Course id:{id} not found"
            )
    
    course_data = course.model_dump()
    course_data["website"] = str(course_data["website"])


    existing_course.update(course_data, synchronize_session=False)

    db.commit()
    db.refresh(existing_course.first())
    return {"message": f"Course id:{id} updated successfully!"}

@app.patch("/coursealchemy/{id}")
def partial_update_course(id: int, course: CourseCreate, db: Session = Depends(get_db)):
    existing_course = db.query(models.Course).filter(models.Course.id == id).first()
    if not existing_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"This Course id:{id} not found"
            )
    
    if course.course_name is not None:
        existing_course.course_name = course.course_name
    if course.instructor is not None:
        existing_course.instructor = course.instructor
    if course.duration is not None:
        existing_course.duration = course.duration
    if course.website is not None:
        existing_course.website = course.website

    db.commit()
    db.refresh(existing_course)
    return {"message": f"Course id:{id} partially updated successfully!"}

@app.delete("/coursealchemy/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(id: int, db: Session = Depends(get_db)):
    existing_course = db.query(models.Course).filter(models.Course.id == id).first()
    if not existing_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"This Course id:{id} not found"
            )
    
    db.delete(existing_course)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)