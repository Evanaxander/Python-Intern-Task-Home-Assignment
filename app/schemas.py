from pydantic import BaseModel

class StudentCreate(BaseModel):
    name: str

class StudentRead(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

class StudentUpdate(BaseModel):
    name: str | None = None

class TeacherCreate(BaseModel):
    name: str

class TeacherRead(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

class TeacherUpdate(BaseModel):
    name: str | None = None

class CourseCreate(BaseModel):
    title: str
    capacity: int = 30
    teacher_id: int | None = None

class CourseRead(BaseModel):
    id: int
    title: str
    capacity: int
    teacher_id: int | None
    class Config:
        from_attributes = True

class CourseUpdate(BaseModel):
    title: str | None = None
    capacity: int | None = None
    teacher_id: int | None = None

class EnrollmentCreate(BaseModel):
    course_id: int

class EnrollmentRead(BaseModel):
    id: int
    student_id: int
    course_id: int
    class Config:
        from_attributes = True

class ScrapedResourceIn(BaseModel):
    title: str
    url: str
    category: str | None = None
    price: str | None = None
    author: str | None = None

class ScrapedResourceRead(ScrapedResourceIn):
    id: int
    class Config:
        from_attributes = True
