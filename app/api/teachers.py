from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import crud, schemas

router = APIRouter(prefix="/teachers", tags=["teachers"])

@router.post("/", response_model=schemas.TeacherRead)
def create_teacher(data: schemas.TeacherCreate, db: Session = Depends(get_db)):
    return crud.create_teacher(db, data)

@router.get("/", response_model=list[schemas.TeacherRead])
def list_teachers(limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_teachers(db, limit)

@router.get("/{teacher_id}", response_model=schemas.TeacherRead)
def get_teacher(teacher_id: int, db: Session = Depends(get_db)):
    obj = crud.get_teacher(db, teacher_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return obj

@router.patch("/{teacher_id}", response_model=schemas.TeacherRead)
def update_teacher(teacher_id: int, data: schemas.TeacherUpdate, db: Session = Depends(get_db)):
    obj = crud.update_teacher(db, teacher_id, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return obj

@router.delete("/{teacher_id}")
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_teacher(db, teacher_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return {"deleted": True}
