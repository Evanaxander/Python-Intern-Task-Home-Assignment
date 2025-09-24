from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import crud, schemas

router = APIRouter(prefix="/students", tags=["students"])

@router.post("/", response_model=schemas.StudentRead)
def create_student(data: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db, data)

@router.get("/", response_model=list[schemas.StudentRead])
def list_students(limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_students(db, limit)

@router.get("/{student_id}", response_model=schemas.StudentRead)
def get_student(student_id: int, db: Session = Depends(get_db)):
    obj = crud.get_student(db, student_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Student not found")
    return obj

@router.post("/{student_id}/enroll", response_model=schemas.EnrollmentRead)
def enroll(student_id: int, data: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    try:
        return crud.enroll_student(db, student_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{student_id}", response_model=schemas.StudentRead)
def update_student(student_id: int, data: schemas.StudentUpdate, db: Session = Depends(get_db)):
    obj = crud.update_student(db, student_id, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Student not found")
    return obj

@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_student(db, student_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"deleted": True}
