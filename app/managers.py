import time
from random import randint, random
from uuid import uuid4

from numpy import asarray, savetxt

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

    def live_a_day(self, people_to_connect):
        self.last_test_was -= 1
        self.check_is_need_go_to_doctor()
        if people_to_connect is not None:
            people_to_connect.connect(self.diseases)
            self.connect(people_to_connect.diseases)

    def connect(self, connect_diseases):
        for connect_disease in connect_diseases:
            if len(self.diseases) > 14:
                break
            if decision(DISEASES_LIST.get(connect_disease)):
                self.diseases.append(connect_disease)
        self.is_already_connected_today = True

    def check_is_need_go_to_doctor(self):
        if self.last_test_was < 1:
            self.last_test_was = 180
            self.diseases = []


def save_output_to_file(results: list):
    with open("output.txt", "w") as txt_file:
        txt_file.write(str(results) + "\n")


def simulate_simple_connections() -> list:

    persons = []

    people_with_diseases_by_day = []

    for i in range(POPULATION):
        persons.append(StandardPerson(uuid4()))

    people_with_diseases_by_day.append(len(list(filter(lambda person_to_check: len(person_to_check.diseases) > 0, persons))))

    print(people_with_diseases_by_day)

    save_output_to_file(people_with_diseases_by_day)

    for i in range(TIME_INTERVAL_DAYS):
        for index, person in enumerate(persons):
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
        print('Empty people connections')

        people_with_diseases_by_day.append(len(list(filter(lambda person_to_check: len(person.diseases) > 0, persons))))

        print(f'here\'s come {i} day')

        print(people_with_diseases_by_day)

        save_output_to_file(people_with_diseases_by_day)

    return people_with_diseases_by_day


start_time = time.time()

list_to_print = simulate_simple_connections()

save_output_to_file(list_to_print)

print("--- %s seconds ---" % (time.time() - start_time))

print(list_to_print[0], list_to_print[-1])

