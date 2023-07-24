import numpy as np
import random
import math

class Student:
    def __init__(self, id, arrival_time):
        self.id = id
        self.arrival_time = arrival_time
        self.service_time = 0

class SchoolSystemSimulation:
    def __init__(self, num_students):
        self.num_students = num_students
        self.students = []
        self.current_time = 0
        self.cumulative_arrival = 0

    def generate_arrival_time(self):
        # Use a cumulative random function that increases with time
        self.cumulative_arrival += np.random.randint(1, 5)
        return self.cumulative_arrival

    def generate_service_time(self):
        # Use a random sine function to generate service time
        amplitude = random.uniform(0.5, 1.5)
        frequency = random.uniform(0.1, 0.5)
        service_time = amplitude * math.sin(frequency * self.current_time)
        return max(service_time, 0)  # Ensure non-negative service time

    def run_simulation(self):
        # Generate students and their arrival times
        for i in range(self.num_students):
            arrival_time = self.generate_arrival_time()
            student = Student(i, arrival_time)
            self.students.append(student)

        # Simulation loop
        while self.students:
            # Get the student with the earliest arrival time
            current_student = min(self.students, key=lambda s: s.arrival_time)

            # Move simulation time forward to the current student's arrival time
            self.current_time = current_student.arrival_time

            # Generate service time for the current student
            current_student.service_time = self.generate_service_time()

            # Process the current student
            print(f"Processing student {current_student.id} at time {self.current_time}")
            # ... Do whatever processing you need for the student ...

            # Remove the processed student from the list
            self.students.remove(current_student)

# Create an instance of SchoolSystemSimulation and pass the number of students as an argument
num_students = 40000  # You can change this value to simulate a different number of students
simulation = SchoolSystemSimulation(num_students)
simulation.run_simulation()
