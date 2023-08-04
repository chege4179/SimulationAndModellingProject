import random
from math import cos

class SchoolSimulation:

    # Initialize the class with the number of servers and the number of students
    def __init__(self, num_servers, num_students):
        self.num_servers = num_servers
        self.num_students = num_students
        self.service_times = []
        self.arrival_times = []
        self.servers_data = {}

    # Generate the random service times for the using the cos function

    def generate_service_times(self):
        for _ in range(self.num_students):
            num = random.random()
            time = round((5 * (cos(num) + 1) / 2), 2)
            self.service_times.append(time)

    # Generate arrival times
    def generate_arrival_times(self):
        self.arrival_times.append(round(10 * random.random(), 2))
        for i in range(1, self.num_students):
            arrival_time = 10 * random.random() * ((60000 - self.arrival_times[i - 1]) / 60000) + self.arrival_times[i - 1]
            self.arrival_times.append(round(arrival_time, 2))

    # start the simulation process
    def simulate_enrolment_service(self):
        for server_id in range(self.num_servers):
            self.servers_data[server_id] = {
                'service_begin_times': [self.arrival_times[0]],
                'queue_wait_times': [0.00],
                'service_end_times': [self.arrival_times[0] + self.service_times[0]],
                'times_in_system': [self.service_times[0]],
                'server_idle_times': [0.00]
            }

        for i in range(1, self.num_students):
            # Find the server that ends service earliest
            server_id = min(self.servers_data, key=lambda x: self.servers_data[x]['service_end_times'][-1])

            if self.arrival_times[i] > self.servers_data[server_id]['service_end_times'][-1]:
                service_begin_time = self.arrival_times[i]
                queue_wait_time = 0.00
                server_idle_time = self.arrival_times[i] - self.servers_data[server_id]['service_end_times'][-1]
            else:
                service_begin_time = self.servers_data[server_id]['service_end_times'][-1]
                queue_wait_time = self.servers_data[server_id]['service_end_times'][-1] - self.arrival_times[i]
                server_idle_time = 0.00

            service_end_time = round(self.service_times[i] + service_begin_time, 2)
            time_in_system = round(queue_wait_time + self.service_times[i], 2)

            self.servers_data[server_id]['service_begin_times'].append(service_begin_time)
            self.servers_data[server_id]['queue_wait_times'].append(queue_wait_time)
            self.servers_data[server_id]['service_end_times'].append(service_end_time)
            self.servers_data[server_id]['times_in_system'].append(time_in_system)
            self.servers_data[server_id]['server_idle_times'].append(server_idle_time)

    # Calculate average time in the system
    def generate_average_time_in_system(self):
        total = 0
        for num in self.service_times:

            total += num
        average = total / self.num_students
        print(f"The average amount of time spent in the system is {average} minutes")

    # Calculate average service time in the system
    def calculate_average_service_time(self):
        total_service_time = sum(self.service_times)
        average_service_time = total_service_time / self.num_students
        print(f"The average service time is {average_service_time:.2f} minutes")

    # Calculate idle time for the servers

    def calculate_idle_time_for_servers(self):
        total_idle_time = sum(sum(data['server_idle_times']) for data in self.servers_data.values())
        print(f"The total idle time for all servers is {total_idle_time:.2f} minutes")

    # Calculate the probability of the students waiting in line
    def calculate_probability_of_waiting(self):
        num_students_waiting = sum(1 for data in self.servers_data.values() if max(data['queue_wait_times']) > 0)
        probability_of_waiting = num_students_waiting / self.num_students
        print(f"The probability a student waits in the queue is {probability_of_waiting:.2f}")

    # Calculate average waiting time for students
    def calculate_average_waiting_time(self):
        total_waiting_time = sum(sum(data['queue_wait_times']) for data in self.servers_data.values())
        average_waiting_time = total_waiting_time / self.num_students
        print(f"The average waiting time for a student is {average_waiting_time:.2f} minutes")

    # Calculate average inter arrival times
    def calculate_average_time_between_arrivals(self):
        total_time_between_arrivals = sum(
            self.arrival_times[i] - self.arrival_times[i - 1] for i in range(1, self.num_students))
        average_time_between_arrivals = total_time_between_arrivals / (self.num_students - 1)
        print(f"The average time between arrivals is {average_time_between_arrivals:.2f} minutes")

    # wrapper function to call the other methods to generate the relevant metrics
    def calculate_metrics(self):
        self.generate_average_time_in_system()
        self.calculate_average_time_between_arrivals()
        self.calculate_average_service_time()
        self.calculate_idle_time_for_servers()
        self.calculate_probability_of_waiting()
        self.calculate_average_waiting_time()

    # export the data to CSV
    def save_to_csv(self):
        import pandas as pd

        for server_id, data in self.servers_data.items():
            ss = {
                'arrival_time': data['queue_wait_times'],
                'service_time': data['service_begin_times'],
                'inter_arrival_time': [data['service_begin_times'][i] - data['queue_wait_times'][i] for i in range(len(data['service_begin_times']))],
                'time_service_begins': data['service_begin_times'],
                'queue_wait_time': data['queue_wait_times'],
                'time_service_ends': data['service_end_times'],
                'time_in_system': data['times_in_system'],
                'server_idle_time': data['server_idle_times']

            }

            df = pd.DataFrame(ss)
            df.to_csv(f'school_simulation_for_teller_{server_id}.csv', index=False)

if __name__ == "__main__":
    num_servers = 2
    num_students = 40000

    school_simulator = SchoolSimulation(num_servers, num_students)
    school_simulator.generate_service_times()
    school_simulator.generate_arrival_times()
    school_simulator.simulate_enrolment_service()
    school_simulator.save_to_csv()
    school_simulator.generate_average_time_in_system()
    school_simulator.calculate_metrics()
