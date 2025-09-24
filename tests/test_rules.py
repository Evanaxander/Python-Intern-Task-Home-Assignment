import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base
from app import models
from app import crud
from app.schemas import StudentCreate, CourseCreate, EnrollmentCreate

@pytest.fixture()
def db_session(tmp_path):
    # Use a temporary SQLite DB for tests
    db_url = f"sqlite:///{tmp_path}/test.db"
    engine = create_engine(db_url, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def setup_entities(db):
    s = models.StudentORM(name="Alice")
    c = models.CourseORM(title="Math", capacity=1)
    db.add_all([s, c])
    db.commit()
    db.refresh(s)
    db.refresh(c)
    return s, c


def test_duplicate_enrollment_prevented(db_session):
    s, c = setup_entities(db_session)
    crud.enroll_student(db_session, s.id, EnrollmentCreate(course_id=c.id))
    with pytest.raises(ValueError):
        crud.enroll_student(db_session, s.id, EnrollmentCreate(course_id=c.id))


def test_capacity_enforced(db_session):
    s1, c = setup_entities(db_session)
    s2 = models.StudentORM(name="Bob")
    db_session.add(s2)
    db_session.commit()
    db_session.refresh(s2)

    crud.enroll_student(db_session, s1.id, EnrollmentCreate(course_id=c.id))
    with pytest.raises(ValueError):
        crud.enroll_student(db_session, s2.id, EnrollmentCreate(course_id=c.id))
