from time import time

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, HttpUrl
import uvicorn
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


#define request body schema
class Course(BaseModel):
    course_name: str
    instructor: str
    duration: float
    website: str


while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="aiquest",
            user="postgres",
            password="1234",
            cursor_factory=RealDictCursor
        )
        coursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Database connection failed!")
        print("Error details:", error)
        time.sleep(2)  # Wait for 2 seconds before retrying
    


@app.post("/post_course")
def create_course(course: Course):
    coursor.execute(
        """INSERT INTO courses (course_name, instructor, duration, website) VALUES(%s,%s,%s,%s) RETURNING *""",
        (course.course_name, course.instructor, course.duration, course.website)
    )
    conn.commit()
    return {"message": f"Course '{course.course_name}' created successfully!"}

@app.get("/")
def read_data():
    coursor.execute("SELECT * FROM courses")
    data = coursor.fetchall()
    return {"data": data}

# fetch one course by id
@app.get("/course/{id}")
def get(id: int):
    coursor.execute("SELECT * FROM courses WHERE id=%s", (id,))
    data = coursor.fetchone()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This Course id:{id} not found")
    return {"data": data}

@app.delete("/course/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int):
    coursor.execute("DELETE FROM courses WHERE id=%s RETURNING *", (str(id),))
    delete_data = coursor.fetchone()
    conn.commit()
    if not delete_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This Course id:{id} not found")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/course/{id}")
def update(id: int, course: Course):
    coursor.execute(
        """UPDATE courses SET course_name=%s, instructor=%s, duration=%s, website=%s WHERE id=%s RETURNING *""",
        (course.course_name, course.instructor, course.duration, course.website, str(id))
    )
    update_data = coursor.fetchone()
    conn.commit()
    if not update_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This Course id:{id} not found")
    
    return {"message": f"Course id:{id} updated successfully!"}
#partial update
@app.patch("/course/{id}")
def partial_update(id: int, course: Course):
    coursor.execute(
        """UPDATE courses SET course_name=COALESCE(%s, course_name), instructor=COALESCE(%s, instructor), duration=COALESCE(%s, duration), website=COALESCE(%s, website) WHERE id=%s RETURNING *""",
        (course.course_name, course.instructor, course.duration, course.website, str(id))
    )
    update_data = coursor.fetchone()
    conn.commit()
    if not update_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This Course id:{id} not found")
    
    return {"message": f"Course id:{id} partially updated successfully!"}