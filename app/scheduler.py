import random
import copy

def run_genetic_scheduler(students, courses, rooms, timeslots, generations=50, population_size=20):
    # STEP 1: Helper to generate random schedule
    def create_random_schedule():
        schedule = []
        for course in courses:
            random_timeslot = random.choice(timeslots)
            random_room = random.choice(rooms)
            schedule.append({
                "course_id": course["id"],
                "timeslot_id": random_timeslot["id"],
                "room_id": random_room["id"]
            })
        return schedule

    # STEP 2: Helper to calculate fitness (lower conflicts = better)
    def calculate_fitness(schedule):
        conflict_count = 0

        # Build a mapping of student to their exam times
        student_exam_times = {student["id"]: [] for student in students}

        # Course to timeslot mapping
        course_timeslot = {entry["course_id"]: entry["timeslot_id"] for entry in schedule}

        # Check for student conflicts (same timeslot exams)
        for student in students:
            timeslot_seen = set()
            for course_id in student["courses"]:
                timeslot = course_timeslot.get(course_id)
                if timeslot:
                    if timeslot in timeslot_seen:
                        conflict_count += 1  # Clash: student has 2 exams at same time
                    else:
                        timeslot_seen.add(timeslot)

        # You could also check room over-capacity here (not done for simplicity)
        return -conflict_count  # Higher fitness is better (so negative conflicts)

    # STEP 3: Helper to mutate a schedule slightly
    def mutate(schedule):
        new_schedule = copy.deepcopy(schedule)
        if new_schedule:
            course_to_change = random.choice(new_schedule)
            course_to_change["timeslot_id"] = random.choice(timeslots)["id"]
            course_to_change["room_id"] = random.choice(rooms)["id"]
        return new_schedule

    # STEP 4: Genetic Algorithm loop
    # Initialize population
    population = [create_random_schedule() for _ in range(population_size)]

    for _ in range(generations):
        # Evaluate fitness
        population = sorted(population, key=lambda sch: calculate_fitness(sch), reverse=True)

        # Keep the top 20% schedules
        survivors = population[:max(1, population_size // 5)]

        # Generate new offspring by mutating survivors
        offspring = []
        while len(offspring) + len(survivors) < population_size:
            parent = random.choice(survivors)
            child = mutate(parent)
            offspring.append(child)

        population = survivors + offspring

    # Final best schedule
    best_schedule = max(population, key=lambda sch: calculate_fitness(sch))

    return best_schedule
