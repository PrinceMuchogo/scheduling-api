# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from sqlalchemy.orm import Session
from app import  schemas
from app.scheduler import run_genetic_scheduler  # your GHA code here
# from app.database import SessionLocal, engine

app = FastAPI(
    title="Scheduling API",
    version="1.1.0",
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# models.Base.metadata.create_all(bind=engine)

# Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @app.post("/upload_data/")
# def upload_data(payload: schemas.UploadDataRequest, db: Session = Depends(get_db)):
#     # Insert Courses
#     for course in payload.courses:
#         db_course = models.Course(id=course.id, course_code=course.course_code, name=course.name, faculty = course.faculty)
#         db.add(db_course)
#     db.commit()

#     # Insert Students
#     for student in payload.students:
#         db_student = models.Student(
#             id = student.id,
#             name=student.name,
#             registration_number=student.registration_number
#         )
#         db.add(db_student)
#         db.commit()
#         db.refresh(db_student)

#         for courseId in student.courses:
#             course = db.query(models.Course).filter_by(id=courseId).first()
#             if course:
#                 db_student_course = models.StudentCourse(
#                     student_id=db_student.id,
#                     course_id=course.id
#                 )
#                 db.add(db_student_course)
#     db.commit()

#     # Insert Rooms
#     for room in payload.rooms:
#         db_room = models.Room(id=room.id, room_code=room.room_code, name=room.name, capacity=room.capacity)
#         db.add(db_room)
#     db.commit()

#     # Insert Timeslots
#     for timeslot in payload.timeslots:
#         db_timeslot = models.Timeslot(
#             id=timeslot.id,
#             timeslot_code=timeslot.timeslot_code,
#             date=timeslot.date,
#             start_time=timeslot.start_time,
#             end_time=timeslot.end_time
#         )
#         db.add(db_timeslot)
#     db.commit()

#     return {"message": "Data uploaded successfully"}

@app.post("/generate_schedule/")
def generate_schedule(payload: schemas.UploadDataRequest):
    # Prepare data for scheduler

    student_data = []
    for student in payload.students:

        student_data.append({
            "id": student.id,
            "name": student.name,
            "registration_number": student.registration_number,
            "courses": student.student_courses  # Only including course_ids here
        })

    print(student_data)

    course_data = [c.model_dump() for c in payload.courses]
    room_data = [r.model_dump() for r in payload.rooms]
    timeslot_data = [t.model_dump() for t in payload.timeslots]

    # Run Genetic Hybrid Algorithm
    best_schedule = run_genetic_scheduler(
        students=student_data,
        courses=course_data,
        rooms=room_data,
        timeslots=timeslot_data
    )

    return {"schedule": best_schedule}
