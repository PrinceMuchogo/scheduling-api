import random
import copy

def run_genetic_scheduler(students, courses, rooms, timeslots, generations=50, population_size=20):
    # Helper: Count number of students registered for a course
    def course_student_count(course_id):
        return sum(1 for student in students if course_id in student["courses"])

    # Helper: Check if two courses have student conflicts
    def has_student_conflict(course_id_1, course_id_2):
        for student in students:
            if course_id_1 in student["courses"] and course_id_2 in student["courses"]:
                return True
        return False

    # STEP 1: Create a smart random schedule
    def create_random_schedule():
        schedule = []
        assigned_courses = set()

        # Sort courses by number of students descending (allocate big ones first)
        courses_sorted = sorted(courses, key=lambda c: course_student_count(c["id"]), reverse=True)

        for course in courses_sorted:
            if course["id"] in assigned_courses:
                continue

            random_timeslot = random.choice(timeslots)
            random_room = random.choice(rooms)

            schedule.append({
                "course_id": course["id"],
                "timeslot_id": random_timeslot["id"],
                "room_id": random_room["id"]
            })
            assigned_courses.add(course["id"])

            # Check if we can fit another course in same room/timeslot
            remaining_capacity = random_room["capacity"] - course_student_count(course["id"])

            if remaining_capacity > 0:
                for other_course in courses_sorted:
                    if other_course["id"] in assigned_courses:
                        continue
                    if course_student_count(other_course["id"]) <= remaining_capacity:
                        if not has_student_conflict(course["id"], other_course["id"]):
                            schedule.append({
                                "course_id": other_course["id"],
                                "timeslot_id": random_timeslot["id"],
                                "room_id": random_room["id"]
                            })
                            assigned_courses.add(other_course["id"])
                            remaining_capacity -= course_student_count(other_course["id"])

                            if remaining_capacity <= 0:
                                break

        return schedule

    # STEP 2: Calculate fitness of a schedule
    def calculate_fitness(schedule):
        conflict_count = 0

        # Map student -> timeslots they have exams in
        student_exam_times = {student["id"]: [] for student in students}
        course_timeslot = {entry["course_id"]: entry["timeslot_id"] for entry in schedule}
        course_room = {entry["course_id"]: entry["room_id"] for entry in schedule}

        # Student exam conflicts
        for student in students:
            timeslot_seen = set()
            for course_id in student["courses"]:
                timeslot = course_timeslot.get(course_id)
                if timeslot:
                    if timeslot in timeslot_seen:
                        conflict_count += 1
                    else:
                        timeslot_seen.add(timeslot)

        # Room over-capacity conflicts
        for timeslot in timeslots:
            exams_in_timeslot = [e for e in schedule if e["timeslot_id"] == timeslot["id"]]
            room_course_students = {}

            for exam in exams_in_timeslot:
                room_id = exam["room_id"]
                if room_id not in room_course_students:
                    room_course_students[room_id] = 0
                room_course_students[room_id] += course_student_count(exam["course_id"])

            for room_id, total_students in room_course_students.items():
                room_capacity = next(r for r in rooms if r["id"] == room_id)["capacity"]
                if total_students > room_capacity:
                    conflict_count += (total_students - room_capacity)  # Penalty for over-capacity

        return -conflict_count  # Higher fitness = less conflicts

    # STEP 3: Mutate a schedule
    def mutate(schedule):
        new_schedule = copy.deepcopy(schedule)
        if new_schedule:
            course_to_change = random.choice(new_schedule)
            course_to_change["timeslot_id"] = random.choice(timeslots)["id"]
            course_to_change["room_id"] = random.choice(rooms)["id"]
        return new_schedule

    # STEP 4: Genetic Algorithm
    population = [create_random_schedule() for _ in range(population_size)]

    for _ in range(generations):
        # Evaluate fitness
        population = sorted(population, key=lambda sch: calculate_fitness(sch), reverse=True)

        # Keep the top 20%
        survivors = population[:max(1, population_size // 5)]

        # Generate new offspring by mutating survivors
        offspring = []
        while len(offspring) + len(survivors) < population_size:
            parent = random.choice(survivors)
            child = mutate(parent)
            offspring.append(child)

        population = survivors + offspring

    best_schedule = max(population, key=lambda sch: calculate_fitness(sch))

    return best_schedule
