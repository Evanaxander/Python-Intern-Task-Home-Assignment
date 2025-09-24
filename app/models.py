from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base

class StudentORM(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    enrollments: Mapped[list["EnrollmentORM"]] = relationship(back_populates="student", cascade="all, delete-orphan")

class TeacherORM(Base):
    __tablename__ = "teachers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    courses: Mapped[list["CourseORM"]] = relationship(back_populates="teacher")

class CourseORM(Base):
    __tablename__ = "courses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False, default=30)
    teacher_id: Mapped[int | None] = mapped_column(ForeignKey("teachers.id"), nullable=True)

    teacher: Mapped[TeacherORM | None] = relationship(back_populates="courses")
    enrollments: Mapped[list["EnrollmentORM"]] = relationship(back_populates="course", cascade="all, delete-orphan")

class EnrollmentORM(Base):
    __tablename__ = "enrollments"
    __table_args__ = (
        UniqueConstraint("student_id", "course_id", name="uq_student_course"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)

    student: Mapped[StudentORM] = relationship(back_populates="enrollments")
    course: Mapped[CourseORM] = relationship(back_populates="enrollments")

class ScrapedResourceORM(Base):
    __tablename__ = "scrapedresources"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    category: Mapped[str | None] = mapped_column(String(255), nullable=True)
    price: Mapped[str | None] = mapped_column(String(50), nullable=True)
    author: Mapped[str | None] = mapped_column(String(255), nullable=True)
