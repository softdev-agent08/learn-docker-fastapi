# Start FastAPI
1. At first create a virtual environment 
2. start env
```bash
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
.\env\Scripts\Activate.ps1
```
3. Install these module
```bash
    pip3 install fastapi
    pip3 install uvicorn
    pip3 freeze
```
4. create `main.py` file
5. run these fastapi using 
```bash
    fastapi dev main.py
```

6. Connect PostgreSql
```bash
    pip install psycopg2 (Import module)
    pip install psycopg2-binary
```
```python
import psycopg2
from psycopg2.extras import RealDictCursor

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


@app.get("/")
def read_data():
    coursor.execute("SELECT * FROM courses")
    data = coursor.fetchall()
    return {"data": data}

@app.post("/post_course")
def create_course(course: Course):
    coursor.execute(
        """INSERT INTO courses (course_name, instructor, duration, website) VALUES(%s,%s,%s,%s) RETURNING *""",
        (course.course_name, course.instructor, course.duration, course.website)
    )
    conn.commit()
    return {"message": f"Course '{course.course_name}' created successfully!"}
```

# Fast Api + SQLAlchemi

1. create a folder name as `app`
2. create `__init__.py` to make it project
3. create `model.py`
```python
    from sqlalchemy import Column, Integer, String
    from .database import Base


    class Course(Base):
        __tablename__ = "sqldb"

        id = Column(Integer, primary_key=True, index=True)
        course_name = Column(String, nullable=False)
        instructor = Column(String, nullable=False)
        duration = Column(Integer, nullable=False)
        website = Column(String, nullable=False)
```
4. create `database.py`
```python
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, declarative_base

    DATABASE_URL = "postgresql://postgres:1234@localhost/aiquest"

    engine = create_engine(DATABASE_URL)

    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )

    Base = declarative_base()


    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
```
5. main `.py` file like `main.py`
```python
    from fastapi import FastAPI, Depends
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
```
- <h5> Show all Data and show by id</h5>

```python
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
```

