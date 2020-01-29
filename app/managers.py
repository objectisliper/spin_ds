import json
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
        self.luck = randint(27, 1000) / 10000
        self.last_test_was = randint(1, 180)
        self.is_already_connected_today = bool(randint(0, 1))
        self.diseases = []
        self.name = name

        for disease in DISEASES_LIST:
            if len(self.diseases) > 14:
                break
            if decision(DISEASES_LIST.get(disease)):
                self.diseases.append(disease)

    def live_a_day(self, person_to_connect):
        if person_to_connect is not None:
            person_to_connect.connect(self.diseases)
            self.connect(person_to_connect.diseases)
        self.last_test_was -= 1
        self.check_is_need_go_to_doctor()

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


def save_output_to_file(results: dict):
    with open('output.json', 'w+') as f:
        f.write(json.dumps(results))


def simulate_simple_connections() -> dict:

    persons = []

    people_with_diseases_by_day = {'HIV': [], 'Chlamydia': [], 'HSV-2': [], 'Gonorrhea': [], 'HBV': []}

    for i in range(POPULATION):
        persons.append(StandardPerson(uuid4()))

    for disease in people_with_diseases_by_day:
        people_with_diseases_by_day[disease].append(
            len(list(filter(lambda person_to_check: disease in person_to_check.diseases, persons)))
        )

    print(people_with_diseases_by_day)

    save_output_to_file(people_with_diseases_by_day)

    for i in range(TIME_INTERVAL_DAYS):
        # persons = MultiprocSimulation(persons).process_population()

        for person in persons:
            if not person.is_already_connected_today and decision(person.luck):
                list_of_possible_people_to_connect = list(
                        filter(lambda person_to_chose: not person_to_chose.is_already_connected_today and
                               person_to_chose.name != person.name, persons)
                    )

                people_to_connect = list_of_possible_people_to_connect[randint(0, len(list_of_possible_people_to_connect) - 1)]
            else:
                people_to_connect = None

            person.live_a_day(people_to_connect)

        for person in persons:
            person.is_already_connected_today = False

        for disease in people_with_diseases_by_day:
            people_with_diseases_by_day[disease].append(
                len(list(filter(lambda person_to_check: disease in person_to_check.diseases, persons)))
            )

        # print(people_with_diseases_by_day)

    return people_with_diseases_by_day


start_time = time.time()

list_to_print = simulate_simple_connections()

print(list_to_print)

save_output_to_file(list_to_print)

print("--- %s seconds ---" % (time.time() - start_time))

