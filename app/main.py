from fastapi import FastAPI
from .db import engine, Base
from .api import students, teachers, courses, scraped, enrollments

Base.metadata.create_all(bind=engine)

app = FastAPI(title="School Management System")

app.include_router(students.router)
app.include_router(teachers.router)
app.include_router(courses.router)
app.include_router(scraped.router)
app.include_router(enrollments.router)

@app.get("/")
def root():
    return {"status": "ok"}
