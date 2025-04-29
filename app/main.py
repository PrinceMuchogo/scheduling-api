# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.scheduler import run_genetic_scheduler  # your GHA code here
from app.database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload_data/")
def upload_data(payload: schemas.UploadDataRequest, db: Session = Depends(get_db)):
    # Insert Courses
    for course in payload.courses:
        db_course = models.Course(id=course.id, course_code=course.course_code, name=course.name, faculty = course.faculty)
        db.add(db_course)
    db.commit()

    # Insert Students
    for student in payload.students:
        db_student = models.Student(
            id = student.id,
            name=student.name,
            registration_number=student.registration_number
        )
        db.add(db_student)
        db.commit()
        db.refresh(db_student)

        for courseId in student.courses:
            course = db.query(models.Course).filter_by(id=courseId).first()
            if course:
                db_student_course = models.StudentCourse(
                    student_id=db_student.id,
                    course_id=course.id
                )
                db.add(db_student_course)
    db.commit()

    # Insert Rooms
    for room in payload.rooms:
        db_room = models.Room(id=room.id, room_code=room.room_code, name=room.name, capacity=room.capacity)
        db.add(db_room)
    db.commit()

    # Insert Timeslots
    for timeslot in payload.timeslots:
        db_timeslot = models.Timeslot(
            id=timeslot.id,
            timeslot_code=timeslot.timeslot_code,
            date=timeslot.date,
            start_time=timeslot.start_time,
            end_time=timeslot.end_time
        )
        db.add(db_timeslot)
    db.commit()

    return {"message": "Data uploaded successfully"}

@app.get("/generate_schedule/")
def generate_schedule(db: Session = Depends(get_db)):
    # Fetch data
    students = db.query(models.Student).all()
    courses = db.query(models.Course).all()
    rooms = db.query(models.Room).all()
    timeslots = db.query(models.Timeslot).all()

    # Prepare data for scheduler
    student_data = [{"id": s.id, "name": s.name, "courses": [c.id for c in s.courses]} for s in students]
    course_data = [{"id": c.id, "name": c.name} for c in courses]
    room_data = [{"id": r.id, "name": r.name, "capacity": r.capacity} for r in rooms]
    timeslot_data = [{"id": t.id, "date": t.date, "start_time": t.start_time, "end_time": t.end_time} for t in timeslots]

    # Run Genetic Hybrid Algorithm
    best_schedule = run_genetic_scheduler(
        students=student_data,
        courses=course_data,
        rooms=room_data,
        timeslots=timeslot_data
    )

    return {"schedule": best_schedule}
