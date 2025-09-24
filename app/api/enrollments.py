from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import crud, schemas

router = APIRouter(prefix="/enrollments", tags=["enrollments"])

@router.get("/", response_model=list[schemas.EnrollmentRead])
def list_enrollments(student_id: int | None = None, course_id: int | None = None, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_enrollments(db, student_id=student_id, course_id=course_id, limit=limit)

@router.delete("/{enrollment_id}")
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_enrollment(db, enrollment_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return {"deleted": True}
