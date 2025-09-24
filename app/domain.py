from __future__ import annotations
from abc import ABC, abstractmethod

class Person(ABC):
    def __init__(self, name: str) -> None:
        self._name = name  # encapsulation via underscore convention

    @abstractmethod
    def get_display_name(self) -> str:  # abstraction
        raise NotImplementedError

class Student(Person):  # inheritance
    def get_display_name(self) -> str:  # polymorphism
        return f"Student: {self._name}"

class Teacher(Person):
    def get_display_name(self) -> str:
        return f"Teacher: {self._name}"

class Course:
    def __init__(self, title: str, capacity: int) -> None:
        self.title = title
        self.capacity = capacity
        self._enrolled: set[str] = set()

    def enroll(self, student_name: str) -> bool:
        if student_name in self._enrolled:
            return False
        if len(self._enrolled) >= self.capacity:
            return False
        self._enrolled.add(student_name)
        return True
