from typing import List
from pydantic import BaseModel


class CourseCreate(BaseModel):
    id: int
    course_code: str
    name: str
    faculty: str
    createdAt: str = None
    # updatedAt: str = None



class StudentCourse(BaseModel):
    id: int
    student_id: int
    course_id: int
    courses: List[CourseCreate]
    createdAt: str = None
    # updatedAt: str = None

class StudentCreate(BaseModel):
    id: int
    name: str
    registration_number: str
    createdAt: str = None
    # updatedAt: str = None
    student_courses: List[int]  # List of Course Codes


    

class RoomCreate(BaseModel):
    id: int
    room_code: str
    name: str
    capacity: int
    createdAt: str = None
    # updatedAt: str = None

class TimeslotCreate(BaseModel):
    id: int
    timeslot_code: str
    date: str
    start_time: str
    end_time: str
    createdAt: str = None
    # updatedAt: str = None

class UploadDataRequest(BaseModel):
    students: List[StudentCreate]
    courses: List[CourseCreate]
    rooms: List[RoomCreate]
    timeslots: List[TimeslotCreate]


