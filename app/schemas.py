from typing import List
from pydantic import BaseModel

class StudentCreate(BaseModel):
    id: int
    name: str
    registration_number: str
    courses: List[int]  # List of Course Codes

class CourseCreate(BaseModel):
    id: int
    course_code: str
    name: str
    faculty: str

class RoomCreate(BaseModel):
    id: int
    room_code: str
    name: str
    capacity: int

class TimeslotCreate(BaseModel):
    id: int
    timeslot_code: str
    date: str
    start_time: str
    end_time: str

class UploadDataRequest(BaseModel):
    students: List[StudentCreate]
    courses: List[CourseCreate]
    rooms: List[RoomCreate]
    timeslots: List[TimeslotCreate]
