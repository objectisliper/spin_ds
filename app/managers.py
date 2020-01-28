import time
from random import randint, random
from uuid import uuid4
import multiprocessing as mp

from numpy import asarray, savetxt, loadtxt

from app.settings import DISEASES_LIST, POPULATION, TIME_INTERVAL_DAYS


def decision(probability: float) -> bool:
    return random() < probability


class StandardPerson:

    def __init__(self, name: str):
        self.luck = randint(10, 90) / 100
        self.last_test_was = randint(1, 180)
        self.is_already_connected_today = bool(randint(0, 1))
        self.diseases = []
        self.name = name

        for disease in DISEASES_LIST:
            if len(self.diseases) > 14:
                break
            if decision(DISEASES_LIST.get(disease)):
                self.diseases.append(disease)

    def connect(self, connect_diseases):
        for connect_disease in connect_diseases:
            if connect_disease in self.diseases:
                continue
            elif len(self.diseases) > 14:
                break
            elif decision(DISEASES_LIST.get(connect_disease)):
                self.diseases.append(connect_disease)
        self.is_already_connected_today = True

    def check_is_need_go_to_doctor(self):
        if self.last_test_was < 1:
            self.last_test_was = 180
            self.diseases = []


def save_output_to_file(results: list):
    savetxt('output.csv', asarray(results), delimiter=',')


class MultiprocSimulation:

    def __init__(self, population):
        self.population = population

    def process_population(self) -> list:
        # start_of_processing = time.time()
        cores = mp.cpu_count()
        pool = mp.Pool(cores)
        jobs = []

        for start_of_chunk, end_of_chunk in self.chunkify(cores):
            jobs.append(
                pool.apply_async(self.process_wrapper, (start_of_chunk, end_of_chunk)))

        for job in jobs:
            job.get()

        pool.close()

        # end_of_processing = time.time()
        #
        # print('Time wasted ', end_of_processing - start_of_processing)

        return self.population

    def process_wrapper(self, chunk_start, chunk_end):
        for person in self.population[chunk_start: chunk_end]:
            if not person.is_already_connected_today and decision(person.luck):
                list_of_possible_people_to_connect = list(
                        filter(lambda person_to_chose: not person_to_chose.is_already_connected_today and
                               person_to_chose.name != person.name, self.population[chunk_start: chunk_end])
                    )

                people_to_connect = list_of_possible_people_to_connect[randint(0, len(list_of_possible_people_to_connect) - 1)]

                people_to_connect.connect(person.diseases)
                person.connect(people_to_connect.diseases)
            person.last_test_was -= 1
            person.check_is_need_go_to_doctor()
            # person.live_a_day(people_to_connect)
        for person in self.population[chunk_start: chunk_end]:
            person.is_already_connected_today = False

    def chunkify(self, cores: int):
        chunk_end = 0
        step = int(POPULATION/cores)
        for i in range(cores - 2):
            chunk_start = chunk_end
            chunk_end = chunk_start + step
            yield chunk_start, chunk_end
        yield chunk_end, -1


def simulate_simple_connections() -> list:

    persons = []

    people_with_diseases_by_day = []

    for i in range(POPULATION):
        persons.append(StandardPerson(uuid4()))

    people_with_diseases_by_day.append(len(list(filter(lambda person_to_check: len(person_to_check.diseases) > 0, persons))))

    print(people_with_diseases_by_day)

    save_output_to_file(people_with_diseases_by_day)

    for i in range(TIME_INTERVAL_DAYS):
        persons = MultiprocSimulation(persons).process_population()

        people_with_diseases_by_day.append(len(list(filter(lambda person_to_check: len(person_to_check.diseases) > 0, persons))))

        # print(people_with_diseases_by_day)

    return people_with_diseases_by_day


start_time = time.time()

list_to_print = simulate_simple_connections()

save_output_to_file(list_to_print)

print("--- %s seconds ---" % (time.time() - start_time))

print(list_to_print[0], list_to_print[-1])
