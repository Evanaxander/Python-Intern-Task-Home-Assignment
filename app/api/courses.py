from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import crud, schemas

router = APIRouter(prefix="/courses", tags=["courses"])

@router.post("/", response_model=schemas.CourseRead)
def create_course(data: schemas.CourseCreate, db: Session = Depends(get_db)):
    return crud.create_course(db, data)

@router.get("/", response_model=list[schemas.CourseRead])
def list_courses(limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_courses(db, limit)

@router.get("/{course_id}", response_model=schemas.CourseRead)
def get_course(course_id: int, db: Session = Depends(get_db)):
    obj = crud.get_course(db, course_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Course not found")
    return obj

@router.patch("/{course_id}", response_model=schemas.CourseRead)
def update_course(course_id: int, data: schemas.CourseUpdate, db: Session = Depends(get_db)):
    obj = crud.update_course(db, course_id, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Course not found")
    return obj

@router.delete("/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_course(db, course_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Course not found")
    return {"deleted": True}
