from sqlalchemy.orm import Session
from sqlalchemy import select, func
from . import models
from .schemas import (
    StudentCreate, StudentUpdate,
    TeacherCreate, TeacherUpdate,
    CourseCreate, CourseUpdate,
    EnrollmentCreate,
    ScrapedResourceIn,
)

# Students

def create_student(db: Session, data: StudentCreate):
    obj = models.StudentORM(name=data.name)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_student(db: Session, student_id: int):
    return db.get(models.StudentORM, student_id)

def list_students(db: Session, limit: int = 100):
    return list(db.execute(select(models.StudentORM).limit(limit)).scalars())

def update_student(db: Session, student_id: int, data: StudentUpdate):
    obj = get_student(db, student_id)
    if not obj:
        return None
    if data.name is not None:
        obj.name = data.name
    db.commit()
    db.refresh(obj)
    return obj

def delete_student(db: Session, student_id: int) -> bool:
    obj = get_student(db, student_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True

# Teachers

def create_teacher(db: Session, data: TeacherCreate):
    obj = models.TeacherORM(name=data.name)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_teacher(db: Session, teacher_id: int):
    return db.get(models.TeacherORM, teacher_id)

def list_teachers(db: Session, limit: int = 100):
    return list(db.execute(select(models.TeacherORM).limit(limit)).scalars())

def update_teacher(db: Session, teacher_id: int, data: TeacherUpdate):
    obj = get_teacher(db, teacher_id)
    if not obj:
        return None
    if data.name is not None:
        obj.name = data.name
    db.commit()
    db.refresh(obj)
    return obj

def delete_teacher(db: Session, teacher_id: int) -> bool:
    obj = get_teacher(db, teacher_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True

# Courses

def create_course(db: Session, data: CourseCreate):
    obj = models.CourseORM(title=data.title, capacity=data.capacity, teacher_id=data.teacher_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_course(db: Session, course_id: int):
    return db.get(models.CourseORM, course_id)

def list_courses(db: Session, limit: int = 100):
    return list(db.execute(select(models.CourseORM).limit(limit)).scalars())

def update_course(db: Session, course_id: int, data: CourseUpdate):
    obj = get_course(db, course_id)
    if not obj:
        return None
    if data.title is not None:
        obj.title = data.title
    if data.capacity is not None:
        obj.capacity = data.capacity
    if data.teacher_id is not None:
        obj.teacher_id = data.teacher_id
    db.commit()
    db.refresh(obj)
    return obj

def delete_course(db: Session, course_id: int) -> bool:
    obj = get_course(db, course_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True

# Enrollment business rules

def enroll_student(db: Session, student_id: int, data: EnrollmentCreate):
    # Duplicate check
    exists_stmt = select(models.EnrollmentORM).where(
        models.EnrollmentORM.student_id == student_id,
        models.EnrollmentORM.course_id == data.course_id,
    )
    existing = db.execute(exists_stmt).scalar_one_or_none()
    if existing:
        raise ValueError("Student already enrolled in this course")

    # Capacity check
    count_stmt = select(func.count(models.EnrollmentORM.id)).where(
        models.EnrollmentORM.course_id == data.course_id
    )
    current_count = db.execute(count_stmt).scalar_one()
    course = get_course(db, data.course_id)
    if course is None:
        raise ValueError("Course not found")
    if current_count >= course.capacity:
        raise ValueError("Course capacity reached")

    obj = models.EnrollmentORM(student_id=student_id, course_id=data.course_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_enrollments(db: Session, student_id: int | None = None, course_id: int | None = None, limit: int = 100):
    stmt = select(models.EnrollmentORM)
    if student_id is not None:
        stmt = stmt.where(models.EnrollmentORM.student_id == student_id)
    if course_id is not None:
        stmt = stmt.where(models.EnrollmentORM.course_id == course_id)
    stmt = stmt.limit(limit)
    return list(db.execute(stmt).scalars())

def delete_enrollment(db: Session, enrollment_id: int) -> bool:
    obj = db.get(models.EnrollmentORM, enrollment_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True

# Scraped resources

def insert_scraped(db: Session, items: list[ScrapedResourceIn]):
    rows = [
        models.ScrapedResourceORM(
            title=i.title, url=i.url, category=i.category, price=i.price, author=i.author
        ) for i in items
    ]
    db.add_all(rows)
    db.commit()
    return rows

def list_scraped(db: Session, limit: int = 100):
    stmt = select(models.ScrapedResourceORM).limit(limit)
    return list(db.execute(stmt).scalars())
